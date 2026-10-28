"""The knob of a lesson changes one literal value and nothing else (M2 AK 11)."""

import numpy as np
import pytest
from pydantic import ValidationError

from app.engine.simulate import simulate
from app.lessons.knob import current_value, with_value
from app.model.compile import compile_model
from app.model.schema import ConstantNode, EventNode, UncertainNode
from app.model.yaml_io import model_from_yaml

TEXT = (
    "schema_version: 1\nmodel: m\nsettings: {n: 5000, seed: 3}\nnodes:\n"
    "  k: {type: constant, value: 2}\n"
    "  e: {type: event, p: 0.2}\n"
    "  a: {type: uncertain, dist: normal, mean: 10, sd: 2}\n"
    "  b: {type: uncertain, dist: exponential, input: mean, mean: 5}\n"
    "  y: {type: output, expr: 'a * k + where(e, b, 0)'}\n"
    "  z: {type: output, expr: b}\n"
)


def test_current_values() -> None:
    model = model_from_yaml(TEXT)
    assert current_value(model, "k", "value") == 2.0
    assert current_value(model, "e", "p") == 0.2
    assert current_value(model, "a", "sd") == 2.0
    assert current_value(model, "y", "expr") is None
    assert current_value(model, "missing", "value") is None


def test_with_value_changes_only_that_field() -> None:
    model = model_from_yaml(TEXT)
    changed = with_value(model, "a", "sd", 3.0)
    a = changed.nodes["a"]
    assert isinstance(a, UncertainNode)
    assert a.params() == {"mean": 10, "sd": 3.0}
    assert model.nodes["a"] != a  # original untouched
    assert {k: v for k, v in changed.nodes.items() if k != "a"} == {
        k: v for k, v in model.nodes.items() if k != "a"
    }
    k = with_value(model, "k", "value", 4).nodes["k"]
    assert isinstance(k, ConstantNode)
    assert k.value == 4
    e = with_value(model, "e", "p", 0.5).nodes["e"]
    assert isinstance(e, EventNode)
    assert e.p == 0.5


def test_unaffected_nodes_draw_bitwise_equal() -> None:
    model = model_from_yaml(TEXT)
    before = simulate(compile_model(model))
    after = simulate(compile_model(with_value(model, "a", "mean", 20)))
    np.testing.assert_array_equal(before.samples["z"], after.samples["z"])
    assert not np.array_equal(before.samples["y"], after.samples["y"])


def test_invalid_value_rejected_by_schema() -> None:
    with pytest.raises(ValidationError):
        with_value(model_from_yaml(TEXT), "k", "value", "viel")  # pyright: ignore[reportArgumentType]
