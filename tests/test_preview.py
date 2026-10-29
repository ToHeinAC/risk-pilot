"""Distribution preview on the node card (M6 AK 1)."""

import re

import numpy as np
import pytest

from app.model.compile import compile_model
from app.model.yaml_io import model_from_yaml
from app.present import preview

MODEL = (
    "schema_version: 1\nmodel: m\nsettings: {seed: 3}\nnodes:\n"
    "  k: {type: constant, value: 10}\n"
    "  x: {type: uncertain, dist: normal, mean: 'k', sd: 2, bounds: {min: 8, max: 13}}\n"
    "  u: {type: uncertain, dist: uniform, low: 0, high: 1}\n"
    "  y: {type: output, expr: 'x + u'}\n"
)


def test_figures_from_the_node_draws() -> None:
    c = compile_model(model_from_yaml(MODEL))
    p = preview.node_preview(c, "x", n=20_000)
    assert p.mean == pytest.approx(10, abs=0.1)  # mean is an expression of another node
    assert p.median == pytest.approx(float(np.median(p.samples)))
    assert p.p5 == pytest.approx(10 - 1.645 * 2, abs=0.1)
    assert p.p95 == pytest.approx(10 + 1.645 * 2, abs=0.1)
    assert p.below == pytest.approx(0.1587, abs=0.01)  # P(X < 8) = Φ(−1)
    assert p.above == pytest.approx(0.0668, abs=0.01)  # P(X > 13) = Φ(−1.5)
    rows = dict(preview.preview_rows(p, "d"))
    assert re.fullmatch(
        r"\d+,\d+ % / \d+,\d+ %", rows["Unzulässig (unter Untergrenze / über Obergrenze)"]
    )


def test_without_bounds_says_so() -> None:
    c = compile_model(model_from_yaml(MODEL))
    p = preview.node_preview(c, "u", n=2000)
    assert p.below is None
    assert p.above is None
    rows = dict(preview.preview_rows(p, None))
    assert rows["Unzulässig (unter Untergrenze / über Obergrenze)"] == "keine Grenzen gesetzt"


def test_figures_are_density_and_cdf() -> None:
    c = compile_model(model_from_yaml(MODEL))
    density, cdf = preview.preview_figures(preview.node_preview(c, "u", n=2000), None)
    assert getattr(density, "data")[0].type == "bar"  # noqa: B009 - untyped plotly
    assert getattr(cdf, "data")[0].type == "scatter"  # noqa: B009 - untyped plotly


def test_runtime_problem_is_reported() -> None:
    text = MODEL.replace("expr: 'x + u'", "expr: 'log(u - 2)'")
    c = compile_model(model_from_yaml(text))
    with pytest.raises(preview.PreviewError) as exc:
        preview.node_preview(c, "x", n=500)
    assert exc.value.issue.node_id == "y"
