"""Form values <-> raw model data (M6 AK 2), pure.

The form edits the data read from the YAML text, valid model or not, so a new node may stay
incomplete until its fields are filled (E5). ``apply`` writes only the fields whose form value
changed; everything else stays exactly as it was, which makes the round trip lossless.
"""

import copy
import re
from typing import Any, cast

from app.dists.base import ParamSpec
from app.dists.registry import get_family
from app.errors import InputError, Issue
from app.model.graph import expression_names
from app.model.schema import id_problem
from app.model.yaml_patch import Data

Values = dict[str, Any]

TEXT = ("name", "unit", "description", "expr", "better", "dist", "input")
NUMBERS = ("value", "p", "horizon", "loss_reference")  # number or expression text
TYPE_FIELDS = {
    "constant": ("value",),
    "event": ("p",),
    "derived": ("expr",),
    "output": ("expr", "better", "horizon", "loss_reference", "target_op", "target_value"),
    "uncertain": ("dist", "input"),
    "choice": ("options",),
}
COMMON = ("type", "dist", "input", "name", "unit", "description", "why", "tags", "bounds", "track")
TARGET_OPS = ("le", "lt", "ge", "gt")
_NUMBER = re.compile(r"^[+-]?(\d+([.,]\d*)?|[.,]\d+)([eE][+-]?\d+)?$")
_LIST_SPLIT = re.compile(r"[;\s]+")


def _fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(_fmt(v) for v in cast(list[Any], value))
    return repr(value) if isinstance(value, float) else str(value)


def number(text: str) -> int | float | None:
    """A number typed in German or English notation (``2,5`` or ``2.5``), else None."""
    text = text.strip()
    if not _NUMBER.match(text):
        return None
    text = text.replace(",", ".")
    return int(text) if text.lstrip("+-").isdigit() else float(text)


def _scalar(text: str) -> int | float | str:
    parsed = number(text)
    return text.strip() if parsed is None else parsed


def _numbers(text: str) -> list[int | float]:
    items = [p for p in _LIST_SPLIT.split(text.strip()) if p]
    parsed = [number(p) for p in items]
    bad = [p for p, x in zip(items, parsed, strict=True) if x is None]
    if bad:
        raise InputError(Issue("form.list", params={"value": bad[0]}))
    return [x for x in parsed if x is not None]


def node_ids(data: Data) -> list[str]:
    return list(cast(dict[str, Any], data.get("nodes") or {}))


def _node(data: Data, node_id: str) -> dict[str, Any]:
    return cast(dict[str, Any], data["nodes"][node_id])


def _with_node(data: Data, node_id: str, node: dict[str, Any]) -> Data:
    return {**data, "nodes": {**data.get("nodes", {}), node_id: node}}


def param_fields(data: Data, node_id: str) -> list[ParamSpec]:
    """Parameter fields of an uncertain node: the family's mode, then unknown extra keys."""
    node = _node(data, node_id)
    family = get_family(str(node.get("dist", "")))
    specs = list(family.modes.get(str(node.get("input", "params")), ())) if family else []
    known = {s.name for s in specs} | set(COMMON)
    extra = [ParamSpec(k, is_list=isinstance(v, list)) for k, v in node.items() if k not in known]
    return specs + extra


def _why_text(node: dict[str, Any]) -> str:
    why = node.get("why")
    return str(cast(dict[str, Any], why).get("text", "")) if isinstance(why, dict) else _fmt(why)


def _common_values(node: dict[str, Any]) -> Values:
    bounds = cast(dict[str, Any], node.get("bounds") or {})
    return {
        "name": _fmt(node.get("name")),
        "unit": _fmt(node.get("unit")),
        "description": _fmt(node.get("description")),
        "why": _why_text(node),
        "tags": ", ".join(str(t) for t in node.get("tags", [])),
        "bounds_min": _fmt(bounds.get("min")),
        "bounds_max": _fmt(bounds.get("max")),
        "track": bool(node.get("track", False)),
    }


def values(data: Data, node_id: str) -> Values:
    """The form's view of one node: texts, ``track`` as bool, options as (label, weight)."""
    node = _node(data, node_id)
    result = {"type": str(node.get("type", "")), **_common_values(node)}
    target = cast(dict[str, Any], node.get("target") or {})
    for name in TYPE_FIELDS.get(result["type"], ()):
        if name == "target_op":
            result[name] = next((op for op in TARGET_OPS if op in target), "")
        elif name == "target_value":
            result[name] = next((_fmt(target[op]) for op in TARGET_OPS if op in target), "")
        elif name == "options":
            options = cast(list[dict[str, Any]], node.get("options", []))
            result[name] = [(_fmt(o.get("label")), _fmt(o.get("weight"))) for o in options]
        else:
            result[name] = _fmt(node.get(name))
    if result["type"] == "uncertain":
        for spec in param_fields(data, node_id):
            result[f"param.{spec.name}"] = _fmt(node.get(spec.name))
    return result


def _put(target: dict[str, Any], key: str, value: Any) -> None:
    if value is None or value is False or value == "" or value == []:  # 0 is a value
        target.pop(key, None)
    else:
        target[key] = value


def _set_why(node: dict[str, Any], text: str) -> None:
    why = node.get("why")
    if isinstance(why, dict):  # links and date stay, also when the text is cleared
        node["why"] = {**cast(dict[str, Any], why), "text": text}
    else:
        _put(node, "why", text)


def _set_bound(node: dict[str, Any], side: str, text: str) -> None:
    bounds = dict(cast(dict[str, Any], node.get("bounds") or {}))
    value = number(text) if text.strip() else None
    if text.strip() and value is None:
        raise InputError(Issue("form.number", params={"value": text.strip()}))
    _put(bounds, side, value)
    _put(node, "bounds", bounds or None)


def _set_target(node: dict[str, Any], op: str, text: str) -> None:
    _put(node, "target", {op: _scalar(text)} if op else None)


def _set_param(node: dict[str, Any], spec: ParamSpec, text: str) -> None:
    is_list = spec.is_list or isinstance(node.get(spec.name), list)
    _put(node, spec.name, (_numbers(text) if is_list else _scalar(text)) if text.strip() else None)


def _set(node: dict[str, Any], key: str, value: Any, specs: dict[str, ParamSpec]) -> None:
    if key in TEXT:
        _put(node, key, str(value).strip())
    elif key in NUMBERS:
        _put(node, key, _scalar(str(value)) if str(value).strip() else None)
    elif key == "why":
        _set_why(node, str(value).strip())
    elif key == "tags":
        _put(node, "tags", [t.strip() for t in str(value).split(",") if t.strip()])
    elif key in ("bounds_min", "bounds_max"):
        _set_bound(node, key.removeprefix("bounds_"), str(value))
    elif key == "track":
        _put(node, "track", bool(value))
    elif key == "options":
        rows = cast(list[tuple[str, str]], value)
        _put(node, "options", [{"label": label, "weight": _scalar(w)} for label, w in rows])
    elif key.startswith("param."):
        name = key.removeprefix("param.")
        _set_param(node, specs.get(name, ParamSpec(name)), str(value))


def apply(data: Data, node_id: str, new: Values) -> Data:
    """``data`` with the changed form fields of ``node_id`` written; the input stays unchanged."""
    old = values(data, node_id)
    node = copy.deepcopy(_node(data, node_id))
    changed = {k: v for k, v in new.items() if old.get(k) != v}
    for key, value in changed.items():
        if not key.startswith("param.") and key not in ("target_op", "target_value"):
            _set(node, key, value, {})
    # parameters last: which fields are lists follows from the (possibly new) distribution
    specs = {s.name: s for s in param_fields(_with_node(data, node_id, node), node_id)}
    for key, value in changed.items():
        if key.startswith("param."):
            _set(node, key, value, specs)
    if "target_op" in changed or "target_value" in changed:
        _set_target(node, str(new.get("target_op", "")), str(new.get("target_value", "")))
    return _with_node(data, node_id, node)


def set_dist(data: Data, node_id: str, dist: str, mode: str) -> Data:
    """Another distribution or input mode; only parameters the new mode knows are kept."""
    node = copy.deepcopy(_node(data, node_id))
    family = get_family(dist)
    allowed = {s.name for s in family.modes.get(mode, ())} if family else set[str]()
    node = {k: v for k, v in node.items() if k in COMMON or k in allowed}
    node["dist"] = dist
    if mode != "params" or "input" in node:
        node["input"] = mode
    return _with_node(data, node_id, node)


def header_values(data: Data) -> Values:
    settings = cast(dict[str, Any], data.get("settings") or {})
    return {
        "title": _fmt(data.get("title")),
        "description": _fmt(data.get("description")),
        "illustrative": bool(data.get("illustrative", False)),
        "n": _fmt(settings.get("n")),
        "seed": _fmt(settings.get("seed")),
    }


def apply_header(data: Data, new: Values) -> Data:
    """``data`` with the changed header fields (title, description, illustrative, n, seed)."""
    old = header_values(data)
    out = copy.deepcopy(data)
    settings = cast(dict[str, Any], out.get("settings") or {})
    for key, value in new.items():
        if old.get(key) == value:
            continue
        if key in ("n", "seed"):
            _put(settings, key, _scalar(str(value)) if str(value).strip() else None)
            _put(out, "settings", settings or None)
        else:
            _put(out, key, value.strip() if isinstance(value, str) else bool(value))
    return out


def add_node(data: Data, node_id: str, node_type: str) -> Data:
    """A new node with only its type; required fields stay empty and are reported (E5)."""
    reason = id_problem(node_id)
    if reason:
        raise InputError(Issue("node.id_invalid", params={"id": node_id, "reason": reason}))
    if node_id in data.get("nodes", {}):
        raise InputError(Issue("form.exists", params={"id": node_id}))
    return _with_node(data, node_id, {"type": node_type})


def _uses(node: Any, node_id: str) -> bool:
    if not isinstance(node, dict):
        return False
    texts = [
        v for k, v in cast(dict[str, Any], node).items() if isinstance(v, str) and k not in COMMON
    ]
    return any(node_id in expression_names(t) for t in texts)


def references(data: Data, node_id: str) -> list[str]:
    """Nodes, scenarios and correlation groups that refer to ``node_id``."""
    refs = [n for n, node in data.get("nodes", {}).items() if n != node_id and _uses(node, node_id)]
    for sid, scenario in cast(dict[str, dict[str, Any]], data.get("scenarios") or {}).items():
        overrides = cast(dict[str, Any], scenario.get("overrides") or {})
        own = cast(dict[str, Any], scenario.get("nodes") or {})
        if (
            node_id in overrides
            or node_id in own
            or any(_uses(o, node_id) for o in overrides.values())
        ):
            refs.append(f"Szenario {sid}")
    for gid, group in cast(dict[str, dict[str, Any]], data.get("correlations") or {}).items():
        if node_id in group.get("nodes", []):
            refs.append(f"Korrelationsgruppe {gid}")
    return refs


def remove_node(data: Data, node_id: str) -> Data:
    """``data`` without ``node_id``; refused while anything still refers to it (E6)."""
    refs = references(data, node_id)
    if refs:
        raise InputError(Issue("form.referenced", node_id, params={"refs": refs}))
    nodes = {k: v for k, v in data["nodes"].items() if k != node_id}
    return {**data, "nodes": nodes}
