"""Compact per-node views for the node table (M8 E8, Guesstimate principle), pure.

``brief`` is the short form of a node's input ("10 bis 20 d, meist 15"), ``spark_svg`` a tiny
histogram drawn inline per row, ``trace`` P10/P50/P90 of every node from one trial run.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from app.model.schema import ConstantNode, EventNode, Node, UncertainNode
from app.present.text import number, percent

SPARK_BINS = 20


def _u(unit: str | None) -> str:
    return f" {unit}" if unit else ""


def _value(v: Any) -> str:
    return number(float(v)) if isinstance(v, int | float) else str(v)


def _uncertain(node: UncertainNode) -> str:
    p, u = node.params(), _u(node.unit)
    if {"low", "mode", "high"} <= set(p):
        return f"{_value(p['low'])} bis {_value(p['high'])}{u}, meist {_value(p['mode'])}"
    if {"p10", "p50", "p90"} <= set(p):
        return f"{_value(p['p10'])} bis {_value(p['p90'])}{u}, Mitte {_value(p['p50'])}"
    if {"low", "high"} <= set(p):
        return f"{_value(p['low'])} bis {_value(p['high'])}{u}, gleich verteilt"
    if {"mean", "sd"} <= set(p):
        return f"um {_value(p['mean'])}{u} ± {_value(p['sd'])}"
    return f"{node.dist}({', '.join(f'{k}={_value(v)}' for k, v in p.items())})"


def brief(node: Node) -> str:
    """The node's input in a few words, in the model's unit."""
    if isinstance(node, UncertainNode):
        return _uncertain(node)
    if isinstance(node, ConstantNode):
        return f"{_value(node.value)}{_u(node.unit)}"
    if isinstance(node, EventNode):
        return f"tritt ein mit {percent(node.p)}" if isinstance(node.p, float) else f"p = {node.p}"
    return str(getattr(node, "expr", "") or "")


def spark_svg(x: NDArray[Any], width: int = 96, height: int = 22) -> str:
    """A histogram as inline SVG; one bar per class, colour from the CSS ``currentColor``."""
    values = np.asarray(x, dtype=np.float64)
    if values.size == 0 or float(values.max() - values.min()) == 0:
        counts = np.zeros(SPARK_BINS)
        counts[SPARK_BINS // 2] = 1.0
    else:
        counts = np.histogram(values, bins=SPARK_BINS)[0].astype(np.float64)  # pyright: ignore[reportUnknownMemberType]
    heights = counts / counts.max() * (height - 1)
    bar = width / SPARK_BINS
    rects = "".join(
        f'<rect x="{i * bar:.1f}" y="{height - h:.1f}" width="{bar - 1:.1f}" height="{h:.1f}"/>'
        for i, h in enumerate(heights)
    )
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'fill="currentColor" role="img">{rects}</svg>'
    )


@dataclass(frozen=True)
class Trace:
    p10: float
    p50: float
    p90: float
    mean: float  # for yes/no nodes the share of "yes"


def trace(samples: Mapping[str, NDArray[Any]]) -> dict[str, Trace]:
    """P10/P50/P90 and mean of every node of a trial run."""
    found: dict[str, Trace] = {}
    for node_id, x in samples.items():
        values = np.asarray(x, dtype=np.float64)
        q = np.quantile(values, [0.1, 0.5, 0.9])  # pyright: ignore[reportUnknownMemberType]
        found[node_id] = Trace(float(q[0]), float(q[1]), float(q[2]), float(values.mean()))
    return found
