"""Gaussian copula: correlated uniforms from the members' own streams (M5)."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
from collections.abc import Mapping
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from app.engine.streams import uniforms
from app.model.correlations import Group

_EDGE = 2.0**-53


def correlated_uniforms(seed: int, group: Group, n: int) -> dict[str, NDArray[np.float64]]:
    """Per member: Φ(F z) with z = Φ⁻¹(u) from the member's stream, in the open interval (0, 1).

    Nodes outside groups keep their streams untouched; inside a group the streams stay the same
    across scenarios, so common random numbers hold.
    """
    z = np.stack([_normal_ppf(uniforms(seed, node, n)) for node in group.nodes])
    u = np.clip(_normal_cdf(group.factor @ z), _EDGE, 1 - _EDGE)
    return {node: u[i] for i, node in enumerate(group.nodes)}


def _normal_ppf(u: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.asarray(stats.norm.ppf(u), dtype=np.float64)  # pyright: ignore[reportUnknownArgumentType]


def _normal_cdf(z: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.asarray(stats.norm.cdf(z), dtype=np.float64)  # pyright: ignore[reportUnknownArgumentType]


def _ranks(x: NDArray[Any]) -> NDArray[np.float64]:
    ranks = stats.rankdata(np.asarray(x, dtype=np.float64))  # pyright: ignore[reportUnknownVariableType]
    return np.asarray(ranks, dtype=np.float64)  # pyright: ignore[reportUnknownArgumentType]


def achieved(values: Mapping[str, NDArray[Any]], group: Group) -> NDArray[np.float64]:
    """Spearman matrix the run reached between the group's members."""
    ranks = np.stack([_ranks(values[node]) for node in group.nodes])
    with np.errstate(all="ignore"):
        return np.asarray(np.corrcoef(ranks), dtype=np.float64)
