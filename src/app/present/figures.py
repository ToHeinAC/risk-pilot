"""Plotly figures for the result view."""

# plotly ships without type stubs; its members are untyped for pyright.
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false, reportMissingTypeStubs=false
from collections.abc import Mapping
from typing import Any

import numpy as np
import plotly.graph_objects as go
from numpy.typing import NDArray

from app.messages import t
from app.present.references import Curve

MAX_BINS = 200
CDF_POINTS = 2000
THIN_ABOVE = 20_000


def _bins(x: NDArray[np.float64]) -> int:
    """Freedman-Diaconis rule, at most MAX_BINS, at least one bin."""
    q75, q25 = np.percentile(x, [75, 25])
    width = 2 * (q75 - q25) / np.cbrt(x.size)
    span = float(x.max() - x.min())
    if width <= 0 or span <= 0:
        return 1
    return int(min(MAX_BINS, max(1, np.ceil(span / width))))


def _layout(fig: go.Figure, x_title: str, y_title: str) -> go.Figure:
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        margin={"l": 40, "r": 10, "t": 30, "b": 40},
        separators=",\u202f",  # decimal comma, narrow space between thousands
    )
    return fig


def _axis(unit: str | None) -> str:
    return t("fig.value_unit", unit=unit) if unit else t("fig.value")


def histogram(x: NDArray[Any], unit: str | None, overlays: list[Curve]) -> go.Figure:
    values = np.asarray(x, dtype=np.float64)
    density, edges = np.histogram(values, bins=_bins(values), density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    fig = go.Figure(go.Bar(x=centers, y=density, name=t("fig.simulation"), marker_line_width=0))
    fig.update_layout(bargap=0)
    for curve in overlays:
        fig.add_trace(go.Scatter(x=curve.x, y=curve.y, mode="lines", name=curve.label))
    return _layout(fig, _axis(unit), t("fig.density"))


def _ecdf(x: NDArray[Any]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    values = np.sort(np.asarray(x, dtype=np.float64))
    probs = np.arange(1, values.size + 1, dtype=np.float64) / values.size
    if values.size > THIN_ABOVE:
        index = np.unique(np.linspace(0, values.size - 1, CDF_POINTS + 1).astype(int))
        values, probs = values[index], probs[index]
    return values, probs


def cdf(x: NDArray[Any], unit: str | None, overlays: list[Curve]) -> go.Figure:
    values, probs = _ecdf(x)
    fig = go.Figure(go.Scatter(x=values, y=probs, mode="lines", name=t("fig.simulation")))
    for curve in overlays:
        fig.add_trace(
            go.Scatter(x=curve.x, y=curve.y, mode="lines", name=curve.label, line_dash="dash")
        )
    return _layout(fig, _axis(unit), t("fig.cdf"))


def compare_cdfs(
    samples: Mapping[str, NDArray[Any]], unit: str | None, overlays: list[Curve] | None = None
) -> go.Figure:
    fig = go.Figure()
    for label, x in samples.items():
        values, probs = _ecdf(x)
        fig.add_trace(go.Scatter(x=values, y=probs, mode="lines", name=label))
    for curve in overlays or []:
        fig.add_trace(
            go.Scatter(x=curve.x, y=curve.y, mode="lines", name=curve.label, line_dash="dash")
        )
    return _layout(fig, _axis(unit), t("fig.cdf"))


def share_bar(x: NDArray[np.bool_]) -> go.Figure:
    share = float(np.mean(x))
    fig = go.Figure(go.Bar(x=[t("fig.true"), t("fig.false")], y=[share, 1 - share]))
    return _layout(fig, "", t("fig.share"))
