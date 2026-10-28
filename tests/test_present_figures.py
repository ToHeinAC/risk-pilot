"""Plotly figures of the result view (M2 AK 2)."""

from typing import Any

import numpy as np
import plotly.graph_objects as go

from app.present import figures
from app.present.references import Curve


class Trace:
    """Typed view of a plotly trace (plotly has no type stubs)."""

    def __init__(self, trace: Any) -> None:
        self.trace = trace

    def __getitem__(self, key: str) -> Any:
        value = getattr(self.trace, key)
        return value if key == "name" else np.asarray(value)


def traces(fig: go.Figure) -> list[Trace]:
    return [Trace(trace) for trace in getattr(fig, "data")]  # noqa: B009 - untyped plotly


def test_histogram_bins_bounded_and_density() -> None:
    x = np.random.default_rng(1).normal(size=50_000)
    fig = figures.histogram(x, "d", [Curve("Analytisch", np.linspace(-3, 3, 50), np.ones(50))])
    bars = traces(fig)[0]
    centers, heights = np.asarray(bars["x"]), np.asarray(bars["y"])
    assert len(centers) <= 200
    assert abs(float(np.sum(heights) * np.diff(centers)[0]) - 1) < 0.01
    assert [trace["name"] for trace in traces(fig)[1:]] == ["Analytisch"]


def test_histogram_of_constant() -> None:
    assert len(traces(figures.histogram(np.full(100, 3.0), None, []))[0]["x"]) == 1


def test_cdf_thinned() -> None:
    x = np.random.default_rng(2).random(100_000)
    line = traces(figures.cdf(x, "d", []))[0]
    y = np.asarray(line["y"])
    assert len(line["x"]) <= 2001
    assert y[0] > 0
    assert y[-1] == 1.0


def test_cdf_not_thinned_up_to_20000() -> None:
    x = np.random.default_rng(3).random(15_000)
    assert len(traces(figures.cdf(x, None, []))[0]["x"]) == 15_000


def test_german_number_separators() -> None:
    layout: Any = getattr(figures.cdf(np.arange(5.0), None, []), "layout")  # noqa: B009 - untyped plotly
    assert layout.separators == ",\u202f"


def test_share_bar_for_bool() -> None:
    bar = traces(figures.share_bar(np.array([True, False, True, True])))[0]
    assert list(bar["y"]) == [0.75, 0.25]


def test_compare_cdfs() -> None:
    fig = figures.compare_cdfs({"vorher": np.arange(10.0), "nachher": np.arange(10.0) + 1}, "d")
    assert [trace["name"] for trace in traces(fig)] == ["vorher", "nachher"]
