"""Decisive path, criticality index and path constellations (M4 AK 2)."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from app.analysis.stats import Proportion, proportion, wilson
from app.expr.activity import activity, selects_path
from app.model.compile import CExpr, CompiledModel

Mask = NDArray[np.bool_]
INDEXED = ("uncertain", "event", "derived")
INPUTS = ("uncertain", "event")
TOP = 10  # constellations from this rank on are collected in one row


@dataclass(frozen=True)
class Constellation:
    nodes: tuple[str, ...]  # critical inputs of these iterations
    share: Proportion
    rest: int = 0  # > 0: the row collects this many rarer constellations


@dataclass(frozen=True)
class Criticality:
    output: str
    indices: tuple[tuple[str, Proportion], ...]  # most critical first; they need not sum to 1
    constellations: tuple[Constellation, ...]  # most frequent first; they sum to 1
    selects_path: bool  # False: no max, min or where on the way, every input always critical

    def index(self, node: str) -> Proportion:
        return dict(self.indices)[node]


def ancestors(compiled: CompiledModel, node: str) -> set[str]:
    """``node`` and every node with a path to it."""
    seen, stack = {node}, [node]
    while stack:
        for ref in compiled.refs[stack.pop()]:
            if ref not in seen:
                seen.add(ref)
                stack.append(ref)
    return seen


def decisive_masks(
    compiled: CompiledModel, samples: Mapping[str, NDArray[Any]], output: str
) -> dict[str, Mask]:
    """Per node with a path to ``output``: the iterations in which it is on the decisive path.

    Backwards in reverse topological order; parameters of random nodes are fully on the path.
    """
    n = samples[output].size
    masks = {node: np.zeros(n, dtype=np.bool_) for node in ancestors(compiled, output)}
    masks[output][:] = True
    for node_id in reversed(compiled.order):
        if node_id not in masks:
            continue
        body = compiled.nodes[node_id].body
        if isinstance(body, CExpr):
            parts = activity(body.expr, samples)
        else:
            parts = {ref: np.asarray(True) for ref in compiled.refs[node_id]}
        for ref, active in parts.items():
            masks[ref] |= masks[node_id] & active
    return masks


def criticality(
    compiled: CompiledModel, samples: Mapping[str, NDArray[Any]], output: str, conf: float = 0.95
) -> Criticality:
    """Criticality index of every random or derived node, and the path constellations."""
    masks = decisive_masks(compiled, samples, output)
    types = {node: compiled.nodes[node].type for node in masks}
    indices = sorted(
        ((node, proportion(mask, conf)) for node, mask in masks.items() if types[node] in INDEXED),
        key=lambda row: (-row[1].p, row[0]),
    )
    inputs = sorted(node for node in masks if types[node] in INPUTS)
    selecting = any(
        isinstance(body, CExpr) and selects_path(body.expr)
        for body in (compiled.nodes[node].body for node in masks)
    )
    return Criticality(
        output, tuple(indices), constellations(masks, inputs, samples[output].size, conf), selecting
    )


def constellations(
    masks: Mapping[str, Mask], inputs: list[str], n: int, conf: float
) -> tuple[Constellation, ...]:
    """The set of critical inputs per iteration, counted; rare ones collected from rank TOP on."""
    if not inputs:
        return (Constellation((), _share(n, n, conf)),)
    matrix = np.stack([masks[node] for node in inputs], axis=1)
    rows, counts = np.unique(matrix, axis=0, return_counts=True)
    found = sorted(
        (
            (int(count), tuple(node for node, on in zip(inputs, row, strict=True) if on))
            for row, count in zip(rows, counts, strict=True)
        ),
        key=lambda item: (-item[0], item[1]),
    )
    if len(found) > TOP:
        rest = found[TOP - 1 :]
        tail = Constellation((), _share(sum(k for k, _ in rest), n, conf), rest=len(rest))
        return (*(Constellation(c, _share(k, n, conf)) for k, c in found[: TOP - 1]), tail)
    return tuple(Constellation(c, _share(k, n, conf)) for k, c in found)


def _share(k: int, n: int, conf: float) -> Proportion:
    return Proportion(k, n, k / n, *wilson(k, n, conf))
