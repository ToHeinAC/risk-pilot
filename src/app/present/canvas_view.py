"""What the canvas draws (M9 AP4): Vue Flow nodes and edges from the raw draft, valid or not.

Pure. Node positions come from the ``layout`` block, else from the layered layout; edges are
derived (``canvas.links``) and carry their kind in the ID, so an event on an edge reads back.
"""

import math
from collections.abc import Mapping
from typing import Any, cast

from app.messages import t
from app.model import canvas, layout
from app.model.graph import EdgeKind
from app.model.yaml_patch import Data
from app.present import structure
from app.present.structure import type_label
from app.present.text import number

KINDS: tuple[EdgeKind, ...] = ("ausdruck", "parameter", "korrelation")


def _node(
    node_id: str,
    node: dict[str, Any],
    pos: tuple[float, float],
    selected: bool,
    changed: int,
    used: bool,
) -> dict[str, Any]:
    """One node; its hover hint is the description, or why it is faded (on no output's path)."""
    kind = str(node.get("type", ""))
    data = {"label": str(node.get("name") or node_id), "type": type_label(kind)}
    if changed:
        data["badge"] = str(changed)
    hint = str(node.get("description") or "") if used else t("canvas.unused")
    if hint:
        data["hint"] = hint
    classes = f"rp-node rp-{kind}" + (" rp-selected" if selected else "")
    classes += "" if used else " rp-faded"
    return {
        "id": node_id,
        "position": {"x": pos[0], "y": pos[1]},
        "data": data,
        "class": classes + (" rp-changed" if changed else ""),
        "sourcePosition": "right",
        "targetPosition": "left",
    }


def _edge(link: canvas.Link) -> dict[str, Any]:
    edge: dict[str, Any] = {
        "id": f"{link.kind}:{link.source}->{link.target}",
        "source": link.source,
        "target": link.target,
        "class": f"rp-edge-{link.kind}",
    }
    if link.kind != "korrelation":
        edge["markerEnd"] = "arrowclosed"
    return edge


def view(
    data: Data, selected: str | None, marks: dict[str, int] | None = None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Nodes in the order of ``nodes`` and edges, as Vue Flow props; ``marks`` counts the
    overrides per node in scenario mode. Nodes no output depends on are faded."""
    nodes = cast(dict[str, dict[str, Any]], data.get("nodes") or {})
    pos = layout.placed(data, auto(data))
    counts = marks or {}
    outputs = [n for n, node in nodes.items() if node.get("type") == "output"]
    used = _upstream(data, *outputs) if outputs else set(nodes)
    drawn = [
        _node(n, node, pos[n], n == selected, counts.get(n, 0), n in used)
        for n, node in nodes.items()
    ]
    return drawn, [_edge(k) for k in canvas.links(data)]


def auto(data: Data) -> layout.Layered:
    """The layered layout of the draft (correlations do not order the layers)."""
    nodes = cast(dict[str, Any], data.get("nodes") or {})
    directed = [(k.source, k.target) for k in canvas.links(data) if k.kind != "korrelation"]
    return layout.layers(list(nodes), directed)


def edge_of(edge_id: str) -> tuple[str, str, EdgeKind] | None:
    """(source, target, kind) of an edge ID from ``view``; None for anything else."""
    kind, _, pair = edge_id.partition(":")
    source, _, target = pair.partition("->")
    if kind not in KINDS or not source or not target:
        return None
    return source, target, kind


def name(data: Data, node_id: str) -> str:
    nodes = cast(dict[str, dict[str, Any]], data.get("nodes") or {})
    return str(nodes.get(node_id, {}).get("name") or node_id)


def _listed(names: list[str]) -> str:
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} und {names[-1]}"


def describe(data: Data, source: str, target: str, preset: str, value: str, field: str = "") -> str:
    """The link in plain words, read from ``data`` after the change."""
    s, tg = name(data, source), name(data, target)
    if preset in canvas.JOINS:
        nodes = cast(dict[str, dict[str, Any]], data.get("nodes") or {})
        args = canvas.shape(str(nodes[target].get("expr", ""))).args
        names = [name(data, a) for a in args]
        if len(names) == 1:
            return f"{tg} = {names[0]}"
        return t("canvas.says_join", target=tg, op=t(f"canvas.op_{preset}"), args=_listed(names))
    factor = "" if value.strip() in ("", "1", "1.0") else f" × {value.strip()}"
    params = {"source": s, "target": tg, "value": value.strip(), "field": field, "factor": factor}
    return t(f"canvas.says_{preset}", **params)


def _upstream(data: Data, *outputs: str) -> set[str]:
    """``outputs`` and every node they depend on (expressions and parameters)."""
    inputs: dict[str, set[str]] = {}
    for link in canvas.links(data):
        if link.kind != "korrelation":
            inputs.setdefault(link.target, set()).add(link.source)
    found, todo = set(outputs), list(outputs)
    while todo:
        for source in inputs.get(todo.pop(), set()) - found:
            found.add(source)
            todo.append(source)
    return found


def analysis_view(
    data: Data, values: Mapping[str, float], output: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """The read-only canvas of the analysis page: each node's value (in [0, 1]) as a coloured
    badge; nodes without a path to ``output`` are faded."""
    nodes, edges = view(data, None)
    on_path = _upstream(data, output)
    for node in nodes:
        value = values.get(node["id"])
        if value is not None and math.isfinite(value):
            node["data"]["badge"] = number(value)
            node["data"]["tint"] = structure.color(value)
        if node["id"] not in on_path and "rp-faded" not in node["class"]:
            node["class"] += " rp-faded"
    return nodes, edges
