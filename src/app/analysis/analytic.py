"""Analytic reference solutions and distance measures for the tutorials."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
import math
from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import special

FloatArray = NDArray[np.float64]


def ks_distance(x: FloatArray, cdf: Callable[[FloatArray], Any]) -> float:
    """Kolmogorov distance between the empirical CDF of ``x`` and ``cdf``."""
    s = np.sort(np.asarray(x, dtype=np.float64))
    n = s.size
    f = np.asarray(cdf(s), dtype=np.float64)
    i = np.arange(1, n + 1, dtype=np.float64)
    return float(max(np.max(i / n - f), np.max(f - (i - 1) / n)))


def dkw_epsilon(n: int, alpha: float = 0.001) -> float:
    """DKW bound: the KS distance exceeds it with probability at most ``alpha``."""
    return math.sqrt(math.log(2 / alpha) / (2 * n))


def sum_uniform01_pdf(s: FloatArray) -> FloatArray:
    """Density of U(0,1) + U(0,1): triangle on [0, 2]."""
    s = np.asarray(s, dtype=np.float64)
    return np.where((s >= 0) & (s <= 2), 1 - np.abs(s - 1), 0.0)


def sum_uniform01_cdf(s: FloatArray) -> FloatArray:
    """Distribution function of U(0,1) + U(0,1)."""
    s = np.clip(np.asarray(s, dtype=np.float64), 0.0, 2.0)
    return np.where(s <= 1, s * s / 2, 1 - (2 - s) ** 2 / 2)


def _sample(pdf: Callable[[FloatArray], Any], lo: float, hi: float, h: float) -> FloatArray:
    grid = lo + h * np.arange(round((hi - lo) / h) + 1, dtype=np.float64)
    values = np.asarray(pdf(grid), dtype=np.float64)
    values[[0, -1]] *= 0.5  # trapezoid weights at the ends
    return values


def grid_convolve(
    pdf1: Callable[[FloatArray], Any],
    pdf2: Callable[[FloatArray], Any],
    lo1: float,
    hi1: float,
    lo2: float,
    hi2: float,
    h: float,
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Density and CDF of X1 + X2 by numerical convolution on a grid with step ``h``."""
    pdf = np.convolve(_sample(pdf1, lo1, hi1, h), _sample(pdf2, lo2, hi2, h)) * h
    grid = lo1 + lo2 + h * np.arange(pdf.size, dtype=np.float64)
    cdf = np.concatenate(([0.0], np.cumsum((pdf[1:] + pdf[:-1]) / 2) * h))
    return _f64(grid), _f64(pdf), _f64(cdf)


def _f64(x: Any) -> FloatArray:
    return np.asarray(x, dtype=np.float64)


def max_of_normals_cdf(t: FloatArray, m1: float, s1: float, m2: float, s2: float) -> FloatArray:
    """CDF of max(X1, X2) for independent normal X1, X2: the product of both CDFs."""
    return np.asarray(special.ndtr((t - m1) / s1) * special.ndtr((t - m2) / s2), dtype=np.float64)


def clark_mean(m1: float, s1: float, m2: float, s2: float) -> float:
    """Clark (1961): mean of the maximum of two independent normal variables."""
    theta = math.hypot(s1, s2)
    alpha = (m1 - m2) / theta
    phi = math.exp(-alpha * alpha / 2) / math.sqrt(2 * math.pi)
    return m1 * float(special.ndtr(alpha)) + m2 * float(special.ndtr(-alpha)) + theta * phi


def p_greater_normal(m1: float, s1: float, m2: float, s2: float) -> float:
    """P(X1 > X2) for independent normal X1, X2."""
    return float(special.ndtr((m1 - m2) / math.hypot(s1, s2)))
