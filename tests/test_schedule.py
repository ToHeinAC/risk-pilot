"""Schedule (Gantt) read from the expressions: sum = in series, max/min = in parallel (pure)."""

from pathlib import Path

import numpy as np
import pytest

from app.analysis.schedule import bars, schedule
from app.model.compile import CompiledModel, compile_model
from app.model.yaml_io import model_from_yaml
from app.present import gantt

T2 = Path(__file__).resolve().parent.parent / "examples" / "t2_terminplan.yaml"


def t2() -> CompiledModel:
    return compile_model(model_from_yaml(T2.read_text("utf-8")))


def _samples() -> dict[str, np.ndarray]:
    return {
        "a": np.array([10.0, 12.0]),
        "b": np.array([15.0, 15.0]),
        "c": np.array([24.0, 30.0]),
        "nacharbeit": np.array([False, True]),
        "pfad1": np.array([25.0, 32.0]),
        "ende": np.array([25.0, 32.0]),
    }


def test_a_sum_runs_in_series_and_max_waits_for_all() -> None:
    steps = {s.node: s for s in schedule(t2(), _samples(), "ende")}
    assert steps["a"].kind == "activity"
    np.testing.assert_allclose(steps["a"].start, [0, 0])
    np.testing.assert_allclose(steps["b"].start, [10, 12])
    assert steps["b"].after == ("a",)
    block = steps["pfad1:where(nacharbeit, 5, 0)"]
    assert block.kind == "block"
    assert block.after == ("b",)
    np.testing.assert_allclose(block.finish, [25, 32])
    assert steps["pfad1"].kind == "milestone"
    np.testing.assert_allclose(steps["c"].start, [0, 0])
    assert steps["ende"].kind == "milestone"
    assert set(steps["ende"].after) == {"pfad1", "c"}
    np.testing.assert_allclose(steps["ende"].finish, [25, 32])


def test_a_free_expression_node_is_one_bar_and_min_waits_for_the_first() -> None:
    model = compile_model(
        model_from_yaml(
            "schema_version: 1\nmodel: m\nnodes:\n"
            "  a: {type: constant, value: 4}\n  b: {type: constant, value: 6}\n"
            "  z: {type: derived, expr: 'where(a > 3, 2, 0)'}\n"
            "  y: {type: output, expr: 'min(a, b) + z'}\n"
        )
    )
    values = {"a": np.array([4.0]), "b": np.array([6.0]), "z": np.array([2.0])}
    steps = {s.node: s for s in schedule(model, {**values, "y": np.array([6.0])}, "y")}
    assert steps["z"].kind == "activity"
    assert set(steps["z"].after) == {"a", "b"}
    np.testing.assert_allclose(steps["z"].start, [4])
    np.testing.assert_allclose(steps["y"].finish, [6])


def test_bars_carry_medians_and_the_finish_spread_in_start_order() -> None:
    rows = bars(schedule(t2(), _samples(), "ende"), {"a": "Vorgang A", "ende": "Projektende"})
    assert [r.node for r in rows][:2] in (["a", "c"], ["c", "a"])
    end = next(r for r in rows if r.node == "ende")
    assert end.label == "Projektende"
    assert end.finish == pytest.approx(28.5)
    assert end.lo <= end.finish <= end.hi
    assert rows[-1].node == "ende"


def test_the_figure_draws_bars_milestones_and_one_arrow_per_precondition() -> None:
    rows = bars(schedule(t2(), _samples(), "ende"), {})
    fig = gantt.figure(rows, "d")
    links = sum(len(r.after) for r in rows)
    assert len(fig.layout.annotations) == links
    names = {str(trace["name"]) for trace in fig.to_plotly_json()["data"]}
    assert {"Vorgang", "Meilenstein"} <= names


def test_sum_runs_in_series_and_a_fixed_lag_draws_no_bar() -> None:
    model = compile_model(
        model_from_yaml(
            "schema_version: 1\nmodel: m\nnodes:\n"
            "  a: {type: constant, value: 4}\n  b: {type: constant, value: 6}\n"
            "  y: {type: output, expr: 'sum(a, b) + 2'}\n"
        )
    )
    values = {"a": np.array([4.0]), "b": np.array([6.0]), "y": np.array([12.0])}
    steps = {s.node: s for s in schedule(model, values, "y")}
    assert set(steps) == {"a", "b", "y"}
    assert steps["b"].after == ("a",)
    np.testing.assert_allclose(steps["y"].finish, [12])
