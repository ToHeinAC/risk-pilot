"""Tutorials T1–T5 against their analytic solutions (M1 AK 11, 12; M5 AK 6–8)."""

import math
from pathlib import Path

import numpy as np
import pytest

from app.adapters.files import load_model
from app.analysis.analytic import (
    clark_mean,
    dkw_epsilon,
    grid_convolve,
    ks_distance,
    max_of_normals_cdf,
    p_greater_normal,
    portfolio_moments,
    sum_uniform01_cdf,
    sum_uniform01_pdf,
    t3_connection,
)
from app.analysis.criticality import criticality
from app.analysis.riskmatrix import risk_matrix
from app.analysis.stats import multimodal, summarize, wilson
from app.analysis.tornado import tornado
from app.engine.simulate import simulate
from app.model.compile import compile_model
from app.model.scenarios import effective_model

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def within_4se(x: np.ndarray, expected: float) -> bool:
    s = summarize(x, quantiles=())
    assert s.mean is not None
    return abs(s.mean - expected) < 4 * s.se


def test_t1_sum_of_uniforms() -> None:
    result = simulate(compile_model(load_model(EXAMPLES / "t1_faltung.yaml")))
    s = result.samples["s"]
    assert s.size == 100_000
    assert ks_distance(s, sum_uniform01_cdf) < dkw_epsilon(s.size)
    assert within_4se(s, 1.0)
    assert float(np.var(s, ddof=1)) == pytest.approx(1 / 6, rel=0.02)


def test_t1_grid_convolution() -> None:
    def uniform_pdf(x: np.ndarray) -> np.ndarray:
        return np.where((x >= 0) & (x <= 1), 1.0, 0.0)

    grid, pdf, cdf = grid_convolve(uniform_pdf, uniform_pdf, 0, 1, 0, 1, 1e-3)
    assert grid[0] == 0.0
    assert grid[-1] == pytest.approx(2.0)
    assert float(np.max(np.abs(cdf - sum_uniform01_cdf(grid)))) <= 0.001
    assert float(np.max(np.abs(pdf - sum_uniform01_pdf(grid)))) <= 0.01


def test_t1_analytic_shape() -> None:
    np.testing.assert_allclose(
        sum_uniform01_pdf(np.array([-1, 0.5, 1, 1.5, 3])), [0, 0.5, 1, 0.5, 0]
    )
    np.testing.assert_allclose(sum_uniform01_cdf(np.array([-1, 1, 2, 3])), [0, 0.5, 1, 1])


def test_t2_schedule_merge() -> None:
    result = simulate(compile_model(load_model(EXAMPLES / "t2_terminplan.yaml")))
    ende = result.samples["ende"]
    s13 = math.sqrt(13)

    def cdf(t: np.ndarray) -> np.ndarray:
        return max_of_normals_cdf(t, 25, s13, 24, 4)

    assert ks_distance(ende, cdf) < dkw_epsilon(ende.size)
    assert within_4se(ende, clark_mean(25, s13, 24, 4))
    assert "pfad1" in result.samples


def test_t2_reference_values() -> None:
    assert clark_mean(25, math.sqrt(13), 24, 4) == pytest.approx(26.6853, abs=1e-4)
    assert p_greater_normal(25, math.sqrt(13), 24, 4) == pytest.approx(0.57366, abs=1e-5)


def test_load_model_reads_utf8(tmp_path: Path) -> None:
    path = tmp_path / "m.yaml"
    path.write_text(
        "schema_version: 1\nmodel: m\nnodes:\n  y: {type: output, expr: '1', unit: 'Mio. €'}\n",
        encoding="utf-8",
    )
    assert load_model(path).nodes["y"].unit == "Mio. €"


def test_t3_connection_share_and_multimodal_arrival() -> None:
    c = compile_model(load_model(EXAMPLES / "t3_bahn.yaml"))
    result = simulate(c)
    hit = result.samples["anschluss"]
    expected = t3_connection(0.6, 6.0, 5.0)
    assert expected == pytest.approx(0.8262, abs=1e-4)
    lo, hi = wilson(int(hit.sum()), hit.size, 0.999)
    assert lo <= expected <= hi
    assert multimodal(result.samples["ankunft"]) is not None
    assert c.model.illustrative


def test_t4_portfolio_mean_and_sd() -> None:
    c = compile_model(load_model(EXAMPLES / "t4_portfolio.yaml"))
    w = simulate(c).samples["vermoegen"]
    spearman = np.array([[1, 0.2, 0.1], [0.2, 1, 0.3], [0.1, 0.3, 1]])
    mean, sd = portfolio_moments(
        100_000, [0.6, 0.3, 0.1], [0.06, 0.02, 0.03], [0.18, 0.05, 0.15], 10, spearman
    )
    assert within_4se(w, mean)
    assert float(np.std(w, ddof=1)) == pytest.approx(sd, rel=0.03)
    s = summarize(w, loss_reference=100_000)
    assert s.loss is not None
    assert 0 < s.loss.p_loss.p < 0.5
    assert len(c.model.scenarios) >= 3


def test_t5_runs_with_scenarios_and_analyses() -> None:
    model = load_model(EXAMPLES / "t5_fusion.yaml")
    assert len(model.scenarios) >= 2
    for sid in ["basis", *model.scenarios]:
        c = compile_model(effective_model(model, sid))
        samples = simulate(c, n=5000, seed=1, keep="all").samples
        s = summarize(samples["kommerziell"], horizon=2100)
        assert s.beyond is not None
        assert 0 < s.beyond.p < 1, sid
        assert criticality(c, samples, "kommerziell").indices
        assert risk_matrix(c, samples, "kommerziell")
    bars = tornado(compile_model(effective_model(model, "basis")), "kommerziell", n=2000).bars
    assert any(bar.swing != 0 for bar in bars)


@pytest.mark.parametrize(
    ("stem", "scenario"),
    [("t1_faltung", "basis"), ("t2_terminplan", "basis"), ("t2_terminplan", "nacharbeit")],
)
def test_no_multimodal_hint_for_single_peaked_tutorials(stem: str, scenario: str) -> None:
    model = effective_model(load_model(EXAMPLES / f"{stem}.yaml"), scenario)
    c = compile_model(model)
    output = next(i for i, n in c.nodes.items() if n.type == "output")
    assert multimodal(simulate(c, n=50_000).samples[output]) is None
