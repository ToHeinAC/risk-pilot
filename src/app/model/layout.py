"""Node positions on the canvas: the optional top-level ``layout`` block (M9 E2, E10).

Positions change no number and no hash. Nodes without a position are placed from the layered
layout (``layers``: layer, row; the same layers as ``present.structure.positions``), scaled to
canvas pixels here. Every action is ``Data -> Data`` on the raw YAML data, written back with
``yaml_patch.patch``.
"""

from collections.abc import Iterable, Mapping, Sequence
from graphlib import CycleError, TopologicalSorter
from typing import Any, cast

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


def layers(ids: Sequence[str], links: Iterable[tuple[str, str]]) -> Layered:
    """Layered layout on raw data: each node one layer right of its latest input, rows centred
    per layer in the order of ``ids``. A cycle (invalid draft) puts every node in layer 0."""
    inputs: dict[str, set[str]] = {n: set() for n in ids}
    for source, target in links:
        if source in inputs and target in inputs and source != target:
            inputs[target].add(source)
    layer: dict[str, int] = dict.fromkeys(ids, 0)
    try:
        for node in TopologicalSorter(inputs).static_order():
            layer[node] = 1 + max((layer[i] for i in inputs[node]), default=-1)
    except CycleError:
        layer = dict.fromkeys(ids, 0)
    rows: dict[int, list[str]] = {}
    for node in ids:
        rows.setdefault(layer[node], []).append(node)
    return {
        n: (float(x), (len(row) - 1) / 2 - i)
        for x, row in sorted(rows.items())
        for i, n in enumerate(row)
    }


def _stored(value: object) -> tuple[float, float] | None:
    """A valid stored position, or None (the check reports a broken one)."""
    if not isinstance(value, list) or len(cast(list[object], value)) != 2:
        return None
    x, y = cast(list[object], value)
    numbers = all(isinstance(v, int | float) and not isinstance(v, bool) for v in (x, y))
    return (float(cast(float, x)), float(cast(float, y))) if numbers else None


def placed(data: Data, layered: Layered) -> dict[str, tuple[float, float]]:
    """Every node's position: the stored one, else the automatic one (raw data, valid or not)."""
    auto, stored = _pixels(layered), _layout(data)
    nodes = cast(dict[str, Any], data.get("nodes") or {})
    return {n: _stored(stored.get(n)) or auto.get(n, (0.0, 0.0)) for n in nodes}


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
