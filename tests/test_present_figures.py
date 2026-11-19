"""Plotly figures of the result view (M2 AK 2)."""

from typing import Any

import numpy as np
import plotly.graph_objects as go
import pytest

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
    curve = Curve("Analytisch", np.linspace(-3, 3, 50), np.ones(50))
    fig = figures.histogram(x, "d", [curve], with_cdf=False)
    bars = traces(fig)[0]
    centers, heights = np.asarray(bars["x"]), np.asarray(bars["y"])
    assert len(centers) <= 200
    assert abs(float(np.sum(heights) * np.diff(centers)[0]) - 1) < 0.01
    assert [trace["name"] for trace in traces(fig)[1:]] == ["Analytisch"]


def test_histogram_of_constant() -> None:
    assert len(traces(figures.histogram(np.full(100, 3.0), None, []))[0]["x"]) == 1


def cdf_trace(fig: go.Figure) -> Trace:
    found = [tr for tr in traces(fig) if tr["name"] == "Kumulative Verteilung"]
    assert len(found) == 1
    return found[0]


def test_histogram_carries_the_cdf_on_a_right_axis() -> None:
    x = np.random.default_rng(4).normal(size=5_000)
    fig = figures.histogram(x, "d", [])
    line = cdf_trace(fig)
    assert line.trace.yaxis == "y2"
    layout: Any = getattr(fig, "layout")  # noqa: B009 - untyped plotly
    assert (layout.yaxis2.side, layout.yaxis2.overlaying) == ("right", "y")
    assert tuple(layout.yaxis2.range) == (0, 1)
    assert np.asarray(line["y"])[-1] == 1.0


def test_cdf_layer_marks_p5_median_p95() -> None:
    x = np.arange(1.0, 1001.0)
    fig = figures.histogram(x, None, [])
    layout: Any = getattr(fig, "layout")  # noqa: B009 - untyped plotly
    positions = [shape.x0 for shape in layout.shapes]
    assert positions == pytest.approx(list(np.quantile(x, [0.05, 0.5, 0.95])))
    labels = " ".join(a.text for a in layout.annotations)
    assert all(word in labels for word in ("P5", "Median", "P95"))


def test_reference_cdf_is_dashed_on_the_right_axis() -> None:
    curve = Curve("Analytisch", np.linspace(-3, 3, 50), np.linspace(0, 1, 50))
    fig = figures.histogram(np.random.default_rng(5).normal(size=500), None, [], [curve])
    ref = next(tr for tr in traces(fig) if tr["name"] == "Analytisch")
    assert (ref.trace.yaxis, ref.trace.line.dash) == ("y2", "dash")


def test_histogram_without_cdf() -> None:
    curve = Curve("Analytisch", np.linspace(0, 1, 5), np.linspace(0, 1, 5))
    fig = figures.histogram(np.arange(100.0), None, [], [curve], with_cdf=False)
    layout: Any = getattr(fig, "layout")  # noqa: B009 - untyped plotly
    assert [tr.trace.type for tr in traces(fig)] == ["bar"]
    assert not layout.shapes
    assert "yaxis2" not in fig.to_plotly_json()["layout"]


def test_cdf_thinned() -> None:
    x = np.random.default_rng(2).random(100_000)
    line = cdf_trace(figures.histogram(x, "d", []))
    y = np.asarray(line["y"])
    assert len(line["x"]) <= 2001
    assert y[0] > 0
    assert y[-1] == 1.0


def test_cdf_not_thinned_up_to_20000() -> None:
    x = np.random.default_rng(3).random(15_000)
    assert len(cdf_trace(figures.histogram(x, None, []))["x"]) == 15_000


def test_german_number_separators() -> None:
    fig = figures.histogram(np.arange(5.0), None, [])
    layout: Any = getattr(fig, "layout")  # noqa: B009 - untyped plotly
    assert layout.separators == ",\u202f"


def test_share_bar_for_bool() -> None:
    bar = traces(figures.share_bar(np.array([True, False, True, True])))[0]
    assert list(bar["y"]) == [0.75, 0.25]


def test_compare_cdfs() -> None:
    fig = figures.compare_cdfs({"vorher": np.arange(10.0), "nachher": np.arange(10.0) + 1}, "d")
    assert [trace["name"] for trace in traces(fig)] == ["vorher", "nachher"]
