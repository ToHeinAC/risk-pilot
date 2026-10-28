"""Analytic references of the lessons, evaluated for the model's current knob value.

Each function reads the parameters it needs from the lesson model by fixed node IDs (the IDs
used in ``examples/lernpfad/``) and checks the simulated output with the PRD tolerances.
"""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
import itertools
import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import special

from app.analysis.analytic import dkw_epsilon, ks_distance
from app.analysis.stats import wilson
from app.lessons.knob import current_value
from app.model.schema import Model

FloatArray = NDArray[np.float64]
Cdf = Callable[[FloatArray], FloatArray]


@dataclass(frozen=True)
class Check:
    """One criterion: ``expected`` analytic value against the simulated ``observed`` value."""

    kind: str  # "ks" | "mean" | "share" | "var"
    expected: float
    observed: float
    passed: bool
    cdf: Cdf | None = None


def _v(model: Model, node: str, field: str) -> float:
    value = current_value(model, node, field)
    if value is None:
        raise KeyError(f"{node}.{field}")
    return value


def _ks(x: NDArray[Any], cdf: Cdf) -> Check:
    distance = ks_distance(np.asarray(x, dtype=np.float64), cdf)
    eps = dkw_epsilon(x.size)
    return Check("ks", eps, distance, distance < eps, cdf)


def _mean(x: NDArray[Any], expected: float) -> Check:
    values = np.asarray(x, dtype=np.float64)
    se = float(np.std(values, ddof=1)) / math.sqrt(values.size)
    observed = float(np.mean(values))
    return Check("mean", expected, observed, abs(observed - expected) < 4 * se)


def _share(x: NDArray[Any], expected: float) -> Check:
    k = int(np.count_nonzero(x))
    lo, hi = wilson(k, x.size, conf=0.999)
    return Check("share", expected, k / x.size, lo <= expected <= hi)


def _var(x: NDArray[Any], expected: float) -> Check:
    observed = float(np.var(np.asarray(x, dtype=np.float64), ddof=1))
    return Check("var", expected, observed, abs(observed - expected) <= 0.02 * expected)


def _normal_cdf(mean: float, sd: float) -> Cdf:
    return lambda t: np.asarray(special.ndtr((t - mean) / sd), dtype=np.float64)


def sum_normal(model: Model, x: NDArray[Any]) -> list[Check]:
    """A1: a + b + c for the active segments, independent normals."""
    k = _v(model, "abschnitte", "value")
    active = [n for n, need in (("a", 1), ("b", 2), ("c", 3)) if k >= need]
    mean = sum(_v(model, n, "mean") for n in active)
    sd = math.sqrt(sum(_v(model, n, "sd") ** 2 for n in active))
    return [_ks(x, _normal_cdf(mean, sd))]


def max_iid_normal(model: Model, x: NDArray[Any]) -> list[Check]:
    """A2: maximum of k identically distributed normal paths, F(t) = Φ(t)^k."""
    k = int(_v(model, "pfade", "value"))
    base = _normal_cdf(_v(model, "p1", "mean"), _v(model, "p1", "sd"))
    return [_ks(x, lambda t: base(t) ** k)]


def min_exponential(model: Model, x: NDArray[Any]) -> list[Check]:
    """A3: minimum of independent exponentials is exponential with the summed rate."""
    k = _v(model, "alternativen", "value")
    nodes = [n for n, need in (("zug", 1), ("bus", 2), ("taxi", 3)) if k >= need]
    rate = sum(1 / _v(model, n, "mean") for n in nodes)
    return [_ks(x, lambda t: np.asarray(1 - np.exp(-rate * np.maximum(t, 0)), dtype=np.float64))]


def k_of_n_binomial(model: Model, x: NDArray[Any]) -> list[Check]:
    """A4: P(at least k of three independent events), exact over all combinations."""
    k = _v(model, "benoetigt", "value")
    ps = [_v(model, n, "p") for n in ("m1", "m2", "m3")]
    total = 0.0
    for hits in itertools.product((0, 1), repeat=3):
        if sum(hits) >= k:
            total += math.prod(p if h else 1 - p for p, h in zip(ps, hits, strict=True))
    return [_share(x, total)]


def mixture_shift(model: Model, x: NDArray[Any]) -> list[Check]:
    """A5: with probability p the duration is shifted by d: a two-component mixture."""
    mean, sd = _v(model, "dauer", "mean"), _v(model, "dauer", "sd")
    p, d = _v(model, "nacharbeit", "p"), _v(model, "zusatz", "value")
    without, shifted = _normal_cdf(mean, sd), _normal_cdf(mean + d, sd)
    return [_mean(x, mean + p * d), _ks(x, lambda t: (1 - p) * without(t) + p * shifted(t))]


def threshold_exp(model: Model, x: NDArray[Any]) -> list[Check]:
    """A6: connection reached if the delay stays within the buffer."""
    p0, m = _v(model, "puenktlich", "p"), _v(model, "verspaetung_bei_ausfall", "mean")
    b = _v(model, "puffer", "value")
    return [_share(x, p0 + (1 - p0) * (1 - math.exp(-b / m)))]


def total_expectation(model: Model, x: NDArray[Any]) -> list[Check]:
    """A7: law of total expectation and total variance for a conditional mean."""
    p, base, effect = (
        _v(model, "durchbruch", "p"),
        _v(model, "basis", "value"),
        _v(model, "effekt", "value"),
    )
    sd = _v(model, "plasma", "sd")
    return [_mean(x, base - effect * p), _var(x, sd**2 + effect**2 * p * (1 - p))]


def product_prob(model: Model, x: NDArray[Any]) -> list[Check]:
    """A8: all links of the chain must hold: product of the probabilities."""
    return [_share(x, math.prod(_v(model, n, "p") for n in ("magnete", "plasma", "material")))]


def lognormal_mean(model: Model, x: NDArray[Any]) -> list[Check]:
    """A9: E[exp(X)] = exp(μ + σ²/2) for X ~ N(μ, σ²)."""
    mu, sigma = _v(model, "verzug", "mean"), _v(model, "verzug", "sd")
    return [_mean(x, math.exp(mu + sigma**2 / 2))]


def common_cause_var(model: Model, x: NDArray[Any]) -> list[Check]:
    """A10: a shared driver enters the sum twice: Var = Var(ea) + Var(eb) + 4 g² Var(w)."""
    g = _v(model, "anteil", "value")
    var = (
        _v(model, "ea", "sd") ** 2
        + _v(model, "eb", "sd") ** 2
        + 4 * g**2 * _v(model, "wetter", "sd") ** 2
    )
    return [_var(x, var)]


REFERENCES: dict[str, Callable[[Model, NDArray[Any]], list[Check]]] = {
    "sum_normal": sum_normal,
    "max_iid_normal": max_iid_normal,
    "min_exponential": min_exponential,
    "k_of_n_binomial": k_of_n_binomial,
    "mixture_shift": mixture_shift,
    "threshold_exp": threshold_exp,
    "total_expectation": total_expectation,
    "product_prob": product_prob,
    "lognormal_mean": lognormal_mean,
    "common_cause_var": common_cause_var,
}
