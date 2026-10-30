"""Canvas actions as pure functions on raw model data (M9, spec sections 3 and 4).

Edges are never stored: they follow from expressions and correlation groups. Connecting writes
a preset expression, disconnecting removes an argument from one; a free expression is never
rewritten (PRD §3), the UI opens it instead. Every action is ``Data -> Data`` and is written back
with ``yaml_patch.patch``.
"""

import ast
import copy
from dataclasses import dataclass
from itertools import combinations
from typing import Any, cast

from app.errors import InputError, Issue
from app.model.form import COMMON, param_fields
from app.model.graph import EdgeKind, expression_names
from app.model.yaml_patch import Data

FUNCTIONS = ("max", "min")
OPERATORS: dict[str, type[ast.operator]] = {"sum": ast.Add, "product": ast.Mult}
SYMBOL = {"sum": " + ", "product": " * "}
JOINS = ("sum", "max", "min", "product")  # presets that collect arguments
RANDOM = ("uncertain", "event")  # correlation group members


@dataclass(frozen=True)
class Shape:
    """A preset expression: its kind and argument names; kind None for a free expression."""

    preset: str | None
    args: tuple[str, ...]


def _flatten(node: ast.expr, op: type[ast.operator]) -> list[ast.expr]:
    if isinstance(node, ast.BinOp) and isinstance(node.op, op):
        return _flatten(node.left, op) + _flatten(node.right, op)
    return [node]


def _names(nodes: list[ast.expr]) -> tuple[str, ...] | None:
    names = tuple(n.id for n in nodes if isinstance(n, ast.Name))
    return names if len(names) == len(nodes) else None


def shape(text: str) -> Shape:
    """Recognise a preset expression; anything else is free."""
    if not text.strip():
        return Shape("empty", ())
    try:
        tree = ast.parse(text, mode="eval").body
    except SyntaxError:
        return Shape(None, ())
    if isinstance(tree, ast.Name):
        return Shape("single", (tree.id,))
    if isinstance(tree, ast.Call) and isinstance(tree.func, ast.Name) and not tree.keywords:
        args = _names(list(tree.args))
        if tree.func.id in FUNCTIONS and args is not None:
            return Shape(tree.func.id, args)
    for preset, op in OPERATORS.items():
        args = _names(_flatten(tree, op))
        if isinstance(tree, ast.BinOp) and isinstance(tree.op, op) and args is not None:
            return Shape(preset, args)
    return Shape(None, ())


def render(preset: str, args: tuple[str, ...]) -> str:
    """The expression of a join preset over ``args``; one argument stands alone."""
    if len(args) <= 1:
        return "".join(args)
    if preset in FUNCTIONS:
        return f"{preset}({', '.join(args)})"
    return SYMBOL[preset].join(args)


def _nodes(data: Data) -> dict[str, dict[str, Any]]:
    return cast(dict[str, dict[str, Any]], data.get("nodes") or {})


def _refs(node: dict[str, Any]) -> set[str]:
    texts = [v for k, v in node.items() if isinstance(v, str) and k not in COMMON]
    return {name for text in texts for name in expression_names(text)}


def _depends(data: Data, node_id: str, on: str) -> bool:
    """Whether ``node_id`` refers to ``on``, directly or through other nodes."""
    nodes, seen, todo = _nodes(data), set[str](), [node_id]
    while todo:
        current = todo.pop()
        if current == on:
            return True
        if current not in seen and current in nodes:
            seen.add(current)
            todo.extend(_refs(nodes[current]))
    return False


@dataclass(frozen=True, order=True)
class Link:
    """An edge on the canvas, read from raw data (valid model or not); kinds as ``graph.edges``."""

    source: str
    target: str
    kind: EdgeKind


def links(data: Data) -> list[Link]:
    """Edges of the draft: references in ``expr`` (ausdruck), in parameters or ``p`` (parameter),
    and every pair of a correlation group (korrelation, smaller ID first); sorted."""
    nodes = _nodes(data)
    found: set[Link] = set()
    for node_id, node in nodes.items():
        for key, value in node.items():
            if isinstance(value, str) and key not in COMMON:
                kind: EdgeKind = "ausdruck" if key == "expr" else "parameter"
                names = expression_names(value) & set(nodes) - {node_id}
                found |= {Link(name, node_id, kind) for name in names}
    for group in _groups(data).values():
        members = sorted(set(cast(list[str], group.get("nodes") or [])) & set(nodes))
        found |= {Link(a, b, "korrelation") for a, b in combinations(members, 2)}
    return sorted(found)


def _free(node_id: str, field: str, text: str) -> InputError:
    return InputError(Issue("canvas.free_expression", node_id, field=field, params={"expr": text}))


def presets(data: Data, source: str, target: str) -> list[str]:
    """What connecting ``source`` to ``target`` can mean; the current preset first."""
    if source == target:
        raise InputError(Issue("canvas.self", source))
    if _depends(data, source, target):
        raise InputError(Issue("canvas.cycle", params={"source": source, "target": target}))
    node, kind = _nodes(data)[target], _nodes(data)[source].get("type")
    if node.get("type") == "uncertain":
        return ["param"]
    if node.get("type") == "event":
        return ["p"]
    if node.get("type") not in ("derived", "output"):
        raise InputError(Issue("canvas.no_preset", target, params={"type": node.get("type")}))
    current = shape(str(node.get("expr", ""))).preset
    found = ["edit"] if current is None else sorted(JOINS, key=lambda p: p != current)
    return found + (["delay"] if kind == "event" else [])


def _joined(text: str, source: str, preset: str, node_id: str) -> str:
    found = shape(text)
    if found.preset in ("empty", "single", preset):
        args = found.args if source in found.args else (*found.args, source)
        return render(preset, args)
    raise _free(node_id, "expr", text)


def _scaled(source: str, factor: str) -> str:
    return source if factor.strip() in ("", "1", "1.0") else f"{source} * {factor.strip()}"


def connect(
    data: Data, source: str, target: str, preset: str, field: str = "", value: str = ""
) -> Data:
    """Make ``target`` depend on ``source`` under ``preset``; ``value`` is the parameter factor or
    the delay. Raises ``InputError`` for a free expression or an unknown parameter."""
    out = copy.deepcopy(data)
    node = _nodes(out)[target]
    if preset == "param":
        if field not in {s.name for s in param_fields(data, target)}:
            raise InputError(Issue("canvas.field", target, field=field, params={"field": field}))
        node[field] = _scaled(source, value)
    elif preset == "p":
        node["p"] = source
    elif preset == "delay":
        text = str(node.get("expr", "")).strip()
        delay = f"where({source}, {value.strip() or 0}, 0)"
        node["expr"] = f"{text} + {delay}" if text else delay
    else:
        node["expr"] = _joined(str(node.get("expr", "")), source, preset, target)
    return out


def disconnect(data: Data, source: str, target: str) -> Data:
    """Remove ``source`` from a preset expression of ``target``; anything else raises, naming the
    field to open."""
    out = copy.deepcopy(data)
    node = _nodes(out)[target]
    text = str(node.get("expr", ""))
    found = shape(text)
    if source in found.args:
        rest = tuple(a for a in found.args if a != source)
        node["expr"] = render(found.preset if found.preset in JOINS else "sum", rest)
        return out
    fields = [k for k, v in node.items() if isinstance(v, str) and k not in COMMON]
    field = next((k for k in fields if source in expression_names(node[k])), "expr")
    raise _free(target, field, str(node.get(field, "")))


def _groups(data: Data) -> dict[str, dict[str, Any]]:
    return cast(dict[str, dict[str, Any]], data.get("correlations") or {})


def _group_of(data: Data, node_id: str) -> str | None:
    return next(
        (g for g, group in _groups(data).items() if node_id in group.get("nodes", [])), None
    )


def _check_random(data: Data, *node_ids: str) -> None:
    for node_id in node_ids:
        if _nodes(data)[node_id].get("type") not in RANDOM:
            raise InputError(Issue("canvas.not_random", node_id))


def _grown(group: dict[str, Any], new: str, partner: str, rho: float) -> None:
    """``group`` with ``new`` added, correlated with ``partner`` only."""
    members: list[str] = [*group["nodes"], new]
    rows = [[*row, 0.0] for row in group["spearman"]]
    rows.append([0.0] * (len(members) - 1) + [1.0])
    group["nodes"], group["spearman"] = members, rows
    _set(group, new, partner, rho)


def _set(group: dict[str, Any], a: str, b: str, rho: float) -> None:
    i, j = group["nodes"].index(a), group["nodes"].index(b)
    group["spearman"][i][j] = group["spearman"][j][i] = float(rho)


def correlate(data: Data, a: str, b: str, rho: float) -> Data:
    """Rank correlation ρ between ``a`` and ``b``: a new group, or one of theirs extended."""
    _check_random(data, a, b)
    out = copy.deepcopy(data)
    groups = out.setdefault("correlations", {})
    ga, gb = _group_of(out, a), _group_of(out, b)
    if ga and gb and ga != gb:
        raise InputError(Issue("canvas.other_group", params={"a": a, "b": b, "ga": ga, "gb": gb}))
    if ga is None and gb is None:
        groups[f"{a}_{b}"] = {"nodes": [a, b], "spearman": [[1.0, float(rho)], [float(rho), 1.0]]}
    elif ga == gb:
        _set(groups[ga], a, b, rho)
    elif ga is not None:
        _grown(groups[ga], b, a, rho)
    else:
        _grown(groups[cast(str, gb)], a, b, rho)
    return out


def _shrunk(group: dict[str, Any]) -> None:
    """Drop members without any correlation left."""
    rows: list[list[float]] = group["spearman"]
    keep = [i for i, row in enumerate(rows) if any(v != 0 for j, v in enumerate(row) if j != i)]
    group["nodes"] = [group["nodes"][i] for i in keep]
    group["spearman"] = [[rows[i][j] for j in keep] for i in keep]


def uncorrelate(data: Data, a: str, b: str) -> Data:
    """ρ = 0 between ``a`` and ``b``; uncorrelated members leave, a group below two goes."""
    gid = _group_of(data, a)
    if gid is None or gid != _group_of(data, b):
        return data
    out = copy.deepcopy(data)
    group = _groups(out)[gid]
    _set(group, a, b, 0.0)
    _shrunk(group)
    if len(group["nodes"]) < 2:
        del out["correlations"][gid]
    return out
