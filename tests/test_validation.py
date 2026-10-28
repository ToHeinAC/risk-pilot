"""Compile-time validation: parameters, expressions, model structure (M1 AK 3, AP4)."""

import pytest
from test_dists import INVALID

from app.errors import Issue, ModelError
from app.model.compile import CompiledModel, compile_model
from app.model.yaml_io import model_from_yaml


def compile_text(nodes: str) -> CompiledModel:
    return compile_model(model_from_yaml(f"schema_version: 1\nmodel: m\nnodes:\n{nodes}"))


def issues(nodes: str) -> list[Issue]:
    with pytest.raises(ModelError) as exc:
        compile_text(nodes)
    return exc.value.issues


def node_yaml(dist: str, mode: str, given: dict[str, float]) -> str:
    fields = ", ".join(f"{k}: {v}" for k, v in given.items())
    return (
        f"  x: {{type: uncertain, dist: {dist}, input: {mode}, {fields}}}\n"
        f"  y: {{type: output, expr: x}}\n"
    )


@pytest.mark.parametrize(("dist", "mode", "given", "field"), INVALID)
def test_invalid_literal_parameter_names_node_and_field(
    dist: str, mode: str, given: dict[str, float], field: str
) -> None:
    found = [(i.code, i.node_id, i.field) for i in issues(node_yaml(dist, mode, given))]
    assert ("param.invalid", "x", field) in found


def test_invalid_parameter_carries_value_and_rule() -> None:
    issue = issues(node_yaml("normal", "params", {"mean": 0, "sd": -2}))[0]
    assert issue.params["value"] == -2.0
    assert issue.params["rule"] == "sd > 0"


def test_unknown_distribution_and_mode() -> None:
    found = issues(
        "  a: {type: uncertain, dist: normall, mean: 1, sd: 1}\n"
        "  b: {type: uncertain, dist: normal, input: quantiles, mean: 1, sd: 1}\n"
        "  y: {type: output, expr: '1'}\n"
    )
    assert [(i.code, i.node_id) for i in found] == [
        ("dist.unknown", "a"),
        ("dist.mode_unknown", "b"),
    ]


def test_missing_and_unknown_parameters() -> None:
    found = issues(
        "  a: {type: uncertain, dist: normal, mean: 1, sdd: 1}\n  y: {type: output, expr: a}\n"
    )
    assert {(i.code, i.field) for i in found} == {("param.missing", "sd"), ("param.unknown", "sdd")}


def test_list_parameter_rules() -> None:
    found = issues(
        "  a: {type: uncertain, dist: discrete, values: 3, weights: [1]}\n"
        "  b: {type: uncertain, dist: normal, mean: [1, 2], sd: 1}\n"
        "  y: {type: output, expr: '1'}\n"
    )
    assert {(i.code, i.node_id, i.field) for i in found} == {
        ("param.invalid", "a", "values"),
        ("param.invalid", "b", "mean"),
    }


def test_invalid_discrete_lists() -> None:
    found = issues(
        "  a: {type: uncertain, dist: discrete, values: [1, 2], weights: [0, 0]}\n"
        "  y: {type: output, expr: a}\n"
    )
    assert [(i.code, i.field) for i in found] == [("param.invalid", "weights")]


def test_expression_issue_names_node_and_field() -> None:
    found = issues(
        "  a: {type: uncertain, dist: normal, mean: 'b +', sd: 1}\n"
        "  b: {type: constant, value: 1}\n"
        "  y: {type: output, expr: 'b.real'}\n"
    )
    assert [(i.code, i.node_id, i.field) for i in found] == [
        ("expr.syntax", "a", "mean"),
        ("expr.forbidden", "y", "expr"),
    ]


def test_dependents_of_failed_node_add_no_issues() -> None:
    found = issues(
        "  a: {type: derived, expr: 'nix + 1'}\n"
        "  b: {type: derived, expr: 'a > 1'}\n"
        "  y: {type: output, expr: 'where(b, 1, 0)'}\n"
    )
    assert [(i.code, i.node_id) for i in found] == [("expr.unknown_name", "a")]


def test_event_probability_literal_checked() -> None:
    found = issues("  e: {type: event, p: 1.5}\n  y: {type: output, expr: 'where(e, 1, 0)'}\n")
    assert [(i.code, i.node_id, i.field) for i in found] == [("param.invalid", "e", "p")]


def test_event_probability_expression_must_be_number() -> None:
    found = issues(
        "  r: {type: choice, options: [{label: A, weight: 1}, {label: B, weight: 1}]}\n"
        "  e: {type: event, p: r}\n  y: {type: output, expr: 'where(e, 1, 0)'}\n"
    )
    assert [(i.code, i.node_id, i.field) for i in found] == [("expr.choice_usage", "e", "p")]


def test_output_of_choice_type_rejected() -> None:
    found = issues(
        "  r: {type: choice, options: [{label: A, weight: 1}, {label: B, weight: 1}]}\n"
        "  y: {type: output, expr: r}\n"
    )
    assert [(i.code, i.node_id) for i in found] == [("expr.choice_usage", "y")]


def test_no_output_and_empty() -> None:
    assert [i.code for i in issues("  a: {type: constant, value: 1}\n")] == ["model.no_output"]
    with pytest.raises(ModelError) as exc:
        compile_model(model_from_yaml("schema_version: 1\nmodel: m\nnodes: {}\n"))
    assert [i.code for i in exc.value.issues] == ["model.empty"]


def test_collects_issues_of_several_nodes() -> None:
    found = issues(
        "  a: {type: uncertain, dist: normal, mean: 0, sd: 0}\n"
        "  b: {type: uncertain, dist: uniform, low: 2, high: 1}\n"
        "  c: {type: constant, value: 1}\n"
    )
    assert {(i.code, i.node_id) for i in found} == {
        ("param.invalid", "a"),
        ("param.invalid", "b"),
        ("model.no_output", None),
    }


def test_expression_parameter_not_checked_at_compile_time() -> None:
    compiled = compile_text(
        "  s: {type: constant, value: -1}\n"
        "  a: {type: uncertain, dist: normal, mean: 0, sd: 's'}\n  y: {type: output, expr: a}\n"
    )
    assert "a" not in compiled.canonical


def test_degenerate_uniform_is_notice() -> None:
    compiled = compile_text(
        "  a: {type: uncertain, dist: uniform, low: 3, high: 3}\n  y: {type: output, expr: a}\n"
    )
    assert [(n.code, n.node_id) for n in compiled.notices] == [("uniform.degenerate", "a")]


def test_pert_with_mode_on_boundary_is_valid() -> None:
    compile_text(
        "  a: {type: uncertain, dist: pert, low: 1, mode: 1, high: 4}\n"
        "  y: {type: output, expr: a}\n"
    )


def test_canonical_keeps_mode_and_canonical_values() -> None:
    compiled = compile_text(
        "  a: {type: uncertain, dist: lognormal, input: mean_sd, mean: 3, sd: 1.5}\n"
        "  b: {type: uncertain, dist: pert, low: 8, mode: 10, high: 15}\n"
        "  y: {type: output, expr: a + b}\n"
    )
    a = compiled.canonical["a"]
    assert a["dist"] == "lognormal"
    assert a["input"] == "mean_sd"
    assert a["given"] == {"mean": 3.0, "sd": 1.5}
    assert set(a["canonical"]) == {"mu", "sigma"}  # pyright: ignore[reportArgumentType]
    assert compiled.canonical["b"]["canonical"]["lambda"] == 4.0  # pyright: ignore[reportIndexIssue]


def test_model_hash_depends_on_content() -> None:
    base = "  a: {type: constant, value: 1}\n  y: {type: output, expr: a}\n"
    h1 = compile_text(base).model_hash
    assert h1 == compile_text(base).model_hash
    assert h1 != compile_text(base.replace("value: 1", "value: 2")).model_hash
    assert len(h1) == 64


def test_deep_expression_is_model_error() -> None:
    found = issues(
        "  x: {type: constant, value: 1}\n  y: {type: output, expr: '" + "x+" * 499 + "x'}\n"
    )
    assert [(i.code, i.node_id) for i in found] == [("expr.too_deep", "y")]


@pytest.mark.parametrize("values", ["[a, b]", "[[1], 2]", "[true, 2]"])
def test_list_items_must_be_numbers(values: str) -> None:
    found = issues(
        f"  a: {{type: uncertain, dist: discrete, values: {values}, weights: [1, 1]}}\n"
        "  y: {type: output, expr: '1'}\n"
    )
    assert [(i.code, i.node_id, i.field) for i in found] == [("param.invalid", "a", "values")]
