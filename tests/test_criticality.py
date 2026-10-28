"""Activity of references, decisive path and criticality index (M4 AK 2)."""

from pathlib import Path

import numpy as np
import pytest

from app.analysis.criticality import criticality
from app.analysis.stats import wilson
from app.engine.simulate import simulate
from app.expr.activity import activity, selects_path
from app.expr.parser import NUM, compile_expr
from app.model.compile import CompiledModel, compile_model
from app.model.scenarios import effective_model
from app.model.yaml_io import model_from_yaml

T2 = Path(__file__).resolve().parent.parent / "examples" / "t2_terminplan.yaml"


def compiled(nodes: str) -> CompiledModel:
    return compile_model(model_from_yaml(f"schema_version: 1\nmodel: m\nnodes:\n{nodes}"))


def t2(scenario: str = "basis") -> CompiledModel:
    return compile_model(effective_model(model_from_yaml(T2.read_text("utf-8")), scenario))


def test_t2_index_of_a_and_b_against_analytic_share() -> None:
    c = t2()
    result = simulate(c, n=100_000, seed=1, keep="all")
    crit = criticality(c, result.samples, "ende")
    for node, expected in (("a", 0.5737), ("b", 0.5737), ("c", 0.4263)):
        share = crit.index(node)
        lo, hi = wilson(share.k, share.n, 0.999)
        assert lo <= expected <= hi, node
    assert crit.selects_path
    assert crit.index("nacharbeit").k == 0  # where condition: not on the path


def test_extremum_winners_count_ties() -> None:
    expr = compile_expr("max(a, b, c)", {"a": NUM, "b": NUM, "c": NUM}).node
    values = {"a": np.array([1.0, 2.0]), "b": np.array([1.0, 0.0]), "c": np.array([0.0, 2.0])}
    active = activity(expr, values)
    assert active["a"].tolist() == [True, True]
    assert active["b"].tolist() == [True, False]
    assert active["c"].tolist() == [False, True]


def test_tie_counts_both_and_indices_do_not_sum_to_one() -> None:
    c = compiled(
        "  x: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  d1: {type: derived, expr: 'x'}\n"
        "  d2: {type: derived, expr: 'x'}\n"
        "  y: {type: output, expr: 'max(d1, d2)'}\n"
    )
    crit = criticality(c, simulate(c, n=1000, seed=0, keep="all").samples, "y")
    assert crit.index("d1").p == crit.index("d2").p == 1.0


def test_where_condition_not_on_path() -> None:
    c = compiled(
        "  e: {type: event, p: 0.3}\n"
        "  a: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  b: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  y: {type: output, expr: 'where(e, a, b)'}\n"
    )
    result = simulate(c, n=20_000, seed=0, keep="all")
    crit = criticality(c, result.samples, "y")
    assert crit.index("e").k == 0
    assert crit.selects_path  # no max/min, yet the path differs between iterations
    e = result.samples["e"]
    assert crit.index("a").p == pytest.approx(float(e.mean()))
    assert crit.index("b").p == pytest.approx(1 - float(e.mean()))


def test_parameters_lie_fully_on_path() -> None:
    c = compiled(
        "  m: {type: uncertain, dist: normal, mean: 5, sd: 1}\n"
        "  x: {type: uncertain, dist: normal, mean: 'm', sd: 1}\n"
        "  z: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  y: {type: output, expr: 'max(x, z)'}\n"
    )
    result = simulate(c, n=5000, seed=0, keep="all")
    crit = criticality(c, result.samples, "y")
    assert crit.index("m").k == crit.index("x").k


def test_constellations_sum_to_one_largest_first_rest_collected() -> None:
    nodes = "".join(
        f"  x{i}: {{type: uncertain, dist: normal, mean: 0, sd: 1}}\n" for i in range(12)
    )
    args = ", ".join(f"x{i}" for i in range(12))
    c = compiled(nodes + f"  y: {{type: output, expr: 'max({args})'}}\n")
    crit = criticality(c, simulate(c, n=6000, seed=0, keep="all").samples, "y")
    shares = [row.share.p for row in crit.constellations]
    assert sum(shares) == pytest.approx(1.0)
    assert len(crit.constellations) == 10
    assert crit.constellations[-1].rest == 3
    assert shares[:-1] == sorted(shares[:-1], reverse=True)


def test_model_without_extremum_marks_every_input_critical() -> None:
    c = compiled(
        "  a: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  b: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  lonely: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  y: {type: output, expr: 'a + 2 * b'}\n"
    )
    crit = criticality(c, simulate(c, n=500, seed=0, keep="all").samples, "y")
    assert not crit.selects_path
    assert crit.index("a").p == crit.index("b").p == 1.0
    assert "lonely" not in {node for node, _ in crit.indices}
    assert len(crit.constellations) == 1


def test_keep_all_holds_every_node() -> None:
    c = t2()
    assert set(simulate(c, n=10, seed=0).samples) == {"pfad1", "ende"}
    assert set(simulate(c, n=10, seed=0, keep="all").samples) == set(c.order)


def test_activity_through_operators_and_extremum_detection() -> None:
    env = {name: NUM for name in ("a", "b", "c", "d", "x")}
    text = "abs(a) + -b + interp(c, [0, 1], [0, 1]) + where(not (x > 0) and x < 5, d, 0)"
    expr = compile_expr(text, env).node
    values = {name: np.array([-1.0, 1.0]) for name in env}
    active = activity(expr, values)
    assert {k: v.tolist() for k, v in active.items() if k != "d"} == {
        "a": True,
        "b": True,
        "c": True,
    }
    assert active["d"].tolist() == [True, False]
    assert selects_path(expr)  # where picks a branch per iteration
    assert not selects_path(compile_expr("abs(a) + -b * interp(c, [0, 1], [0, 1])", env).node)
    assert selects_path(compile_expr("min(a, 1) + 0", env).node)
