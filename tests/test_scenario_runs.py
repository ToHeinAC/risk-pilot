"""Simulation per scenario: common random numbers and T2 scenarios (M3 AK 5, 6)."""

from pathlib import Path

import numpy as np

from app.adapters.files import load_model
from app.engine.simulate import simulate
from app.model.compile import compile_model
from app.model.scenarios import effective_model
from app.model.yaml_io import model_from_yaml

T2 = Path(__file__).resolve().parent.parent / "examples" / "t2_terminplan.yaml"

MODEL = """schema_version: 1
model: m
settings: {n: 20000, seed: 5}
nodes:
  a: {type: uncertain, dist: normal, mean: 10, sd: 2, track: true}
  b: {type: uncertain, dist: lognormal, mu: 1, sigma: 0.5, track: true}
  e: {type: event, p: 0.1, track: true}
  y: {type: output, expr: "a + b + where(e, 3, 0)"}
scenarios:
  kind:
    name: Kind
    why: W
    overrides:
      a: {mean: 12}
  enkel:
    name: Enkel
    parent: kind
    why: W
    overrides:
      e: {p: 0.3}
"""


def run(model_text: str, scenario: str) -> dict[str, np.ndarray]:
    model = effective_model(model_from_yaml(model_text), scenario)
    return dict(simulate(compile_model(model)).samples)


def test_not_overridden_nodes_are_bitwise_equal() -> None:
    parent, child, grandchild = run(MODEL, "basis"), run(MODEL, "kind"), run(MODEL, "enkel")
    np.testing.assert_array_equal(parent["b"], child["b"])
    np.testing.assert_array_equal(parent["e"], child["e"])
    np.testing.assert_array_equal(child["a"], grandchild["a"])
    np.testing.assert_allclose(child["a"] - parent["a"], 2.0)  # coupled by inversion
    assert np.all(grandchild["e"][child["e"]])  # higher p: superset of events


def test_t2_faster_b_never_later() -> None:
    model = load_model(T2)
    base = simulate(compile_model(effective_model(model, "basis")), n=100_000).samples["ende"]
    fast = simulate(compile_model(effective_model(model, "b_schneller")), n=100_000).samples["ende"]
    d = fast - base
    assert np.all(d <= 0)
    assert np.any(d < 0)
    assert np.any(d == 0)  # where path 2 (C) decides, B does not matter


def test_t2_main_scenario_has_no_rework() -> None:
    model = load_model(T2)
    samples = simulate(compile_model(effective_model(model, "basis")), n=10_000).samples
    rework = simulate(compile_model(effective_model(model, "nacharbeit")), n=10_000).samples
    assert np.all(rework["ende"] >= samples["ende"])
    assert np.mean(rework["ende"] > samples["ende"]) > 0.05
    assert model.scenarios["nacharbeit"].name == "mit Nacharbeit"
