"""Distribution preview of one node on its form card (M6 AK 1, E8).

The whole model runs with a small N, so parameters that are expressions of other nodes and
correlation groups are honoured; the preview shows that node's draws.
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from app.engine.simulate import simulate
from app.errors import Issue, SimulationError
from app.messages import render, t
from app.model.compile import CompiledModel
from app.present.figures import cdf, histogram
from app.present.text import number, percent

PREVIEW_N = 20_000


class PreviewError(Exception):
    """The model cannot run, so there is nothing to preview."""

    def __init__(self, issue: Issue) -> None:
        super().__init__(render(issue))
        self.issue = issue


@dataclass(frozen=True)
class Preview:
    node: str
    samples: NDArray[np.float64]
    mean: float
    median: float
    p5: float
    p95: float
    below: float | None  # share under bounds.min, None without that bound
    above: float | None  # share over bounds.max, None without that bound


def node_preview(compiled: CompiledModel, node_id: str, n: int = PREVIEW_N) -> Preview:
    """Draws of ``node_id`` from a run of the whole model with the model's seed."""
    try:
        result = simulate(compiled, n=n, keep="all")
    except SimulationError as exc:
        raise PreviewError(exc.issue) from exc
    return preview_of(compiled, node_id, result.samples[node_id])


def preview_of(compiled: CompiledModel, node_id: str, samples: NDArray[Any]) -> Preview:
    """The preview from draws already made (the workbench's trial run, M7)."""
    x = np.asarray(samples, dtype=np.float64)
    bounds = compiled.model.nodes[node_id].bounds
    lo = bounds.min if bounds else None
    hi = bounds.max if bounds else None
    quantiles = np.quantile(x, [0.05, 0.5, 0.95])  # pyright: ignore[reportUnknownMemberType]
    p5, median, p95 = (float(v) for v in quantiles)
    return Preview(
        node=node_id,
        samples=x,
        mean=float(x.mean()),
        median=median,
        p5=p5,
        p95=p95,
        below=float(np.mean(x < lo)) if lo is not None else None,
        above=float(np.mean(x > hi)) if hi is not None else None,
    )


def _share(value: float | None) -> str:
    return "–" if value is None else percent(value)


def preview_rows(p: Preview, unit: str | None) -> list[tuple[str, str]]:
    u = f" {unit}" if unit else ""
    if p.below is None and p.above is None:
        invalid = t("preview.no_bounds")
    else:
        invalid = f"{_share(p.below)} / {_share(p.above)}"
    return [
        (t("preview.mean"), f"{number(p.mean)}{u}"),
        (t("preview.median"), f"{number(p.median)}{u}"),
        ("P5", f"{number(p.p5)}{u}"),
        ("P95", f"{number(p.p95)}{u}"),
        (t("preview.invalid"), invalid),
    ]


def preview_figures(p: Preview, unit: str | None) -> tuple[Any, Any]:
    """Density (histogram) and CDF of the node's draws."""
    return histogram(p.samples, unit, []), cdf(p.samples, unit, [])
