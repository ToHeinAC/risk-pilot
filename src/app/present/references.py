"""Analytic overlays for the tutorials T1 and T2 (only for the unchanged originals)."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from app.analysis.analytic import (
    clark_mean,
    dkw_epsilon,
    grid_convolve,
    ks_distance,
    max_of_normals_cdf,
    sum_uniform01_cdf,
    sum_uniform01_pdf,
)
from app.messages import t
from app.present.text import number

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class Curve:
    label: str
    x: FloatArray
    y: FloatArray


@dataclass(frozen=True)
class Reference:
    output: str
    pdf: list[Curve]
    cdf: list[Curve]
    ks: float
    eps: float
    notes: list[str]

    @property
    def passed(self) -> bool:
        return self.ks < self.eps


def _uniform01_pdf(x: FloatArray) -> FloatArray:
    return np.where((x >= 0) & (x <= 1), 1.0, 0.0)


def _t1(samples: Mapping[str, NDArray[Any]]) -> Reference:
    x = np.asarray(samples["s"], dtype=np.float64)
    grid = np.linspace(0, 2, 401)
    g, g_pdf, g_cdf = grid_convolve(_uniform01_pdf, _uniform01_pdf, 0, 1, 0, 1, 1e-3)
    deviation = float(np.max(np.abs(g_cdf - sum_uniform01_cdf(g))))
    analytic, numeric = t("ref.analytic"), t("ref.grid")
    return Reference(
        "s",
        [Curve(analytic, grid, sum_uniform01_pdf(grid)), Curve(numeric, g, g_pdf)],
        [Curve(analytic, grid, sum_uniform01_cdf(grid)), Curve(numeric, g, g_cdf)],
        ks_distance(x, sum_uniform01_cdf),
        dkw_epsilon(x.size),
        [t("ref.grid_note", deviation=f"{deviation:.1e}".replace(".", ","))],
    )


def _t2(samples: Mapping[str, NDArray[Any]]) -> Reference:
    x = np.asarray(samples["ende"], dtype=np.float64)
    s13 = math.sqrt(13)

    def cdf(t_: FloatArray) -> FloatArray:
        return max_of_normals_cdf(t_, 25, s13, 24, 4)

    grid = np.linspace(5, 50, 901)
    pdf = np.gradient(cdf(grid), grid)
    clark = clark_mean(25, s13, 24, 4)
    analytic = t("ref.analytic")
    note = t("ref.clark_note", clark=number(clark, 5), mean=number(float(np.mean(x)), 5))
    return Reference(
        "ende",
        [Curve(analytic, grid, np.asarray(pdf, dtype=np.float64))],
        [Curve(analytic, grid, cdf(grid))],
        ks_distance(x, cdf),
        dkw_epsilon(x.size),
        [note],
    )


_TUTORIALS = {"t1_faltung": _t1, "t2_terminplan": _t2}


def tutorial_reference(
    model_id: str, model_hash: str, original_hash: str | None, samples: Mapping[str, NDArray[Any]]
) -> Reference | None:
    """The analytic reference, if this is an unchanged tutorial; otherwise None."""
    build = _TUTORIALS.get(model_id)
    if build is None or original_hash is None or model_hash != original_hash:
        return None
    return build(samples)


def has_reference(model_id: str) -> bool:
    return model_id in _TUTORIALS
