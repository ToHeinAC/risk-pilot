"""Reference graph, topological order and cycles (M1 AK 6)."""

from itertools import pairwise

import pytest

from app.errors import ModelError
from app.model.compile import compile_model
from app.model.graph import Edge, collect_refs, edges, topo_order
from app.model.schema import Model
from app.model.yaml_io import model_from_yaml


def model(nodes: str) -> Model:
    return model_from_yaml(f"schema_version: 1\nmodel: m\nnodes:\n{nodes}")


def test_refs_from_expressions_and_parameters() -> None:
    m = model(
        "  a: {type: constant, value: 1}\n"
        "  b: {type: uncertain, dist: normal, mean: 'a * 2', sd: 1}\n"
        "  e: {type: event, p: 'min(a, 0.5)'}\n"
        "  y: {type: output, expr: 'max(b, 0) + where(e, 1, 0) + unknown'}\n"
    )
    refs = collect_refs(m)
    assert refs == {"a": set(), "b": {"a"}, "e": {"a"}, "y": {"b", "e"}}


def test_order_respects_dependencies() -> None:
    order, cycle = topo_order({"y": {"b", "e"}, "b": {"a"}, "e": {"a"}, "a": set()})
    assert cycle is None
    assert order.index("a") < order.index("b") < order.index("y")
    assert order.index("e") < order.index("y")


def test_order_is_deterministic() -> None:
    refs = {"c": set[str](), "b": set[str](), "a": set[str]()}
    assert topo_order(refs) == topo_order(dict(reversed(list(refs.items()))))


def test_cycle_reports_all_nodes_in_order() -> None:
    m = model(
        "  a: {type: derived, expr: 'c + 1'}\n"
        "  b: {type: derived, expr: 'a + 1'}\n"
        "  c: {type: derived, expr: 'b + 1'}\n"
        "  y: {type: output, expr: a}\n"
    )
    with pytest.raises(ModelError) as exc:
        compile_model(m)
    issue = exc.value.issues[0]
    assert issue.code == "graph.cycle"
    cycle = issue.params["cycle"]
    assert isinstance(cycle, list)
    assert set(cycle) == {"a", "b", "c"}
    assert cycle[0] == cycle[-1]
    assert len(cycle) == 4
    refs = collect_refs(m)
    steps = list(pairwise(cycle))
    forward = all(b in refs[a] for a, b in steps)
    backward = all(a in refs[b] for a, b in steps)
    assert forward or backward


def test_self_reference_is_a_cycle() -> None:
    m = model(
        "  a: {type: uncertain, dist: normal, mean: 'a', sd: 1}\n  y: {type: output, expr: a}\n"
    )
    with pytest.raises(ModelError) as exc:
        compile_model(m)
    assert exc.value.issues[0].code == "graph.cycle"
    assert exc.value.issues[0].params["cycle"] == ["a", "a"]


def test_unconnected_nodes_allowed() -> None:
    m = model(
        "  a: {type: constant, value: 1}\n  lonely: {type: constant, value: 2}\n"
        "  y: {type: output, expr: a}\n"
    )
    assert set(compile_model(m).order) == {"a", "lonely", "y"}


def test_edges_by_kind() -> None:
    m = model(
        "  a: {type: constant, value: 1}\n"
        "  b: {type: uncertain, dist: normal, mean: 'a * 2', sd: 1}\n"
        "  e: {type: event, p: 'min(a, 0.5)'}\n"
        "  d: {type: derived, expr: 'b + 1'}\n"
        "  y: {type: output, expr: 'max(d, 0) + where(e, 1, 0)'}\n"
    )
    assert edges(m) == [
        Edge("a", "b", "parameter"),
        Edge("a", "e", "parameter"),
        Edge("b", "d", "ausdruck"),
        Edge("d", "y", "ausdruck"),
        Edge("e", "y", "ausdruck"),
    ]
