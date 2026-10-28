"""Edits of one node's distribution (M5): new models, the input stays unchanged."""

from collections.abc import Mapping
from typing import Any

from app.errors import InputError, Issue
from app.model.schema import Model, UncertainNode

MAX_VALUES = 100_000  # CSV import into a value list
_KEEP = ("type", "name", "unit", "description", "why", "tags", "bounds", "track")


def replace_distribution(model: Model, node_id: str, dist: str, params: Mapping[str, Any]) -> Model:
    """``node_id`` with a new distribution; labels, reason, bounds and tracking stay."""
    data = model.model_dump(mode="json", exclude_unset=True)
    old = data["nodes"][node_id]
    data["nodes"][node_id] = {
        **{k: old[k] for k in _KEEP if k in old},
        "dist": dist,
        "input": "params",
        **params,
    }
    return Model.model_validate(data)


def to_piecewise(model: Model, node_id: str, p0: float, p100: float) -> Model:
    """Quantile input (P10/P50/P90) -> piecewise with the user's bounds P0 and P100."""
    node = model.nodes[node_id]
    assert isinstance(node, UncertainNode)
    given = node.params()
    p10, p50, p90 = (float(given[k]) for k in ("p10", "p50", "p90"))  # pyright: ignore[reportArgumentType]
    if not p0 < p10 or not p100 > p90:
        params = {"p10": p10, "p90": p90}
        raise InputError(Issue("fit.bounds", node_id, params=params))
    params = {"probs": [0, 0.1, 0.5, 0.9, 1], "values": [p0, p10, p50, p90, p100]}
    return replace_distribution(model, node_id, "piecewise", params)


def to_empirical(model: Model, node_id: str, values: list[float]) -> Model:
    """An empirical distribution from imported values (at most MAX_VALUES)."""
    if not values or len(values) > MAX_VALUES:
        raise InputError(
            Issue("csv.too_many", node_id, params={"count": len(values), "limit": MAX_VALUES})
        )
    return replace_distribution(model, node_id, "empirical", {"values": values})
