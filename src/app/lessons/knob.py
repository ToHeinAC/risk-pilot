"""The knob of a lesson: one literal number of the model, changed in memory only."""

from app.model.schema import ConstantNode, EventNode, Model, UncertainNode


def current_value(model: Model, node_id: str, field: str) -> float | None:
    """The literal number in ``node_id.field``, or None if there is none."""
    node = model.nodes.get(node_id)
    value: object = None
    if isinstance(node, ConstantNode) and field == "value":
        value = node.value
    elif isinstance(node, EventNode) and field == "p":
        value = node.p
    elif isinstance(node, UncertainNode):
        value = node.params().get(field)
    if isinstance(value, int | float) and not isinstance(value, bool):
        return float(value)
    return None


def with_value(model: Model, node_id: str, field: str, value: float) -> Model:
    """A new model with ``node_id.field`` set to ``value``; ``model`` stays unchanged.

    This is a transient change for the learning path, not a scenario (M3).
    """
    data = model.model_dump(mode="json", exclude_unset=True)
    data["nodes"][node_id][field] = value
    return Model.model_validate(data)
