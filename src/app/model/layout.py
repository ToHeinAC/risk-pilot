"""Node positions on the canvas: the optional top-level ``layout`` block (M9 E2, E10).

Positions change no number and no hash. Nodes without a position are placed from the layered
layout (``present.structure.positions``: layer, row), scaled to canvas pixels here. Every action
is ``Data -> Data`` on the raw YAML data, written back with ``yaml_patch.patch``.
"""

from collections.abc import Mapping
from typing import Any, cast

from app.model.schema import Model
from app.model.yaml_patch import Data

STEP_X = 220  # canvas pixels between two layers
STEP_Y = 110  # canvas pixels between two rows of a layer

Layered = Mapping[str, tuple[float, float]]


def _layout(data: Data) -> dict[str, Any]:
    return dict(cast(dict[str, Any], data.get("layout") or {}))


def _pixels(layered: Layered) -> dict[str, tuple[float, float]]:
    """Layer and row as pixels; the top row at y = 0 (canvas y grows downwards)."""
    top = max((y for _, y in layered.values()), default=0.0)
    return {n: (x * STEP_X, (top - y) * STEP_Y) for n, (x, y) in layered.items()}


def placed(model: Model, layered: Layered) -> dict[str, tuple[float, float]]:
    """Every node's position: the stored one, else the automatic one."""
    auto = _pixels(layered)
    return {n: model.layout.get(n, auto.get(n, (0.0, 0.0))) for n in model.nodes}


def move(data: Data, node_id: str, x: float, y: float) -> Data:
    """``data`` with ``node_id`` at (x, y), rounded to whole pixels."""
    return {**data, "layout": {**_layout(data), node_id: [round(x), round(y)]}}


def arrange(data: Data, layered: Layered) -> Data:
    """„Neu anordnen“: every node at its automatic position, in the order of ``nodes``."""
    pos = _pixels(layered)
    nodes = cast(dict[str, Any], data.get("nodes") or {})
    return {**data, "layout": {n: [round(pos[n][0]), round(pos[n][1])] for n in nodes if n in pos}}


def unknown(data: Data) -> list[str]:
    """Positions of nodes the model does not have."""
    nodes = cast(dict[str, Any], data.get("nodes") or {})
    return [n for n in _layout(data) if n not in nodes]


def prune(data: Data) -> Data:
    """``data`` without positions of unknown nodes (only on request, never silently)."""
    gone = set(unknown(data))
    return {**data, "layout": {n: p for n, p in _layout(data).items() if n not in gone}}


def without(data: Data, node_id: str) -> Data:
    """``data`` without the position of a removed node."""
    if node_id not in _layout(data):
        return data
    return {**data, "layout": {n: p for n, p in _layout(data).items() if n != node_id}}
