"""Paired comparison of two scenarios run with the same seed (common random numbers)."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from app.analysis.stats import Proportion, proportion
from app.model.schema import Target

Direction = Literal["lower", "higher"]
Stat = Callable[[NDArray[Any]], float]


@dataclass(frozen=True)
class DiffEstimate:
    metric: str  # "mean" | "median" | "p10" | "p90" | "target" | "share"
    a: float
    b: float
    diff: float
    lo: float
    hi: float


@dataclass(frozen=True)
class Comparison:
    kind: Literal["num", "bool"]
    estimates: tuple[DiffEstimate, ...]
    direction: Direction | None
    lower: Proportion  # share of iterations with B < A
    ties: Proportion  # B = A
    higher: Proportion  # B > A
    d: NDArray[np.float64]

    def estimate(self, metric: str) -> DiffEstimate:
        return next(e for e in self.estimates if e.metric == metric)

    @property
    def better(self) -> Proportion | None:
        return {"lower": self.lower, "higher": self.higher}.get(self.direction or "")

    @property
    def worse(self) -> Proportion | None:
        return {"lower": self.higher, "higher": self.lower}.get(self.direction or "")


def direction(target: Target | None, better: Direction | None) -> Direction | None:
    """Which way is better: from the output's target, else its ``better`` field."""
    if target is not None:
        return "lower" if target.op in ("le", "lt") else "higher"
    return better


def batch_means(
    a: NDArray[Any], b: NDArray[Any], stat: Stat, metric: str, batches: int, conf: float
) -> DiffEstimate:
    """Difference of a statistic; its uncertainty from ``batches`` equal blocks of iterations."""
    sa, sb = stat(a), stat(b)
    blocks = [
        stat(y) - stat(x)
        for x, y in zip(np.array_split(a, batches), np.array_split(b, batches), strict=True)
    ]
    se = float(np.std(blocks, ddof=1)) / math.sqrt(batches)
    half = float(stats.t.ppf(1 - (1 - conf) / 2, batches - 1)) * se
    return DiffEstimate(metric, sa, sb, sb - sa, sb - sa - half, sb - sa + half)


def _paired_mean(a: NDArray[Any], b: NDArray[Any], conf: float) -> DiffEstimate:
    d = b - a
    se = float(np.std(d, ddof=1)) / math.sqrt(d.size)
    half = float(stats.norm.ppf(1 - (1 - conf) / 2)) * se
    mean = float(np.mean(d))
    return DiffEstimate(
        "mean", float(np.mean(a)), float(np.mean(b)), mean, mean - half, mean + half
    )


def _quantile(q: float) -> Stat:
    return lambda x: float(np.quantile(x, q))


def _hits(target: Target) -> Callable[[NDArray[Any]], NDArray[np.bool_]]:
    compare = {"le": np.less_equal, "lt": np.less, "ge": np.greater_equal, "gt": np.greater}
    return lambda x: compare[target.op](x, target.value)


def _share(x: NDArray[Any]) -> float:
    return float(np.mean(x))


def compare(
    a: NDArray[Any],
    b: NDArray[Any],
    *,
    target: Target | None = None,
    better: Direction | None = None,
    batches: int = 20,
    conf: float = 0.95,
) -> Comparison:
    """B against reference A, iteration by iteration (both from the same seed)."""
    if a.dtype == np.bool_:
        share = batch_means(a, b, _share, "share", batches, conf)
        d = b.astype(np.float64) - a.astype(np.float64)
        return Comparison("bool", (share,), None, *_signs(d, conf), d)
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    d = b - a
    estimates = [
        _paired_mean(a, b, conf),
        batch_means(a, b, _quantile(0.5), "median", batches, conf),
        batch_means(a, b, _quantile(0.1), "p10", batches, conf),
        batch_means(a, b, _quantile(0.9), "p90", batches, conf),
    ]
    if target is not None:
        hits = _hits(target)
        estimates.append(batch_means(hits(a), hits(b), _share, "target", batches, conf))
    return Comparison("num", tuple(estimates), direction(target, better), *_signs(d, conf), d)


def _signs(d: NDArray[np.float64], conf: float) -> tuple[Proportion, Proportion, Proportion]:
    return proportion(d < 0, conf), proportion(d == 0, conf), proportion(d > 0, conf)
