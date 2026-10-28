"""Tornado: each uncertain input fixed at its P10 and P90, common random numbers (M4 AK 3)."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
import dataclasses
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray

from app.analysis.criticality import ancestors
from app.analysis.stats import hits
from app.engine.simulate import simulate
from app.model.compile import CConstant, CompiledModel, CUncertain
from app.model.schema import Target

Metric = Literal["mean", "median", "target"]
DEFAULT_N = 20_000
MANY_RUNS = 50  # the page warns about the run time above this


@dataclass(frozen=True)
class TornadoBar:
    node: str
    low_value: float  # P10 of the simulated marginal distribution
    high_value: float  # P90
    low: float  # metric of the output with the input fixed at P10
    high: float
    connected: bool  # has a path to the output

    @property
    def swing(self) -> float:
        return self.high - self.low


@dataclass(frozen=True)
class Tornado:
    output: str
    metric: Metric
    base: float
    bars: tuple[TornadoBar, ...]  # largest |swing| first
    runs: int


def _stat(metric: Metric, target: Target | None) -> Callable[[NDArray[Any]], float]:
    if metric == "target":
        if target is None:
            raise ValueError("metric 'target' needs an output with a target")
        return lambda x: float(np.mean(hits(np.asarray(x, dtype=np.float64), target)))
    fn = np.mean if metric == "mean" else np.median
    return lambda x: float(fn(np.asarray(x, dtype=np.float64)))


def fixed(compiled: CompiledModel, node: str, value: float) -> CompiledModel:
    """The model with ``node`` replaced by a constant; every other stream stays the same."""
    cnode = dataclasses.replace(compiled.nodes[node], body=CConstant(value))
    return dataclasses.replace(compiled, nodes={**compiled.nodes, node: cnode})


def p10_p90(body: CUncertain, x: NDArray[Any]) -> tuple[float, float]:
    """Quantiles of the simulated marginal; discrete families keep real values of the support."""
    method = "inverted_cdf" if body.family.kind == "discrete" else "linear"
    lo, hi = np.quantile(x, [0.1, 0.9], method=method)
    return float(lo), float(hi)


def tornado(
    compiled: CompiledModel,
    output: str,
    *,
    metric: Metric = "mean",
    n: int = DEFAULT_N,
    seed: int = 0,
) -> Tornado:
    """Two runs per uncertain input with the same seed; swing = metric(P90) − metric(P10)."""
    stat = _stat(metric, compiled.nodes[output].target)
    base = simulate(compiled, n=n, seed=seed, keep="all").samples
    connected = ancestors(compiled, output)
    bars: list[TornadoBar] = []
    for node_id in compiled.order:
        body = compiled.nodes[node_id].body
        if not isinstance(body, CUncertain):
            continue
        lo_value, hi_value = p10_p90(body, base[node_id])
        lo, hi = (
            stat(simulate(fixed(compiled, node_id, v), n=n, seed=seed).samples[output])
            for v in (lo_value, hi_value)
        )
        bars.append(TornadoBar(node_id, lo_value, hi_value, lo, hi, node_id in connected))
    bars.sort(key=lambda bar: (-abs(bar.swing), bar.node))
    return Tornado(output, metric, stat(base[output]), tuple(bars), 2 * len(bars))


def run_count(compiled: CompiledModel) -> int:
    """Simulation runs a tornado needs (without the base run)."""
    return 2 * sum(isinstance(node.body, CUncertain) for node in compiled.nodes.values())
