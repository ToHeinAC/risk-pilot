"""Contract of a distribution family."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal, Protocol

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]
Params = Mapping[str, FloatArray]


class Frozen(Protocol):
    """The part of a frozen SciPy distribution the tests use."""

    def cdf(self, x: Any) -> Any: ...

    def mean(self) -> Any: ...

    def std(self) -> Any: ...


@dataclass(frozen=True)
class ParamSpec:
    """An input field; ``default`` None means required, ``is_list`` a literal number list."""

    name: str
    default: float | None = None
    is_list: bool = False


@dataclass(frozen=True)
class Violation:
    """Iterations where ``rule`` fails for input field ``field`` (mask True = violated).

    Rules are written as positive comparisons so NaN (an unknown parameter) never counts.
    """

    field: str
    rule: str
    mask: NDArray[np.bool_]


class Family(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def kind(self) -> Literal["continuous", "discrete"]: ...

    @property
    def modes(self) -> Mapping[str, tuple[ParamSpec, ...]]: ...

    def to_canonical(self, mode: str, p: Params) -> dict[str, FloatArray]: ...

    def check(self, mode: str, p: Params) -> list[Violation]: ...

    def ppf(self, u: FloatArray, c: Params) -> FloatArray: ...

    def reference(self, c: Mapping[str, float]) -> Frozen: ...


def fill_defaults(family: Family, mode: str, given: Params) -> dict[str, FloatArray]:
    """Add the defaults of optional fields that ``given`` leaves out."""
    filled = dict(given)
    for spec in family.modes[mode]:
        if spec.name not in filled and spec.default is not None:
            filled[spec.name] = np.asarray(spec.default)
    return filled


def violation(field: str, rule: str, mask: object) -> Violation:
    return Violation(field, rule, np.asarray(mask, dtype=np.bool_))
