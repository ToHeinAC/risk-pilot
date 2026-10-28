"""Registry of the functions available in expressions."""

from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce
from typing import Any

import numpy as np
from numpy.typing import NDArray

from app.expr.evaluate import EvalError

Array = NDArray[Any]


@dataclass(frozen=True)
class ExprFunction:
    """A function with numeric arguments; ``max_args`` None means unlimited."""

    name: str
    min_args: int
    max_args: int | None
    impl: Callable[..., Array]


_REGISTRY: dict[str, ExprFunction] = {}


def register_function(fn: ExprFunction) -> None:
    """Make ``fn`` available in expressions under ``fn.name``."""
    _REGISTRY[fn.name] = fn


def get_function(name: str) -> ExprFunction | None:
    return _REGISTRY.get(name)


def function_names() -> frozenset[str]:
    return frozenset(_REGISTRY)


def _clip(x: Array, lo: Array, hi: Array) -> Array:
    bad = np.asarray(lo > hi)
    if bad.any():
        raise EvalError("runtime.clip_bounds", float(np.mean(bad)))
    return np.clip(x, lo, hi)  # pyright: ignore[reportUnknownMemberType]


def _sum(*args: Array) -> Array:
    return reduce(np.add, args)


def _unsupported(*_args: Array) -> Array:  # pragma: no cover - built by the parser
    raise NotImplementedError


for _fn in (
    ExprFunction("min", 2, None, _unsupported),
    ExprFunction("max", 2, None, _unsupported),
    ExprFunction("where", 3, 3, _unsupported),
    ExprFunction("interp", 3, 3, _unsupported),
    ExprFunction("sum", 1, None, _sum),
    ExprFunction("abs", 1, 1, np.abs),
    ExprFunction("exp", 1, 1, np.exp),
    ExprFunction("log", 1, 1, np.log),
    ExprFunction("sqrt", 1, 1, np.sqrt),
    ExprFunction("floor", 1, 1, np.floor),
    ExprFunction("ceil", 1, 1, np.ceil),
    ExprFunction("clip", 3, 3, _clip),
):
    register_function(_fn)
