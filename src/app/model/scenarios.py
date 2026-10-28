"""Scenarios: inheritance chain, effective model, validation, diff and editing (pure)."""

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Any

from pydantic import ValidationError

from app.errors import Issue, ModelError, Notice
from app.model.compile import compile_model
from app.model.schema import BASIS, Model, Scenario, id_problem
from app.model.yaml_io import issues_from_validation

META = ("why", "inactive")
_LABEL_FIELDS = frozenset({"name", "unit", "description", "tags", "track"})
_COMMON = ("type", "name", "unit", "description", "why", "tags", "bounds", "track")
_FIELDS = {
    "constant": {"value", "bounds"},
    "event": {"p", "bounds"},
    "choice": {"options"},
    "derived": {"expr", "bounds"},
    "output": {"expr", "target", "better", "bounds", "horizon", "loss_reference"},
}

Data = dict[str, Any]


@dataclass(frozen=True)
class DiffRow:
    node: str
    field: str
    before: object
    after: object
    why: str | None
    status: str  # "geändert" | "gleich" | "inaktiv"


def chain(model: Model, scenario_id: str) -> list[str]:
    """IDs from the root (basis or a detached scenario) down to ``scenario_id``."""
    path: list[str] = []
    current = scenario_id
    while current != BASIS:
        if current not in model.scenarios:
            raise ModelError(
                [Issue("scenario.parent_unknown", scenario=scenario_id, params={"parent": current})]
            )
        if current in path:
            cycle = [*path[path.index(current) :], current]
            raise ModelError(
                [Issue("scenario.parent_cycle", scenario=scenario_id, params={"cycle": cycle})]
            )
        path.append(current)
        scenario = model.scenarios[current]
        if scenario.nodes is not None:
            return list(reversed(path))
        current = scenario.parent
    return [BASIS, *reversed(path)]


def _nodes_data(nodes: Mapping[str, Any]) -> dict[str, Data]:
    return {k: v.model_dump(mode="json", exclude_unset=True) for k, v in nodes.items()}


def _apply(data: dict[str, Data], overrides: Mapping[str, Mapping[str, Any]]) -> None:
    for node_id, fields in overrides.items():
        if fields.get("inactive") or node_id not in data:
            continue
        values = {k: v for k, v in fields.items() if k not in META}
        target = data[node_id]
        if target.get("type") == "uncertain" and ("dist" in values or "input" in values):
            target = {k: target[k] for k in _COMMON if k in target} | {"dist": target["dist"]}
        data[node_id] = {**target, **values}


def effective_model(model: Model, scenario_id: str) -> Model:
    """The main model with the overrides of the chain applied; without scenarios."""
    ids = chain(model, scenario_id)
    root = model.nodes if ids[0] == BASIS else (model.scenarios[ids[0]].nodes or {})
    data = _nodes_data(root)
    for sid in ids[1:]:
        _apply(data, model.scenarios[sid].overrides)
    top = model.model_dump(mode="json", exclude_unset=True, exclude={"scenarios", "nodes"})
    groups = {gid: dict(g) for gid, g in top.get("correlations", {}).items()}
    for sid in (i for i in ids if i != BASIS):  # a detached root keeps its frozen matrices
        for gid, fields in (model.scenarios[sid].correlations or {}).items():
            if gid in groups:
                groups[gid].update(fields)
    if groups:
        top["correlations"] = groups
    try:
        return Model.model_validate({**top, "nodes": data})
    except ValidationError as exc:
        raise ModelError(issues_from_validation(exc)) from exc


def _root_nodes(model: Model, sid: str) -> Mapping[str, Any]:
    """Nodes of the chain's root: the main model, or a detached scenario's frozen set."""
    root = chain(model, sid)[0]
    return model.nodes if root == BASIS else (model.scenarios[root].nodes or {})


def _override_issues(
    model: Model, sid: str, scenario: Scenario
) -> tuple[list[Issue], list[Notice]]:
    issues: list[Issue] = []
    notices: list[Notice] = []
    nodes = _root_nodes(model, sid)
    for node_id, fields in scenario.overrides.items():
        node = nodes.get(node_id)
        if node is None:
            if fields.get("inactive"):
                notices.append(Notice("scenario.inactive", node_id, scenario=sid))
            else:
                issues.append(Issue("scenario.node_unknown", node_id, scenario=sid))
            continue
        for name in fields:
            if name in META:
                continue
            if name == "type":
                issues.append(Issue("scenario.type_change", node_id, "type", scenario=sid))
            elif not _allowed(node.type, name):
                issues.append(Issue("scenario.field_invalid", node_id, name, scenario=sid))
    return issues, notices


def _allowed(node_type: str, field: str) -> bool:
    if field in _LABEL_FIELDS:
        return False
    return node_type == "uncertain" or field in _FIELDS[node_type]


def _same_values(model: Model, sid: str, scenario: Scenario) -> list[Notice]:
    if scenario.nodes is not None:
        return []
    parent = _nodes_data(effective_model(model, scenario.parent).nodes)
    return [
        Notice("scenario.same_value", node_id, scenario=sid, params={"field": name})
        for node_id, fields in scenario.overrides.items()
        if node_id in parent and not fields.get("inactive")
        for name, value in fields.items()
        if name not in META and parent[node_id].get(name) == value
    ]


def _correlation_issues(model: Model, sid: str, scenario: Scenario) -> list[Issue]:
    """Scenarios may replace the matrix (and reason) of an existing group, nothing else."""
    issues: list[Issue] = []
    for gid, fields in (scenario.correlations or {}).items():
        if gid not in model.correlations:
            issues.append(Issue("scenario.corr_unknown", scenario=sid, params={"group": gid}))
        elif set(fields) - {"spearman", "why"}:
            issues.append(Issue("scenario.corr_field", scenario=sid, params={"group": gid}))
    return issues


def _check(model: Model, sid: str, compile_scenarios: bool) -> tuple[list[Issue], list[Notice]]:
    scenario = model.scenarios[sid]
    issues = _correlation_issues(model, sid, scenario)
    try:
        chain(model, sid)
    except ModelError as exc:
        return issues + exc.issues, []
    found, notices = _override_issues(model, sid, scenario)
    issues += found
    if issues or not compile_scenarios:
        return issues, notices
    try:
        compile_model(effective_model(model, sid))
    except ModelError as exc:
        return [replace(i, scenario=sid) for i in exc.issues], notices
    return [], notices + _same_values(model, sid, scenario)


def validate(model: Model, compile_scenarios: bool = True) -> tuple[list[Issue], list[Notice]]:
    """All problems and hints of all scenarios; each scenario is also compiled as a model.

    ``compile_scenarios=False`` checks only the scenario structure (used when the main scenario
    itself does not compile, so its errors are not repeated once per scenario).
    """
    issues: list[Issue] = []
    notices: list[Notice] = []
    for sid in model.scenarios:
        found, hints = _check(model, sid, compile_scenarios)
        issues += found
        notices += hints
    return issues, notices


def diff(model: Model, scenario_id: str) -> list[DiffRow]:
    """Exactly the overrides of a scenario, each against its parent's effective value."""
    scenario = model.scenarios[scenario_id]
    parent_id = scenario.detached_from or BASIS if scenario.nodes is not None else scenario.parent
    parent_model = effective_model(model, parent_id)
    parent = _nodes_data(parent_model.nodes)
    matrices = _correlation_rows(parent_model, scenario)
    if scenario.nodes is not None:
        return _detached_diff(parent, _nodes_data(scenario.nodes)) + matrices
    rows: list[DiffRow] = []
    for node_id, fields in scenario.overrides.items():
        for name, value in fields.items():
            if name in META:
                continue
            before = parent.get(node_id, {}).get(name)
            status = (
                "inaktiv" if fields.get("inactive") else "gleich" if before == value else "geändert"
            )
            rows.append(DiffRow(node_id, name, before, value, fields.get("why"), status))
    return rows + matrices


def _correlation_rows(parent: Model, scenario: Scenario) -> list[DiffRow]:
    """Replaced matrices of correlation groups; the group ID stands in the node column."""
    rows: list[DiffRow] = []
    for gid, fields in (scenario.correlations or {}).items():
        if "spearman" not in fields or gid not in parent.correlations:
            continue
        before = parent.correlations[gid].spearman
        after = fields["spearman"]
        status = "gleich" if before == after else "geändert"
        rows.append(DiffRow(gid, "spearman", before, after, fields.get("why"), status))
    return rows


def _detached_diff(parent: dict[str, Data], own: dict[str, Data]) -> list[DiffRow]:
    rows: list[DiffRow] = []
    for node_id, fields in own.items():
        for name, value in fields.items():
            before = parent.get(node_id, {}).get(name)
            if before != value:
                rows.append(DiffRow(node_id, name, before, value, None, "geändert"))
    return rows


def _with_scenarios(model: Model, scenarios: dict[str, Data]) -> Model:
    data = model.model_dump(mode="json", exclude_unset=True)
    data["scenarios"] = scenarios
    return Model.model_validate(data)


def _scenarios_data(model: Model) -> dict[str, Data]:
    return {k: v.model_dump(mode="json", exclude_unset=True) for k, v in model.scenarios.items()}


def _new_id(model: Model, new_id: str) -> None:
    if new_id == BASIS or new_id in model.scenarios:
        raise ValueError(f"Die Szenario-ID „{new_id}“ ist schon vergeben.")
    reason = id_problem(new_id)
    if reason:
        raise ValueError(f"Die Szenario-ID „{new_id}“ ist nicht zulässig: {reason}.")


def add_scenario(model: Model, sid: str, name: str, parent: str, why: str) -> Model:
    _new_id(model, sid)
    if not why.strip():
        raise ValueError("Ein Szenario braucht eine Begründung.")
    entry: Data = {"name": name, "why": why, "overrides": {}}
    if parent != BASIS:
        entry["parent"] = parent
    return _with_scenarios(model, {**_scenarios_data(model), sid: entry})


def set_override(
    model: Model, sid: str, node: str, field: str, value: Any, why: str | None
) -> Model:
    nodes = _root_nodes(model, sid)
    if node not in nodes:
        raise ValueError(f"Den Knoten „{node}“ gibt es nicht.")
    if field in META or field == "type" or not _allowed(nodes[node].type, field):
        raise ValueError(f"Knoten „{node}“: Das Feld „{field}“ lässt sich nicht überschreiben.")
    data = _scenarios_data(model)
    fields = data[sid].setdefault("overrides", {}).setdefault(node, {})
    fields[field] = value
    if why:
        fields["why"] = why
    return _with_scenarios(model, data)


def remove_override(model: Model, sid: str, node: str, field: str) -> Model:
    data = _scenarios_data(model)
    overrides = data[sid].get("overrides", {})
    overrides.get(node, {}).pop(field, None)
    if node in overrides and not set(overrides[node]) - set(META):
        del overrides[node]
    return _with_scenarios(model, data)


def mark_unknown_inactive(model: Model) -> Model:
    """Mark overrides of nodes that no longer exist as inactive (visible, never silent)."""
    data = _scenarios_data(model)
    for entry in data.values():
        for node_id, fields in entry.get("overrides", {}).items():
            if node_id not in model.nodes:
                fields["inactive"] = True
    return _with_scenarios(model, data)


def duplicate(model: Model, sid: str, new_id: str) -> Model:
    _new_id(model, new_id)
    data = _scenarios_data(model)
    copy = dict(data[sid])
    copy["name"] = f"Kopie von {copy['name']}"
    return _with_scenarios(model, {**data, new_id: copy})


def detach(model: Model, sid: str) -> Model:
    """Freeze the effective model into the scenario; later parent changes no longer apply."""
    data = _scenarios_data(model)
    entry = data[sid]
    effective = effective_model(model, sid)
    data[sid] = {
        "name": entry["name"],
        "why": entry["why"],
        "nodes": _nodes_data(effective.nodes),
        "detached_from": entry.get("parent", BASIS),
    }
    if effective.correlations:
        data[sid]["correlations"] = {
            gid: {"spearman": g.spearman} for gid, g in effective.correlations.items()
        }
    return _with_scenarios(model, data)


def tree(model: Model) -> list[tuple[str, int]]:
    """(ID, depth) in display order: basis, then each scenario below its parent."""
    order: list[tuple[str, int]] = [(BASIS, 0)]

    def children(parent: str) -> list[str]:
        return [
            sid
            for sid, s in model.scenarios.items()
            if (s.nodes is None and s.parent == parent) or (s.nodes is not None and parent == BASIS)
        ]

    def walk(parent: str, depth: int) -> None:
        for sid in children(parent):
            if all(sid != seen for seen, _ in order):
                order.append((sid, depth))
                walk(sid, depth + 1)

    walk(BASIS, 1)
    order += [(sid, 1) for sid in model.scenarios if all(sid != seen for seen, _ in order)]
    return order
