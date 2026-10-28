"""YAML text <-> Model, pure (no file I/O)."""

from typing import Any, cast

import yaml
from pydantic import ValidationError

from app.errors import Issue, ModelError
from app.model.schema import Model, id_problem

_PYDANTIC_DE = {
    "missing": "Angabe fehlt",
    "extra_forbidden": "unbekannter Schlüssel",
    "float_parsing": "Zahl erwartet",
    "float_type": "Zahl erwartet",
    "int_parsing": "ganze Zahl erwartet",
    "int_type": "ganze Zahl erwartet",
    "int_from_float": "ganze Zahl erwartet",
    "string_type": "Text erwartet",
    "bool_type": "true oder false erwartet",
    "bool_parsing": "true oder false erwartet",
    "list_type": "Liste erwartet",
    "dict_type": "Zuordnung (Schlüssel: Wert) erwartet",
    "model_type": "Zuordnung (Schlüssel: Wert) erwartet",
    "union_tag_invalid": "unbekannter Knotentyp",
    "union_tag_not_found": "Feld „type“ fehlt",
    "greater_than_equal": "Wert zu klein",
    "literal_error": "unzulässiger Wert",
}
_NODE_TYPES = ("constant", "uncertain", "event", "choice", "derived", "output")


class _UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate mapping keys instead of keeping the last one."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        seen: set[object] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)  # pyright: ignore[reportUnknownMemberType]
            if key in seen:
                raise ModelError(
                    [
                        Issue(
                            "yaml.duplicate_key",
                            line=key_node.start_mark.line + 1,
                            params={"key": str(key)},
                        )
                    ]
                )
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def _parse(text: str) -> object:
    try:
        return yaml.load(text, Loader=_UniqueKeyLoader)  # SafeLoader subclass, no Python tags
    except yaml.MarkedYAMLError as exc:
        mark = exc.problem_mark or exc.context_mark
        line = mark.line + 1 if mark else None
        raise ModelError(
            [Issue("yaml.syntax", line=line, params={"problem": exc.problem or str(exc)})]
        ) from exc
    except yaml.YAMLError as exc:
        raise ModelError([Issue("yaml.syntax", params={"problem": str(exc)})]) from exc


def _issue_from_pydantic(error: Any) -> Issue:
    loc = [str(p) for p in error["loc"] if p not in _NODE_TYPES]
    node_id = loc[1] if len(loc) > 1 and loc[0] == "nodes" else None
    msg = _PYDANTIC_DE.get(error["type"])
    if msg is None:
        msg = str(error["msg"]).removeprefix("Value error, ")
    return Issue(
        "model.schema",
        node_id=node_id,
        field=loc[-1] if loc else None,
        params={"loc": ".".join(loc) or "Modell", "msg": msg},
    )


def _id_issues(model: Model) -> list[Issue]:
    issues: list[Issue] = []
    for value, node_id in [(model.model, None), *((k, k) for k in model.nodes)]:
        reason = id_problem(value)
        if reason:
            issues.append(
                Issue("node.id_invalid", node_id=node_id, params={"id": value, "reason": reason})
            )
    return issues


def model_from_yaml(text: str) -> Model:
    """Parse and validate a model; raise ModelError with all problems found."""
    data = _parse(text)
    if not isinstance(data, dict):
        raise ModelError(
            [Issue("model.schema", params={"loc": "Modell", "msg": "Zuordnung erwartet"})]
        )
    if "schema_version" not in data:
        params = {"loc": "schema_version", "msg": _PYDANTIC_DE["missing"]}
        raise ModelError([Issue("model.schema", field="schema_version", params=params)])
    version = cast(dict[str, object], data)["schema_version"]
    if isinstance(version, bool) or version != 1:
        raise ModelError([Issue("model.schema_version", params={"version": str(version)})])
    try:
        model = Model.model_validate(data)
    except ValidationError as exc:
        raise ModelError([_issue_from_pydantic(e) for e in exc.errors()]) from exc
    issues = _id_issues(model)
    if issues:
        raise ModelError(issues)
    return model


def model_to_yaml(model: Model) -> str:
    """Serialise a model to YAML; ``model_from_yaml`` reads it back to an equal model."""
    data = model.model_dump(mode="json", exclude_unset=True)
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
