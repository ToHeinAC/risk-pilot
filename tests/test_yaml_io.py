"""YAML loading, schema validation and node IDs (M1 AP1)."""

import pytest
import yaml

from app.errors import ModelError
from app.model.schema import ChoiceNode, ConstantNode, OutputNode, UncertainNode
from app.model.yaml_io import model_from_yaml, model_to_yaml

T2 = """
schema_version: 1
model: t2_terminplan
title: "Mini-Terminplan"
settings: {n: 100000, seed: 20261027}
nodes:
  a: {type: uncertain, dist: normal, mean: 10, sd: 2, unit: d, name: "Vorgang A"}
  b: {type: uncertain, dist: normal, mean: "a / 2", sd: 3, unit: d}
  c: {type: constant, value: 24}
  route: {type: choice, options: [{label: ICE, weight: 2}, {label: Bus, weight: 1}]}
  ende: {type: output, expr: "max(a + b, c)", unit: d, target: {le: 30}}
"""


def codes(exc: pytest.ExceptionInfo[ModelError]) -> list[str]:
    return [i.code for i in exc.value.issues]


def test_loads_valid_model() -> None:
    model = model_from_yaml(T2)
    assert model.model == "t2_terminplan"
    assert model.settings.n == 100000
    assert model.settings.seed == 20261027
    a = model.nodes["a"]
    assert isinstance(a, UncertainNode)
    assert a.dist == "normal"
    assert a.params() == {"mean": 10, "sd": 2}
    b = model.nodes["b"]
    assert isinstance(b, UncertainNode)
    assert b.params()["mean"] == "a / 2"
    assert isinstance(model.nodes["c"], ConstantNode)
    assert isinstance(model.nodes["route"], ChoiceNode)
    ende = model.nodes["ende"]
    assert isinstance(ende, OutputNode)
    assert ende.target is not None
    assert ende.target.op == "le"
    assert ende.target.value == 30


def test_settings_defaults() -> None:
    model = model_from_yaml("schema_version: 1\nmodel: m\nnodes:\n  y: {type: output, expr: '1'}\n")
    assert (model.settings.n, model.settings.seed) == (10000, 0)


@pytest.mark.parametrize("unit", ["Mio. EUR", "€/kWh", "Tage (Arbeitstage)", "m²·K"])
def test_unit_passes_through_unchanged(unit: str) -> None:
    text = (
        f"schema_version: 1\nmodel: m\nnodes:\n  y: {{type: output, expr: '1', unit: '{unit}'}}\n"
    )
    assert model_from_yaml(text).nodes["y"].unit == unit


def test_number_strings_accepted_in_number_fields() -> None:
    text = (
        "schema_version: 1\nmodel: m\nsettings: {n: 1e5}\n"
        "nodes:\n  c: {type: constant, value: 2.5e3}\n  y: {type: output, expr: c}\n"
    )
    model = model_from_yaml(text)
    assert model.settings.n == 100000
    c = model.nodes["c"]
    assert isinstance(c, ConstantNode)
    assert c.value == 2500.0


def test_n_must_be_integer() -> None:
    text = (
        "schema_version: 1\nmodel: m\nsettings: {n: 1.5}\nnodes:\n  y: {type: output, expr: '1'}\n"
    )
    with pytest.raises(ModelError) as exc:
        model_from_yaml(text)
    assert codes(exc) == ["model.schema"]


def test_yaml_syntax_error_has_line() -> None:
    with pytest.raises(ModelError) as exc:
        model_from_yaml("schema_version: 1\nmodel: m\nnodes:\n  a: {type: constant, value: [1\n")
    issue = exc.value.issues[0]
    assert issue.code == "yaml.syntax"
    assert issue.line is not None
    assert issue.line >= 4


def test_duplicate_node_id_rejected_with_line() -> None:
    text = (
        "schema_version: 1\nmodel: m\nnodes:\n"
        "  a: {type: constant, value: 1}\n  a: {type: constant, value: 2}\n"
        "  y: {type: output, expr: a}\n"
    )
    with pytest.raises(ModelError) as exc:
        model_from_yaml(text)
    issue = exc.value.issues[0]
    assert (issue.code, issue.line, issue.params["key"]) == ("yaml.duplicate_key", 5, "a")


def test_unknown_key_rejected() -> None:
    text = "schema_version: 1\nmodel: m\nnodes:\n  y: {type: output, expr: '1', sdd: 3}\n"
    with pytest.raises(ModelError) as exc:
        model_from_yaml(text)
    issue = exc.value.issues[0]
    assert (issue.code, issue.node_id, issue.field) == ("model.schema", "y", "sdd")


def test_unknown_schema_version() -> None:
    with pytest.raises(ModelError) as exc:
        model_from_yaml("schema_version: 2\nmodel: m\nnodes: {}\n")
    assert codes(exc) == ["model.schema_version"]


def test_top_level_must_be_mapping() -> None:
    with pytest.raises(ModelError) as exc:
        model_from_yaml("- a\n- b\n")
    assert codes(exc) == ["model.schema"]


@pytest.mark.parametrize("bad", ["A", "1a", "a-b", "max", "where", "lambda", "true", "x" * 65])
def test_invalid_node_ids(bad: str) -> None:
    text = f"schema_version: 1\nmodel: m\nnodes:\n  '{bad}': {{type: output, expr: '1'}}\n"
    with pytest.raises(ModelError) as exc:
        model_from_yaml(text)
    issue = exc.value.issues[0]
    assert (issue.code, issue.node_id) == ("node.id_invalid", bad)


def test_invalid_model_id() -> None:
    with pytest.raises(ModelError) as exc:
        model_from_yaml("schema_version: 1\nmodel: 'Mein Modell'\nnodes: {}\n")
    assert codes(exc) == ["node.id_invalid"]


@pytest.mark.parametrize(
    "options",
    [
        "[{label: A, weight: 1}]",
        "[{label: A, weight: 1}, {label: A, weight: 1}]",
        "[{label: A, weight: 0}, {label: B, weight: 0}]",
        "[{label: A, weight: -1}, {label: B, weight: 2}]",
    ],
)
def test_invalid_choice_options(options: str) -> None:
    text = f"schema_version: 1\nmodel: m\nnodes:\n  r: {{type: choice, options: {options}}}\n"
    with pytest.raises(ModelError) as exc:
        model_from_yaml(text)
    assert codes(exc) == ["model.schema"]


@pytest.mark.parametrize("target", ["{}", "{le: 1, ge: 0}"])
def test_target_needs_exactly_one_operator(target: str) -> None:
    text = (
        f"schema_version: 1\nmodel: m\nnodes:\n  y: {{type: output, expr: '1', target: {target}}}\n"
    )
    with pytest.raises(ModelError) as exc:
        model_from_yaml(text)
    assert codes(exc) == ["model.schema"]


def test_collects_several_issues() -> None:
    text = (
        "schema_version: 1\nmodel: m\nnodes:\n"
        "  a: {type: constant}\n  b: {type: nonsense}\n  y: {type: output, expr: '1'}\n"
    )
    with pytest.raises(ModelError) as exc:
        model_from_yaml(text)
    assert {i.node_id for i in exc.value.issues} == {"a", "b"}


def test_why_and_bounds_and_tags() -> None:
    text = (
        "schema_version: 1\nmodel: m\nnodes:\n"
        "  a: {type: uncertain, dist: normal, mean: 1, sd: 1, bounds: {min: 0},\n"
        "      why: {text: Studie, links: ['https://example.org'], date: '2026-10-01'},\n"
        "      tags: [kosten], track: true}\n"
        "  y: {type: output, expr: a}\n"
    )
    a = model_from_yaml(text).nodes["a"]
    assert a.bounds is not None
    assert (a.bounds.min, a.bounds.max) == (0, None)
    assert a.tags == ["kosten"]
    assert a.track is True


def test_roundtrip() -> None:
    model = model_from_yaml(T2)
    assert model_from_yaml(model_to_yaml(model)) == model
    assert yaml.safe_load(model_to_yaml(model))["nodes"]["a"]["mean"] == 10


def test_missing_schema_version_is_schema_error() -> None:
    with pytest.raises(ModelError) as exc:
        model_from_yaml("model: m\nnodes: {}\n")
    issue = exc.value.issues[0]
    assert (issue.code, issue.field) == ("model.schema", "schema_version")


def test_boolean_schema_version_rejected() -> None:
    with pytest.raises(ModelError) as exc:
        model_from_yaml("schema_version: true\nmodel: m\nnodes: {}\n")
    assert codes(exc) == ["model.schema_version"]
