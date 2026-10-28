"""Expression tree nodes with vectorised evaluation over all iterations."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from functools import reduce
from typing import Any, Protocol

import numpy as np
from numpy.typing import NDArray

Array = NDArray[Any]
Values = Mapping[str, Array]


class EvalError(Exception):
    """Runtime problem in a share of the iterations; the engine adds the node ID."""

    def __init__(self, code: str, share: float) -> None:
        super().__init__(code)
        self.code = code
        self.share = share


class Expr(Protocol):
    def evaluate(self, values: Values) -> Array: ...


def as_num(a: Array) -> NDArray[np.float64]:
    """Booleans take part in arithmetic as 0/1."""
    return a.astype(np.float64) if a.dtype == np.bool_ else a


_ARITH: dict[str, Callable[[Array, Array], Array]] = {
    "Add": np.add,
    "Sub": np.subtract,
    "Mult": np.multiply,
    "Div": np.divide,
    "Pow": np.power,
    "Mod": np.mod,
}
_COMPARE: dict[str, Callable[[Array, Array], Array]] = {
    "Lt": np.less,
    "LtE": np.less_equal,
    "Gt": np.greater,
    "GtE": np.greater_equal,
    "Eq": np.equal,
    "NotEq": np.not_equal,
}


@dataclass(frozen=True)
class Const:
    value: float | bool

    def evaluate(self, values: Values) -> Array:
        return np.asarray(self.value)


@dataclass(frozen=True)
class Var:
    name: str

    def evaluate(self, values: Values) -> Array:
        return values[self.name]


@dataclass(frozen=True)
class Arith:
    op: str
    left: Expr
    right: Expr

    def evaluate(self, values: Values) -> Array:
        a, b = as_num(self.left.evaluate(values)), as_num(self.right.evaluate(values))
        with np.errstate(all="ignore"):
            return _ARITH[self.op](a, b)


@dataclass(frozen=True)
class Neg:
    operand: Expr
    sign: float

    def evaluate(self, values: Values) -> Array:
        return self.sign * as_num(self.operand.evaluate(values))


@dataclass(frozen=True)
class Not:
    operand: Expr

    def evaluate(self, values: Values) -> Array:
        return np.logical_not(self.operand.evaluate(values))


@dataclass(frozen=True)
class Logic:
    op: str
    operands: tuple[Expr, ...]

    def evaluate(self, values: Values) -> Array:
        fn = np.logical_and if self.op == "And" else np.logical_or
        return reduce(fn, (o.evaluate(values) for o in self.operands))


@dataclass(frozen=True)
class Cmp:
    op: str
    left: Expr
    right: Expr

    def evaluate(self, values: Values) -> Array:
        a, b = self.left.evaluate(values), self.right.evaluate(values)
        if a.dtype != b.dtype:
            a, b = as_num(a), as_num(b)
        return _COMPARE[self.op](a, b)


@dataclass(frozen=True)
class ChoiceEq:
    name: str
    code: int
    negate: bool

    def evaluate(self, values: Values) -> Array:
        hit = values[self.name] == self.code
        return np.logical_not(hit) if self.negate else hit


@dataclass(frozen=True)
class Extremum:
    """min/max as their own class so M4 can record the winning argument."""

    kind: str
    args: tuple[Expr, ...]

    def evaluate(self, values: Values) -> Array:
        return self._reduce([as_num(a.evaluate(values)) for a in self.args])

    def winners(self, values: Values) -> list[NDArray[np.bool_]]:
        """Per argument: the iterations where it equals the result (ties: every winner)."""
        evaluated = [as_num(a.evaluate(values)) for a in self.args]
        result = self._reduce(evaluated)
        return [np.asarray(x == result) for x in evaluated]

    def _reduce(self, evaluated: list[Array]) -> Array:
        fn = np.minimum if self.kind == "min" else np.maximum
        return reduce(fn, evaluated)


@dataclass(frozen=True)
class Where:
    cond: Expr
    then: Expr
    other: Expr

    def evaluate(self, values: Values) -> Array:
        a, b = self.then.evaluate(values), self.other.evaluate(values)
        if a.dtype != b.dtype:
            a, b = as_num(a), as_num(b)
        return np.where(self.cond.evaluate(values), a, b)  # pyright: ignore[reportUnknownMemberType]


@dataclass(frozen=True)
class Interp:
    x: Expr
    xs: tuple[float, ...]
    ys: tuple[float, ...]

    def evaluate(self, values: Values) -> Array:
        return np.interp(as_num(self.x.evaluate(values)), self.xs, self.ys)


@dataclass(frozen=True)
class Call:
    impl: Callable[..., Array]
    args: tuple[Expr, ...]

    def evaluate(self, values: Values) -> Array:
        evaluated = [as_num(a.evaluate(values)) for a in self.args]
        with np.errstate(all="ignore"):
            return np.asarray(self.impl(*evaluated))


@dataclass(frozen=True)
class Table:
    """A literal number list (e.g. the values of a discrete distribution)."""

    values: tuple[float, ...]

    def evaluate(self, values: Values) -> Array:
        return np.asarray(self.values, dtype=np.float64)
