"""Tornado: inputs fixed at P10 and P90 with common random numbers (M4 AK 3)."""

from pathlib import Path

import numpy as np
import pytest

from app.analysis.tornado import p10_p90, tornado
from app.model.compile import CompiledModel, CUncertain, compile_model
from app.model.yaml_io import model_from_yaml

T1 = Path(__file__).resolve().parent.parent / "examples" / "t1_faltung.yaml"


def compiled(nodes: str) -> CompiledModel:
    return compile_model(model_from_yaml(f"schema_version: 1\nmodel: m\nnodes:\n{nodes}"))


def test_t1_swings_of_x1_and_x2_equal() -> None:
    c = compile_model(model_from_yaml(T1.read_text("utf-8")))
    result = tornado(c, "s", n=20_000, seed=1)
    swings = {bar.node: bar.swing for bar in result.bars}
    assert swings["x1"] == pytest.approx(swings["x2"], rel=0.02)
    assert swings["x1"] == pytest.approx(0.8, rel=0.02)
    assert result.runs == 4


def test_unconnected_node_swing_exactly_zero_and_sorted() -> None:
    c = compiled(
        "  a: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  b: {type: uncertain, dist: normal, mean: 0, sd: 5}\n"
        "  lonely: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  y: {type: output, expr: 'max(a, b) + a', target: {le: 1}}\n"
    )
    result = tornado(c, "y", n=5000, seed=3)
    assert [bar.node for bar in result.bars] == ["b", "a", "lonely"]
    lonely = result.bars[-1]
    assert lonely.swing == 0.0
    assert not lonely.connected
    for metric in ("median", "target"):
        assert tornado(c, "y", metric=metric, n=2000, seed=3).bars[-1].swing == 0.0


def test_discrete_input_takes_real_values() -> None:
    c = compiled(
        "  k: {type: uncertain, dist: poisson, rate: 3}\n"
        "  d: {type: uncertain, dist: discrete, values: [1, 5, 9], weights: [0.3, 0.4, 0.3]}\n"
        "  y: {type: output, expr: 'k + d'}\n"
    )
    bars = {bar.node: bar for bar in tornado(c, "y", n=5000, seed=0).bars}
    assert (bars["d"].low_value, bars["d"].high_value) == (1.0, 9.0)
    assert float(bars["k"].low_value).is_integer()
    assert float(bars["k"].high_value).is_integer()


def test_target_metric_needs_a_target() -> None:
    c = compiled(
        "  a: {type: uncertain, dist: normal, mean: 0, sd: 1}\n  y: {type: output, expr: a}\n"
    )
    with pytest.raises(ValueError, match="target"):
        tornado(c, "y", metric="target", n=100, seed=0)


def test_discrete_quantiles_stay_on_the_support() -> None:
    c = compiled(
        "  d: {type: uncertain, dist: discrete, values: [0, 10], weights: [0.1, 0.9]}\n"
        "  y: {type: output, expr: d}\n"
    )
    body = c.nodes["d"].body
    assert isinstance(body, CUncertain)
    x = np.array([0.0] + [10.0] * 9)
    assert p10_p90(body, x) == (0.0, 10.0)  # linear interpolation would give 9.0
