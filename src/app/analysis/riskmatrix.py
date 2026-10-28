"""Risk matrix: per event its probability and the conditional difference of an output (M4 AK 6).

The difference is no causal effect when events share causes or interact.
"""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from app.analysis.stats import Proportion, proportion
from app.model.compile import CompiledModel


@dataclass(frozen=True)
class Difference:
    value: float  # E[Y | event] − E[Y | no event]
    lo: float  # Welch interval
    hi: float


@dataclass(frozen=True)
class RiskRow:
    node: str
    p: Proportion
    diff: Difference | None  # None: the event never or always occurs (or too rarely)


def welch(a: NDArray[np.float64], b: NDArray[np.float64], conf: float) -> Difference | None:
    """mean(a) − mean(b) with Welch's interval; None if a group has fewer than two values."""
    na, nb = a.size, b.size
    if na < 2 or nb < 2:
        return None
    va, vb = float(np.var(a, ddof=1)) / na, float(np.var(b, ddof=1)) / nb
    diff = float(np.mean(a) - np.mean(b))
    se = math.sqrt(va + vb)
    if se == 0:
        return Difference(diff, diff, diff)
    df = (va + vb) ** 2 / (va**2 / (na - 1) + vb**2 / (nb - 1))
    half = float(stats.t.ppf(1 - (1 - conf) / 2, df)) * se
    return Difference(diff, diff - half, diff + half)


def risk_matrix(
    compiled: CompiledModel, samples: Mapping[str, NDArray[Any]], output: str, conf: float = 0.95
) -> list[RiskRow]:
    """One row per event node, in model order."""
    y = np.asarray(samples[output], dtype=np.float64)
    rows: list[RiskRow] = []
    for node_id in compiled.order:
        if compiled.nodes[node_id].type != "event":
            continue
        occurs = np.asarray(samples[node_id], dtype=np.bool_)
        rows.append(RiskRow(node_id, proportion(occurs, conf), welch(y[occurs], y[~occurs], conf)))
    return rows
