"""Model edits of M5: quantile input -> piecewise, CSV values -> empirical."""

import pytest

from app.errors import InputError
from app.model.compile import compile_model
from app.model.edits import MAX_VALUES, to_empirical, to_piecewise
from app.model.schema import UncertainNode
from app.model.yaml_io import model_from_yaml

TEXT = (
    "schema_version: 1\nmodel: m\nnodes:\n"
    "  x: {type: uncertain, dist: normal, input: quantiles, p10: 2031, p50: 2038, p90: 2060,"
    " name: Reife, why: Studie}\n"
    "  y: {type: output, expr: x}\n"
)


def test_to_piecewise_keeps_quantiles_labels_and_reason() -> None:
    model = to_piecewise(model_from_yaml(TEXT), "x", 2025, 2090)
    node = model.nodes["x"]
    assert isinstance(node, UncertainNode)
    assert node.dist == "piecewise"
    assert node.params() == {
        "probs": [0, 0.1, 0.5, 0.9, 1],
        "values": [2025, 2031, 2038, 2060, 2090],
    }
    assert (node.name, node.why) == ("Reife", "Studie")
    compile_model(model)


@pytest.mark.parametrize(("p0", "p100"), [(2031, 2090), (2025, 2060)])
def test_to_piecewise_needs_bounds_outside_quantiles(p0: float, p100: float) -> None:
    with pytest.raises(InputError) as exc:
        to_piecewise(model_from_yaml(TEXT), "x", p0, p100)
    assert exc.value.issue.code == "fit.bounds"


def test_to_empirical_sets_values_and_limits_count() -> None:
    model = to_empirical(model_from_yaml(TEXT), "x", [3.0, 1.0, 2.0])
    node = model.nodes["x"]
    assert isinstance(node, UncertainNode)
    assert (node.dist, node.input, node.params()) == ("empirical", "params", {"values": [3, 1, 2]})
    with pytest.raises(InputError) as exc:
        to_empirical(model_from_yaml(TEXT), "x", [1.0] * (MAX_VALUES + 1))
    assert exc.value.issue.code == "csv.too_many"
    with pytest.raises(InputError):
        to_empirical(model_from_yaml(TEXT), "x", [])
