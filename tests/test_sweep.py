"""Sweep: a metric over k values of one literal parameter, same seed (M4 AK 4)."""

from itertools import pairwise
from pathlib import Path

from app.analysis.sweep import plan_sweep, run_sweep, sweep_params, sweep_values
from app.model.scenarios import effective_model
from app.model.schema import Model
from app.model.yaml_io import model_from_yaml

T2 = Path(__file__).resolve().parent.parent / "examples" / "t2_terminplan.yaml"


def t2() -> Model:
    return effective_model(model_from_yaml(T2.read_text("utf-8")), "basis")


def test_t2_target_share_not_increasing_in_mean_of_b() -> None:
    plan = plan_sweep(t2(), "b", "mean", sweep_values(10, 20, 9))
    assert plan.invalid == ()
    result = run_sweep(plan, "ende", n=20_000, seed=1, quantile=0.8)
    shares = [point.summary.target.p for point in result.points if point.summary.target]
    assert len(shares) == 9
    assert all(later <= earlier for earlier, later in pairwise(shares))
    assert shares[0] > shares[-1]
    assert result.points[0].value == 10.0
    assert result.points[0].summary.quantiles[-1].q == 0.8


def test_invalid_values_reported_before_running() -> None:
    plan = plan_sweep(t2(), "b", "sd", sweep_values(-1, 3, 5))
    assert [value for value, _ in plan.invalid] == [-1.0, 0.0]
    assert all(issue.field == "sd" for _, issue in plan.invalid)


def test_sweep_params_lists_literal_numbers() -> None:
    params = sweep_params(t2())
    assert ("b", "mean", 15.0) in params
    assert ("nacharbeit", "p", 0.0) in params
    assert all(node not in ("pfad1", "ende") for node, _, _ in params)
