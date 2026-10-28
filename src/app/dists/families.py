"""The 14 built-in families. Sampling is by inversion: ``ppf`` maps uniforms to values."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
from collections.abc import Mapping
from typing import Any, ClassVar, Literal

import numpy as np
from scipy import special, stats

from app.dists.base import FloatArray, Frozen, Params, ParamSpec, Violation, violation

P = ParamSpec
Kind = Literal["continuous", "discrete"]
_LOW_HIGH = (P("low"), P("high"))
_THREE = (P("low"), P("mode"), P("high"))
_MEAN_SD = (P("mean"), P("sd"))


def _arr(x: Any) -> FloatArray:
    return np.asarray(x, dtype=np.float64)


class _Base:
    NAME: ClassVar[str]
    KIND: ClassVar[Kind] = "continuous"
    MODES: ClassVar[Mapping[str, tuple[ParamSpec, ...]]]

    def __init__(self) -> None:
        self.name: str = self.NAME
        self.kind: Kind = self.KIND
        self.modes: Mapping[str, tuple[ParamSpec, ...]] = self.MODES

    def to_canonical(self, mode: str, p: Params) -> dict[str, FloatArray]:
        return {spec.name: p[spec.name] for spec in self.modes[mode]}


class Uniform(_Base):
    NAME = "uniform"
    MODES: ClassVar = {"params": _LOW_HIGH}

    def check(self, mode: str, p: Params) -> list[Violation]:
        return [violation("high", "low ≤ high", p["low"] > p["high"])]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(c["low"] + u * (c["high"] - c["low"]))

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.uniform(loc=c["low"], scale=c["high"] - c["low"])


def _three_point_checks(p: Params) -> list[Violation]:
    return [
        violation("mode", "low ≤ mode ≤ high", (p["mode"] < p["low"]) | (p["mode"] > p["high"])),
        violation("high", "low < high", p["low"] >= p["high"]),
    ]


class Triangular(_Base):
    NAME = "triangular"
    MODES: ClassVar = {"params": _THREE, "three_point": _THREE}

    def check(self, mode: str, p: Params) -> list[Violation]:
        return _three_point_checks(p)

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        low, mode, high = c["low"], c["mode"], c["high"]
        width = high - low
        left = low + np.sqrt(u * width * (mode - low))
        right = high - np.sqrt((1 - u) * width * (high - mode))
        return _arr(np.where(u * width < mode - low, left, right))

    def reference(self, c: Mapping[str, float]) -> Frozen:
        width = c["high"] - c["low"]
        return stats.triang((c["mode"] - c["low"]) / width, loc=c["low"], scale=width)


class Pert(_Base):
    NAME = "pert"
    MODES: ClassVar = {
        "params": (*_THREE, P("lambda", 4.0)),
        "three_point": (*_THREE, P("lambda", 4.0)),
    }

    def to_canonical(self, mode: str, p: Params) -> dict[str, FloatArray]:
        low, high, lam = p["low"], p["high"], p["lambda"]
        width = high - low
        return {
            "alpha": _arr(1 + lam * (p["mode"] - low) / width),
            "beta": _arr(1 + lam * (high - p["mode"]) / width),
            "low": low,
            "high": high,
            "lambda": lam,
        }

    def check(self, mode: str, p: Params) -> list[Violation]:
        return [*_three_point_checks(p), violation("lambda", "lambda > 0", p["lambda"] <= 0)]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(
            c["low"] + special.betaincinv(c["alpha"], c["beta"], u) * (c["high"] - c["low"])
        )

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.beta(c["alpha"], c["beta"], loc=c["low"], scale=c["high"] - c["low"])


class Normal(_Base):
    NAME = "normal"
    MODES: ClassVar = {"params": _MEAN_SD, "mean_sd": _MEAN_SD}

    def check(self, mode: str, p: Params) -> list[Violation]:
        return [violation("sd", "sd > 0", p["sd"] <= 0)]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(c["mean"] + c["sd"] * special.ndtri(u))

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.norm(c["mean"], c["sd"])


class TruncNormal(_Base):
    """``mean`` and ``sd`` belong to the untruncated normal distribution."""

    NAME = "truncnormal"
    MODES: ClassVar = {"params": (*_MEAN_SD, P("lower", -np.inf), P("upper", np.inf))}

    def check(self, mode: str, p: Params) -> list[Violation]:
        mean, sd, lower, upper = p["mean"], p["sd"], p["lower"], p["upper"]
        with np.errstate(all="ignore"):
            mass = special.ndtr((upper - mean) / sd) - special.ndtr((lower - mean) / sd)
        return [
            violation("sd", "sd > 0", sd <= 0),
            violation("upper", "lower < upper", lower >= upper),
            violation(
                "lower", "mindestens eine endliche Grenze", np.isinf(lower) & np.isinf(upper)
            ),
            violation("lower", "Masse zwischen lower und upper ≥ 1e-9", (sd > 0) & (mass < 1e-9)),
        ]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        a, b = (c["lower"] - c["mean"]) / c["sd"], (c["upper"] - c["mean"]) / c["sd"]
        return _arr(stats.truncnorm.ppf(u, a, b, loc=c["mean"], scale=c["sd"]))

    def reference(self, c: Mapping[str, float]) -> Frozen:
        a, b = (c["lower"] - c["mean"]) / c["sd"], (c["upper"] - c["mean"]) / c["sd"]
        return stats.truncnorm(a, b, loc=c["mean"], scale=c["sd"])


class LogNormal(_Base):
    NAME = "lognormal"
    MODES: ClassVar = {"params": (P("mu"), P("sigma")), "mean_sd": _MEAN_SD}

    def to_canonical(self, mode: str, p: Params) -> dict[str, FloatArray]:
        if mode == "params":
            return {"mu": p["mu"], "sigma": p["sigma"]}
        sigma2 = np.log1p(p["sd"] ** 2 / p["mean"] ** 2)
        return {"mu": _arr(np.log(p["mean"]) - sigma2 / 2), "sigma": _arr(np.sqrt(sigma2))}

    def check(self, mode: str, p: Params) -> list[Violation]:
        if mode == "params":
            return [violation("sigma", "sigma > 0", p["sigma"] <= 0)]
        return [
            violation("mean", "mean > 0", p["mean"] <= 0),
            violation("sd", "sd > 0", p["sd"] <= 0),
        ]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(np.exp(c["mu"] + c["sigma"] * special.ndtri(u)))

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.lognorm(s=c["sigma"], scale=np.exp(c["mu"]))


class Beta(_Base):
    NAME = "beta"
    MODES: ClassVar = {
        "params": (P("alpha"), P("beta"), P("low", 0.0), P("high", 1.0)),
        "mean_sd": (*_MEAN_SD, P("low", 0.0), P("high", 1.0)),
    }

    def to_canonical(self, mode: str, p: Params) -> dict[str, FloatArray]:
        low, high = p["low"], p["high"]
        if mode == "params":
            return {"alpha": p["alpha"], "beta": p["beta"], "low": low, "high": high}
        m = (p["mean"] - low) / (high - low)
        v = p["sd"] ** 2 / (high - low) ** 2
        nu = m * (1 - m) / v - 1
        return {"alpha": _arr(m * nu), "beta": _arr((1 - m) * nu), "low": low, "high": high}

    def check(self, mode: str, p: Params) -> list[Violation]:
        low, high = p["low"], p["high"]
        result = [violation("high", "low < high", low >= high)]
        if mode == "params":
            return [
                violation("alpha", "alpha > 0", p["alpha"] <= 0),
                violation("beta", "beta > 0", p["beta"] <= 0),
                *result,
            ]
        mean, sd = p["mean"], p["sd"]
        with np.errstate(all="ignore"):
            m = (mean - low) / (high - low)
            v = sd**2 / (high - low) ** 2
        return [
            violation("mean", "low < mean < high", (mean <= low) | (mean >= high)),
            violation(
                "sd", "sd > 0 und sd² < (mean - low)(high - mean)", (sd <= 0) | (v >= m * (1 - m))
            ),
            *result,
        ]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(
            c["low"] + special.betaincinv(c["alpha"], c["beta"], u) * (c["high"] - c["low"])
        )

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.beta(c["alpha"], c["beta"], loc=c["low"], scale=c["high"] - c["low"])


class StudentT(_Base):
    NAME = "student_t"
    MODES: ClassVar = {"params": (P("df"), P("loc"), P("scale"))}

    def check(self, mode: str, p: Params) -> list[Violation]:
        return [
            violation("df", "df > 2", p["df"] <= 2),
            violation("scale", "scale > 0", p["scale"] <= 0),
        ]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(c["loc"] + c["scale"] * special.stdtrit(c["df"], u))

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.t(c["df"], c["loc"], c["scale"])


class Exponential(_Base):
    NAME = "exponential"
    MODES: ClassVar = {"params": (P("rate"),), "mean": (P("mean"),)}

    def to_canonical(self, mode: str, p: Params) -> dict[str, FloatArray]:
        return {"rate": p["rate"] if mode == "params" else _arr(1 / p["mean"])}

    def check(self, mode: str, p: Params) -> list[Violation]:
        field = "rate" if mode == "params" else "mean"
        return [violation(field, f"{field} > 0", p[field] <= 0)]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(-np.log1p(-u) / c["rate"])

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.expon(scale=1 / c["rate"])


class Gamma(_Base):
    NAME = "gamma"
    MODES: ClassVar = {"params": (P("shape"), P("scale")), "mean_sd": _MEAN_SD}

    def to_canonical(self, mode: str, p: Params) -> dict[str, FloatArray]:
        if mode == "params":
            return {"shape": p["shape"], "scale": p["scale"]}
        mean, sd = p["mean"], p["sd"]
        return {"shape": _arr(mean**2 / sd**2), "scale": _arr(sd**2 / mean)}

    def check(self, mode: str, p: Params) -> list[Violation]:
        fields = ("shape", "scale") if mode == "params" else ("mean", "sd")
        return [violation(f, f"{f} > 0", p[f] <= 0) for f in fields]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(special.gammaincinv(c["shape"], u) * c["scale"])

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.gamma(c["shape"], scale=c["scale"])


class Weibull(_Base):
    NAME = "weibull"
    MODES: ClassVar = {"params": (P("shape"), P("scale"), P("loc", 0.0))}

    def check(self, mode: str, p: Params) -> list[Violation]:
        return [violation(f, f"{f} > 0", p[f] <= 0) for f in ("shape", "scale")]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(c["loc"] + c["scale"] * (-np.log1p(-u)) ** (1 / c["shape"]))

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.weibull_min(c["shape"], c["loc"], c["scale"])


class Bernoulli(_Base):
    NAME = "bernoulli"
    KIND: ClassVar[Kind] = "discrete"
    MODES: ClassVar = {"params": (P("p"),)}

    def check(self, mode: str, p: Params) -> list[Violation]:
        return [violation("p", "0 ≤ p ≤ 1", (p["p"] < 0) | (p["p"] > 1))]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(u > 1 - c["p"])

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.bernoulli(c["p"])


class Discrete(_Base):
    """Values with relative weights, in YAML order; parameters are literal lists."""

    NAME = "discrete"
    KIND: ClassVar[Kind] = "discrete"
    MODES: ClassVar = {"params": (P("values", is_list=True), P("weights", is_list=True))}

    def to_canonical(self, mode: str, p: Params) -> dict[str, FloatArray]:
        weights = p["weights"]
        cum = np.cumsum(weights) / np.sum(weights)
        cum[-1] = 1.0
        return {"values": p["values"], "cum": _arr(cum)}

    def check(self, mode: str, p: Params) -> list[Violation]:
        values, weights = p["values"], p["weights"]
        same = values.size == weights.size
        return [
            violation("values", "mindestens ein Wert", values.size == 0),
            violation("values", "Werte eindeutig", np.unique(values).size != values.size),
            violation("weights", "gleich viele Gewichte wie Werte", not same),
            violation("weights", "Gewichte ≥ 0", bool(np.any(weights < 0))),
            violation("weights", "Summe der Gewichte > 0", same and float(np.sum(weights)) <= 0),
        ]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(c["values"][np.searchsorted(c["cum"], u, side="right")])

    def reference(self, c: Mapping[str, float]) -> Frozen:  # pragma: no cover - list params
        raise NotImplementedError("discrete has list parameters; tests use frequencies")


class Poisson(_Base):
    NAME = "poisson"
    KIND: ClassVar[Kind] = "discrete"
    MODES: ClassVar = {"params": (P("rate"),)}

    def check(self, mode: str, p: Params) -> list[Violation]:
        return [violation("rate", "rate ≥ 0", p["rate"] < 0)]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return _arr(stats.poisson.ppf(u, c["rate"]))

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.poisson(c["rate"])


BUILTIN = (
    Uniform(),
    Triangular(),
    Pert(),
    Normal(),
    TruncNormal(),
    LogNormal(),
    Beta(),
    StudentT(),
    Exponential(),
    Gamma(),
    Weibull(),
    Bernoulli(),
    Discrete(),
    Poisson(),
)
