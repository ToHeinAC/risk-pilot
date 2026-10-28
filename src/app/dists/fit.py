"""Quantile fit: parameters of a family from P10/P50/P90 by least squares (M5 AK 4).

Deviations are measured relative to P90 − P10, so that years (2040 ± 2 %) and small numbers
are judged alike.
"""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy import optimize, special

PROBS: NDArray[np.float64] = np.array([0.1, 0.5, 0.9])
FAMILIES = ("normal", "lognormal", "gamma", "weibull")
CONFLICT = 0.02  # above this deviation the app explains the conflict
Triple = tuple[float, float, float]
_Z: NDArray[np.float64] = np.asarray(special.ndtri(PROBS), dtype=np.float64)  # pyright: ignore[reportUnknownArgumentType]


@dataclass(frozen=True)
class QuantileFit:
    family: str
    given: Triple
    fitted: Triple
    canonical: dict[str, float]
    deviation: float  # max |fitted − given| / (P90 − P10)


def _linear(x: NDArray[np.float64], t: NDArray[np.float64]) -> tuple[float, float]:
    """Least squares x ≈ a + b t."""
    b, a = np.polyfit(t, x, 1)
    return float(a), float(b)


def _normal(q: NDArray[np.float64]) -> dict[str, float]:
    mean, sd = _linear(q, _Z)
    return {"mean": mean, "sd": sd}


def _lognormal(q: NDArray[np.float64]) -> dict[str, float]:
    mu, sigma = _linear(np.log(q), _Z)
    return {"mu": mu, "sigma": sigma}


def _gamma_ppf(shape: float, scale: float) -> NDArray[np.float64]:
    return np.asarray(special.gammaincinv(shape, PROBS) * scale, dtype=np.float64)


def _weibull_ppf(shape: float, scale: float) -> NDArray[np.float64]:
    return scale * (-np.log1p(-PROBS)) ** (1 / shape)


def _refine(
    ppf: Callable[[float, float], NDArray[np.float64]], q: NDArray[np.float64], start: Triple
) -> tuple[float, float]:
    """Least squares on log-parameters, from a fixed start (deterministic)."""
    spread = float(q[2] - q[0])

    def residual(x: NDArray[np.float64]) -> NDArray[np.float64]:
        return (ppf(float(np.exp(x[0])), float(np.exp(x[1]))) - q) / spread

    found = optimize.least_squares(residual, np.log(start[:2]), xtol=1e-12, ftol=1e-12)
    x: NDArray[np.float64] = np.asarray(found.x, dtype=np.float64)  # pyright: ignore[reportUnknownArgumentType]
    return float(np.exp(x[0])), float(np.exp(x[1]))


def _gamma(q: NDArray[np.float64]) -> dict[str, float]:
    mean, sd = float(q[1]), float(q[2] - q[0]) / float(_Z[2] - _Z[0])
    shape, scale = _refine(_gamma_ppf, q, ((mean / sd) ** 2, sd**2 / mean, 0.0))
    return {"shape": shape, "scale": scale}


def _weibull(q: NDArray[np.float64]) -> dict[str, float]:
    # ln(−ln(1 − p)) = k ln x − k ln λ gives the start values.
    a, k = _linear(np.log(-np.log1p(-PROBS)), np.log(q))
    shape, scale = _refine(_weibull_ppf, q, (k, float(np.exp(-a / k)), 0.0))
    return {"shape": shape, "scale": scale, "loc": 0.0}


def _fitted(family: str, c: dict[str, float]) -> NDArray[np.float64]:
    if family == "normal":
        return c["mean"] + c["sd"] * _Z
    if family == "lognormal":
        return np.exp(c["mu"] + c["sigma"] * _Z)
    if family == "gamma":
        return _gamma_ppf(c["shape"], c["scale"])
    return _weibull_ppf(c["shape"], c["scale"])


_FITS = {"normal": _normal, "lognormal": _lognormal, "gamma": _gamma, "weibull": _weibull}


def fit_quantiles(family: str, given: Triple) -> QuantileFit:
    """Canonical parameters of ``family`` closest to the three quantiles; the caller checks them
    first (strictly increasing, positive where the family needs it)."""
    q = np.asarray(given, dtype=np.float64)
    canonical = _FITS[family](q)
    fitted = _fitted(family, canonical)
    deviation = float(np.max(np.abs(fitted - q)) / (q[2] - q[0]))
    triple = (float(fitted[0]), float(fitted[1]), float(fitted[2]))
    return QuantileFit(family, given, triple, canonical, deviation)
