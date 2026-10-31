"""A schedule read from the expressions, per draw (pure): the data of the Gantt view.

The expression of an output is read as a network plan: in ``a + b`` and ``sum(a, b)`` b starts
when a ends; in ``max(a, b)`` both start together and the next step waits for both, in
``min(a, b)`` for the first. A node whose expression is a sum, ``max``, ``min`` or a name is a
milestone; any other node is one bar as long as its value, and any other term inside a sum is a
block as long as the term's value.
"""

import ast
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray

from app.expr.evaluate import as_num
from app.expr.parser import compile_expr
from app.model.compile import CompiledModel

Kind = Literal["activity", "milestone", "block"]
Times = NDArray[np.float64]
Samples = Mapping[str, NDArray[Any]]
_JOINS = ("max", "min", "sum")


@dataclass(frozen=True)
class Step:
    node: str  # node ID; a block is "<node>:<term>"
    kind: Kind
    start: Times
    finish: Times
    after: tuple[str, ...]  # the steps whose end lets this one start


@dataclass(frozen=True)
class Bar:
    node: str
    label: str
    kind: Kind
    start: float  # medians over the draws
    finish: float
    lo: float  # P10 and P90 of the finish
    hi: float
    after: tuple[str, ...]


def _expr(compiled: CompiledModel, node_id: str) -> ast.expr | None:
    """The expression of a derived node or output, if it reads as a plan."""
    text = getattr(compiled.model.nodes[node_id], "expr", None)
    if not isinstance(text, str):
        return None
    body = ast.parse(text, mode="eval").body
    planned = isinstance(body, ast.Name) or _join(body) is not None
    return body if planned or _is_sum(body) else None


def _is_sum(node: ast.expr) -> bool:
    return isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add)


def _join(node: ast.expr) -> str | None:
    """``max``, ``min`` or ``sum`` with arguments; None for anything else."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.args:
        return node.func.id if node.func.id in _JOINS else None
    return None


class _Plan:
    def __init__(self, compiled: CompiledModel, samples: Samples) -> None:
        self.compiled = compiled
        self.samples = samples
        self.env = {i: c.vtype for i, c in compiled.nodes.items()}
        self.steps: dict[str, Step] = {}

    def add(self, step: Step) -> None:
        self.steps.setdefault(step.node, step)  # a shared node keeps its first place

    def node(
        self, node_id: str, start: Times, after: tuple[str, ...]
    ) -> tuple[Times, tuple[str, ...]]:
        body = _expr(self.compiled, node_id)
        if body is None:
            finish = start + as_num(np.asarray(self.samples[node_id]))
            self.add(Step(node_id, "activity", start, finish, after))
            return finish, (node_id,)
        finish, enders = self.term(body, start, after, node_id)
        self.add(Step(node_id, "milestone", finish, finish, enders))
        return finish, (node_id,)

    def term(
        self, expr: ast.expr, start: Times, after: tuple[str, ...], owner: str
    ) -> tuple[Times, tuple[str, ...]]:
        if _is_sum(expr):
            assert isinstance(expr, ast.BinOp)
            middle, enders = self.term(expr.left, start, after, owner)
            return self.term(expr.right, middle, enders, owner)
        join = _join(expr)
        if join == "sum":
            assert isinstance(expr, ast.Call)
            for arg in expr.args:
                start, after = self.term(arg, start, after, owner)
            return start, after
        if join is not None:
            assert isinstance(expr, ast.Call)
            parts = [self.term(arg, start, after, owner) for arg in expr.args]
            ends = np.stack([f for f, _ in parts])  # pyright: ignore[reportUnknownMemberType]
            finish = ends.max(axis=0) if join == "max" else ends.min(axis=0)
            return finish, tuple(dict.fromkeys(e for _, ends in parts for e in ends))
        if isinstance(expr, ast.Name) and expr.id in self.compiled.nodes:
            return self.node(expr.id, start, after)
        return self.block(expr, start, after, owner)

    def block(
        self, expr: ast.expr, start: Times, after: tuple[str, ...], owner: str
    ) -> tuple[Times, tuple[str, ...]]:
        text = ast.unparse(expr)
        value = compile_expr(text, self.env).node.evaluate(dict(self.samples))
        finish = start + as_num(np.asarray(value))
        block_id = f"{owner}:{text}"
        if isinstance(expr, ast.Constant):
            return finish, after  # a fixed lag draws no bar of its own
        self.add(Step(block_id, "block", start, finish, after))
        return finish, (block_id,)


def schedule(compiled: CompiledModel, samples: Samples, output: str) -> list[Step]:
    """The steps leading to ``output``, each with its start and finish per draw."""
    plan = _Plan(compiled, samples)
    size = len(np.asarray(samples[output]))
    plan.node(output, np.zeros(size), ())
    return list(plan.steps.values())


def bars(steps: Sequence[Step], names: Mapping[str, str]) -> list[Bar]:
    """One row per step in order of median start, then finish; medians and finish spread."""
    rows: list[Bar] = []
    for s in steps:
        owner, _, term = s.node.partition(":")
        label = f"{names.get(owner, owner)}: {term}" if term else names.get(s.node, s.node)
        spread = np.quantile(s.finish, [0.1, 0.5, 0.9])  # pyright: ignore[reportUnknownMemberType]
        lo, mid, hi = (float(v) for v in spread)
        start = float(np.median(s.start))
        rows.append(Bar(s.node, label, s.kind, start, mid, lo, hi, s.after))
    return sorted(rows, key=lambda r: (r.start, r.finish))
