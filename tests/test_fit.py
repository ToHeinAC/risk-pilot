"""Quantile fit: P10/P50/P90 -> parameters, maximal deviation shown (M5 AK 4)."""

import numpy as np
import pytest
from scipy import stats

from app.dists.fit import fit_quantiles
from app.engine.simulate import simulate
from app.errors import ModelError
from app.model.compile import compile_model
from app.model.yaml_io import model_from_yaml

EXACT = [
    ("normal", stats.norm(10, 2)),
    ("lognormal", stats.lognorm(s=0.4, scale=np.exp(1.0))),
    ("gamma", stats.gamma(2.5, scale=3)),
    ("weibull", stats.weibull_min(1.7, 0, 3)),
]


@pytest.mark.parametrize(("dist", "frozen"), EXACT)
def test_exact_quantiles_are_hit(dist: str, frozen: stats.rv_continuous) -> None:
    given = tuple(float(v) for v in frozen.ppf([0.1, 0.5, 0.9]))
    fit = fit_quantiles(dist, (given[0], given[1], given[2]))
    assert fit.deviation < 0.001
    assert np.allclose(fit.fitted, given, rtol=1e-3)


def test_conflicting_quantiles_exceed_two_percent() -> None:
    fit = fit_quantiles("normal", (2031, 2038, 2060))  # strongly right-skewed: no normal fits
    assert fit.deviation > 0.02
    years = fit_quantiles("normal", (2030, 2040, 2050))
    assert years.deviation < 1e-9  # relative to P90 - P10, not to the year


def model(dist: str, p10: float, p50: float, p90: float) -> str:
    return (
        "schema_version: 1\nmodel: m\nnodes:\n"
        f"  x: {{type: uncertain, dist: {dist}, input: quantiles, p10: {p10}, p50: {p50}, "
        f"p90: {p90}}}\n"
        "  y: {type: output, expr: x}\n"
    )


def test_model_with_quantile_input_simulates_and_reports_fit() -> None:
    c = compile_model(model_from_yaml(model("lognormal", 2, 4, 8)))
    codes = [n.code for n in c.notices]
    assert "fit.deviation" in codes
    x = simulate(c, n=50_000, seed=0).samples["y"]
    assert float(np.median(x)) == pytest.approx(4.0, rel=0.1)
    conflict = compile_model(model_from_yaml(model("normal", 2031, 2038, 2060)))
    assert "fit.conflict" in [n.code for n in conflict.notices]


@pytest.mark.parametrize(
    ("dist", "values", "field"),
    [
        ("normal", (3, 2, 4), "p50"),
        ("normal", (1, 2, 2), "p90"),
        ("gamma", (-1, 2, 3), "p10"),
        ("weibull", (0, 2, 3), "p10"),
    ],
)
def test_invalid_quantiles_rejected(
    dist: str, values: tuple[float, float, float], field: str
) -> None:
    with pytest.raises(ModelError) as exc:
        compile_model(model_from_yaml(model(dist, *values)))
    assert field in [i.field for i in exc.value.issues]


def test_expression_not_allowed_in_quantile_mode() -> None:
    text = (
        model("normal", 1, 2, 3)
        .replace("p10: 1", "p10: 'k'")
        .replace("nodes:\n", "nodes:\n  k: {type: constant, value: 1}\n")
    )
    with pytest.raises(ModelError) as exc:
        compile_model(model_from_yaml(text))
    assert [(i.code, i.field) for i in exc.value.issues] == [("param.invalid", "p10")]


def test_conflict_for_skewed_families_too() -> None:
    assert fit_quantiles("lognormal", (2, 4, 30)).deviation > 0.02
    assert fit_quantiles("gamma", (1, 9, 10)).deviation > 0.02
    assert fit_quantiles("weibull", (1, 9, 10)).deviation > 0.02
