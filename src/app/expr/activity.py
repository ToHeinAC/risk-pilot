"""Which references decide an expression's result, iteration by iteration (M4 criticality)."""

from collections.abc import Iterator

import numpy as np
from numpy.typing import NDArray

from app.expr.evaluate import (
    Arith,
    Call,
    ChoiceEq,
    Cmp,
    Expr,
    Extremum,
    Interp,
    Logic,
    Neg,
    Not,
    Values,
    Var,
    Where,
)

Mask = NDArray[np.bool_]


def children(expr: Expr) -> tuple[Expr, ...]:
    """Direct sub-expressions; leaves (constants, tables, names) have none."""
    if isinstance(expr, Arith | Cmp):
        return expr.left, expr.right
    if isinstance(expr, Neg | Not):
        return (expr.operand,)
    if isinstance(expr, Logic):
        return expr.operands
    if isinstance(expr, Extremum | Call):
        return expr.args
    if isinstance(expr, Where):
        return expr.cond, expr.then, expr.other
    if isinstance(expr, Interp):
        return (expr.x,)
    return ()


def walk(expr: Expr) -> Iterator[Expr]:
    yield expr
    for child in children(expr):
        yield from walk(child)


def selects_path(expr: Expr) -> bool:
    """Whether the decisive references can differ between iterations (max, min or where)."""
    return any(isinstance(e, Extremum | Where) for e in walk(expr))


def activity(expr: Expr, values: Values) -> dict[str, Mask]:
    """Reference -> iterations in which it takes part in the result.

    ``max``/``min``: only the winning arguments (ties: all winners); ``where``: only the chosen
    branch, the condition itself is not on the path; everything else: all operands.
    Masks may be 0-dimensional (True everywhere); callers broadcast them.
    """
    active: dict[str, Mask] = {}
    _collect(expr, values, np.asarray(True), active)
    return active


def _collect(expr: Expr, values: Values, mask: Mask, active: dict[str, Mask]) -> None:
    if isinstance(expr, Var | ChoiceEq):
        previous = active.get(expr.name)
        active[expr.name] = mask if previous is None else previous | mask
    elif isinstance(expr, Extremum):
        for arg, wins in zip(expr.args, expr.winners(values), strict=True):
            _collect(arg, values, mask & wins, active)
    elif isinstance(expr, Where):
        cond = np.asarray(expr.cond.evaluate(values), dtype=np.bool_)
        _collect(expr.then, values, mask & cond, active)
        _collect(expr.other, values, mask & ~cond, active)
    else:
        for child in children(expr):
            _collect(child, values, mask, active)
