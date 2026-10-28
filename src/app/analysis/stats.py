"""Summary statistics of one output, each with its numerical uncertainty."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
import math
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from itertools import pairwise
from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from app.errors import InputError, Issue, Notice
from app.model.schema import Target

METHOD = "quantile: Hyndman-Fan type 7; CI: order statistics; P: Wilson"
DEFAULT_QUANTILES = (0.05, 0.1, 0.5, 0.9, 0.95)


@dataclass(frozen=True)
class Proportion:
    k: int
    n: int
    p: float
    lo: float
    hi: float


@dataclass(frozen=True)
class QuantileEstimate:
    q: float
    value: float
    lo: float
    hi: float


@dataclass(frozen=True)
class LossRisk:
    """Losses against a reference value (e.g. the initial wealth), at level 95 %."""

    reference: float
    p_loss: Proportion  # P(value < reference)
    var: QuantileEstimate  # reference − Q(5 %), interval from the quantile's interval
    es: float  # reference − mean of the values ≤ Q(5 %)
    es_se: float


@dataclass(frozen=True)
class Summary:
    """Numbers and method names only; texts for people come from the UI (M2)."""

    kind: Literal["num", "bool"]
    n: int
    conf: float
    method: str
    mean: float | None = None
    se: float = math.nan
    sd: float | None = None
    var: float | None = None
    median: float | None = None
    min: float | None = None
    max: float | None = None
    quantiles: tuple[QuantileEstimate, ...] = ()
    target: Proportion | None = None
    share: Proportion | None = None
    notices: tuple[Notice, ...] = ()
    horizon: float | None = None
    beyond: Proportion | None = None  # share of values beyond the horizon ("nicht erreicht")
    loss: LossRisk | None = None


def wilson(k: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    """Wilson score interval for k hits in n trials; the upper bound stays > 0 at k = 0."""
    z = float(stats.norm.ppf(1 - (1 - conf) / 2))
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z / denom * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    lo = 0.0 if k == 0 else max(0.0, center - half)
    hi = 1.0 if k == n else min(1.0, center + half)
    return lo, hi


def proportion(hits: NDArray[np.bool_], conf: float) -> Proportion:
    k, n = int(np.count_nonzero(hits)), int(hits.size)
    lo, hi = wilson(k, n, conf)
    return Proportion(k, n, k / n, lo, hi)


def quantile_ci(sorted_x: NDArray[np.float64], q: float, conf: float) -> tuple[float, float]:
    """Distribution-free interval from order statistics (ranks via the binomial distribution)."""
    n = sorted_x.size
    tail = (1 - conf) / 2
    lower = int(stats.binom.ppf(tail, n, q))
    upper = int(stats.binom.ppf(1 - tail, n, q)) + 1
    lower, upper = min(max(lower, 1), n), min(max(upper, 1), n)
    return float(sorted_x[lower - 1]), float(sorted_x[upper - 1])


def hits(x: NDArray[np.float64], target: Target) -> NDArray[np.bool_]:
    compare = {"le": np.less_equal, "lt": np.less, "ge": np.greater_equal, "gt": np.greater}
    return compare[target.op](x, target.value)


VAR_LEVEL = 0.95


def loss_risk(sorted_x: NDArray[np.float64], reference: float, conf: float) -> LossRisk:
    """P(loss), value at risk and expected shortfall at VAR_LEVEL."""
    q = 1 - VAR_LEVEL
    cut = float(np.quantile(sorted_x, q, method="linear"))
    lo, hi = quantile_ci(sorted_x, q, conf)
    tail = sorted_x[sorted_x <= cut]
    es_se = float(np.std(tail, ddof=1)) / math.sqrt(tail.size) if tail.size > 1 else math.nan
    return LossRisk(
        reference,
        proportion(sorted_x < reference, conf),
        QuantileEstimate(VAR_LEVEL, reference - cut, reference - hi, reference - lo),
        reference - float(np.mean(tail)),
        es_se,
    )


def multimodal(x: NDArray[Any], bins: int = 60) -> tuple[float, float] | None:
    """(median, centre of the highest peak) if the density has two or more separate peaks.

    Histogram smoothed over three bins; a peak counts if it reaches 10 % of the highest and the
    density between two peaks falls below half of the smaller one.
    """
    values = np.asarray(x, dtype=np.float64)
    if values.size < 2 or float(np.ptp(values)) == 0.0:
        return None
    counts, edges = np.histogram(values, bins=bins)
    smooth = np.convolve(counts, np.ones(3) / 3, mode="same")
    inner = smooth[1:-1]
    is_peak = (inner > smooth[:-2]) & (inner >= smooth[2:]) & (inner >= 0.1 * smooth.max())
    peaks = [int(i) + 1 for i in np.flatnonzero(is_peak)]
    separate = [
        (a, b)
        for a, b in pairwise(peaks)
        if smooth[a : b + 1].min() < 0.5 * min(smooth[a], smooth[b])
    ]
    if not separate:
        return None
    top = int(np.argmax(smooth))
    return float(np.median(values)), float((edges[top] + edges[top + 1]) / 2)


def summarize(
    x: NDArray[Any],
    *,
    quantiles: Sequence[float] = DEFAULT_QUANTILES,
    target: Target | None = None,
    conf: float = 0.95,
    horizon: float | None = None,
    loss_reference: float | None = None,
) -> Summary:
    """Mean with standard error, median, quantiles with CI, P(target) with Wilson interval."""
    for q in quantiles:
        if not 0 < q < 1:
            raise InputError(Issue("stats.quantile_range", params={"q": q}))
    if x.dtype == np.bool_:
        return Summary("bool", int(x.size), conf, METHOD, share=proportion(x, conf))
    x = np.asarray(x, dtype=np.float64)
    n = int(x.size)
    sorted_x = np.sort(x)
    notices: tuple[Notice, ...] = ()
    sd = float(np.std(x, ddof=1)) if n > 1 else math.nan
    if n == 1:
        notices = (Notice("stats.single_sample"),)
    estimates = tuple(
        QuantileEstimate(
            q, float(np.quantile(sorted_x, q, method="linear")), *quantile_ci(sorted_x, q, conf)
        )
        for q in quantiles
    )
    return Summary(
        "num",
        n,
        conf,
        METHOD,
        mean=float(np.mean(x)),
        se=sd / math.sqrt(n),
        sd=sd,
        var=sd * sd,
        median=float(np.median(x)),
        min=float(sorted_x[0]),
        max=float(sorted_x[-1]),
        quantiles=estimates,
        target=proportion(hits(x, target), conf) if target is not None else None,
        notices=notices,
        horizon=horizon,
        beyond=proportion(x > horizon, conf) if horizon is not None else None,
        loss=loss_risk(sorted_x, loss_reference, conf) if loss_reference is not None else None,
    )


def summary_to_dict(summary: Summary) -> dict[str, Any]:
    """Plain JSON-compatible form, for stored runs."""
    return asdict(summary)
