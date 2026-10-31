"""The analysis run and its derived results; no UI import."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from numpy.typing import NDArray

from app.analysis.criticality import Criticality, criticality
from app.analysis.riskmatrix import RiskRow, risk_matrix
from app.analysis.schedule import Bar, bars, schedule
from app.analysis.sensitivity import RankCorrelation, spearman
from app.analysis.sweep import Sweep
from app.analysis.tornado import Tornado
from app.engine.simulate import simulate
from app.model.compile import CompiledModel

MEMORY_HINT_MB = 500
Key = tuple[str, str, str, int, int]  # draft, scenario, output, N, seed


@dataclass(frozen=True)
class Base:
    """One run with every node kept, and what is computed from it."""

    key: Key
    compiled: CompiledModel
    output: str
    names: Mapping[str, str]
    crit: Criticality
    rho: list[RankCorrelation]
    risks: list[RiskRow]
    plan: list[Bar]  # the schedule up to the output (Gantt)


@dataclass
class AnalysisState:
    """The last analysis of a tab; tornado and sweep remember the settings they ran with."""

    base: Base | None = None
    tornado: tuple[object, Tornado] | None = None
    sweep: tuple[object, Sweep] | None = None


def names(compiled: CompiledModel) -> dict[str, str]:
    return {i: node.name or i for i, node in compiled.model.nodes.items()}


def outputs(compiled: CompiledModel) -> list[str]:
    return [i for i, node in compiled.nodes.items() if node.type == "output"]


def memory_mb(compiled: CompiledModel, n: int) -> float:
    """Memory of a run that keeps every node (8 bytes per draw)."""
    return n * len(compiled.nodes) * 8 / 1e6


def compute(key: Key, compiled: CompiledModel, output: str) -> Base:
    """Simulate with every node kept; raises ``SimulationError``."""
    samples: Mapping[str, NDArray[Any]] = simulate(
        compiled, n=key[3], seed=key[4], keep="all"
    ).samples
    labels = names(compiled)
    return Base(
        key,
        compiled,
        output,
        labels,
        criticality(compiled, samples, output),
        spearman(compiled, samples, output),
        risk_matrix(compiled, samples, output),
        bars(schedule(compiled, samples, output), labels),
    )
