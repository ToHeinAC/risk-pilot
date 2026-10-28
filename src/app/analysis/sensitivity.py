"""Spearman rank correlation of each input with an output, from one run (M4 AK 5).

Descriptive: it shows how inputs and output move together in the model, not a cause and not
an effect size.
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

from app.model.compile import CompiledModel

INPUTS = ("uncertain", "event")
FISHER_SE = 1.03  # Fieller, Hartley and Pearson (1957): SE of atanh(rho) ≈ 1.03 / sqrt(N - 3)


@dataclass(frozen=True)
class RankCorrelation:
    node: str
    rho: float | None  # None: input or output constant, no ranks to compare
    lo: float = math.nan
    hi: float = math.nan


def _ranks(x: NDArray[Any]) -> NDArray[np.float64]:
    """Average ranks (ties share their mean rank)."""
    ranks = stats.rankdata(np.asarray(x, dtype=np.float64))  # pyright: ignore[reportUnknownVariableType]
    return np.asarray(ranks, dtype=np.float64)  # pyright: ignore[reportUnknownArgumentType]


def _rho(x: NDArray[Any], y: NDArray[Any]) -> float | None:
    rx, ry = _ranks(x), _ranks(y)
    if np.ptp(rx) == 0 or np.ptp(ry) == 0:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


def _interval(rho: float, n: int, conf: float) -> tuple[float, float]:
    if n <= 3:
        return -1.0, 1.0
    z = math.atanh(min(max(rho, -0.999999), 0.999999))
    half = float(stats.norm.ppf(1 - (1 - conf) / 2)) * FISHER_SE / math.sqrt(n - 3)
    return math.tanh(z - half), math.tanh(z + half)


def spearman(
    compiled: CompiledModel, samples: Mapping[str, NDArray[Any]], output: str, conf: float = 0.95
) -> list[RankCorrelation]:
    """ρ of every uncertain and event node with ``output``, largest |ρ| first, undefined last."""
    y = samples[output]
    rows: list[RankCorrelation] = []
    for node_id in compiled.order:
        if compiled.nodes[node_id].type not in INPUTS:
            continue
        rho = _rho(samples[node_id], y)
        if rho is None:
            rows.append(RankCorrelation(node_id, None))
        else:
            rows.append(RankCorrelation(node_id, rho, *_interval(rho, y.size, conf)))
    rows.sort(key=lambda r: (r.rho is None, -abs(r.rho or 0.0), r.node))
    return rows
