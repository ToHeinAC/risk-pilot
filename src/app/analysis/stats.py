"""Summary statistics of one output, each with its numerical uncertainty."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
import math
from collections.abc import Sequence
from dataclasses import asdict, dataclass
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


def _hits(x: NDArray[np.float64], target: Target) -> NDArray[np.bool_]:
    compare = {"le": np.less_equal, "lt": np.less, "ge": np.greater_equal, "gt": np.greater}
    return compare[target.op](x, target.value)


def summarize(
    x: NDArray[Any],
    *,
    quantiles: Sequence[float] = DEFAULT_QUANTILES,
    target: Target | None = None,
    conf: float = 0.95,
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
        target=proportion(_hits(x, target), conf) if target is not None else None,
        notices=notices,
    )


def summary_to_dict(summary: Summary) -> dict[str, Any]:
    """Plain JSON-compatible form, for stored runs."""
    return asdict(summary)
