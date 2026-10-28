"""Risk matrix per event: p-hat with Wilson, conditional difference with Welch (M4 AK 6)."""

from pathlib import Path

from app.analysis.riskmatrix import RiskRow, risk_matrix
from app.engine.simulate import simulate
from app.model.compile import compile_model
from app.model.scenarios import effective_model
from app.model.yaml_io import model_from_yaml

T2 = Path(__file__).resolve().parent.parent / "examples" / "t2_terminplan.yaml"


def run(scenario: str) -> list[RiskRow]:
    c = compile_model(effective_model(model_from_yaml(T2.read_text("utf-8")), scenario))
    return list(risk_matrix(c, simulate(c, n=20_000, seed=4, keep="all").samples, "ende"))


def test_t2_rework_difference_in_zero_to_five() -> None:
    (row,) = run("nacharbeit")
    assert row.node == "nacharbeit"
    assert 0.18 < row.p.p < 0.22
    assert row.diff is not None
    assert 0 < row.diff.value <= 5
    assert row.diff.lo < row.diff.value < row.diff.hi


def test_never_or_always_leaves_difference_undefined() -> None:
    (never,) = run("basis")
    assert never.p.k == 0
    assert never.diff is None
    c = compile_model(
        model_from_yaml(
            "schema_version: 1\nmodel: m\nnodes:\n"
            "  e: {type: event, p: 1}\n"
            "  x: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
            "  y: {type: output, expr: 'x + e'}\n"
        )
    )
    (always,) = risk_matrix(c, simulate(c, n=100, seed=0, keep="all").samples, "y")
    assert always.p.p == 1.0
    assert always.diff is None
