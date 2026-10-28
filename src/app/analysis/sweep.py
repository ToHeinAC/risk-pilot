"""Sweep: statistics of an output over k values of one literal parameter (M4 AK 4)."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
from dataclasses import dataclass

import numpy as np

from app.analysis.stats import Summary, summarize
from app.engine.simulate import simulate
from app.errors import Issue, ModelError
from app.lessons.knob import current_value, with_value
from app.model.compile import CompiledModel, compile_model
from app.model.schema import Model, UncertainNode

DEFAULT_K = 9


@dataclass(frozen=True)
class SweepPlan:
    node: str
    field: str
    models: tuple[tuple[float, CompiledModel], ...]
    invalid: tuple[tuple[float, Issue], ...]  # reported before any run


@dataclass(frozen=True)
class SweepPoint:
    value: float
    summary: Summary


@dataclass(frozen=True)
class Sweep:
    node: str
    field: str
    output: str
    points: tuple[SweepPoint, ...]


def sweep_params(model: Model) -> list[tuple[str, str, float]]:
    """(node, field, current value) of every literal number a sweep can turn."""
    params: list[tuple[str, str, float]] = []
    for node_id, node in model.nodes.items():
        fields = list(node.params()) if isinstance(node, UncertainNode) else ["value", "p"]
        for field in fields:
            value = current_value(model, node_id, field)
            if value is not None:
                params.append((node_id, field, value))
    return params


def sweep_values(lo: float, hi: float, k: int = DEFAULT_K) -> tuple[float, ...]:
    return tuple(float(v) for v in np.linspace(lo, hi, k))


def plan_sweep(model: Model, node: str, field: str, values: tuple[float, ...]) -> SweepPlan:
    """Compile the model once per value; values the model does not allow are collected."""
    models: list[tuple[float, CompiledModel]] = []
    invalid: list[tuple[float, Issue]] = []
    for value in values:
        try:
            models.append((value, compile_model(with_value(model, node, field, value))))
        except ModelError as exc:
            invalid.append((value, exc.issues[0]))
    return SweepPlan(node, field, tuple(models), tuple(invalid))


def run_sweep(plan: SweepPlan, output: str, *, n: int, seed: int, quantile: float = 0.9) -> Sweep:
    """Mean, median, the chosen quantile and P(target) per value, all with the same seed."""
    if plan.invalid:
        raise ValueError("the sweep range contains invalid values")
    points = tuple(
        SweepPoint(
            value,
            summarize(
                simulate(compiled, n=n, seed=seed).samples[output],
                quantiles=(0.5, quantile),
                target=compiled.nodes[output].target,
            ),
        )
        for value, compiled in plan.models
    )
    return Sweep(plan.node, plan.field, output, points)
