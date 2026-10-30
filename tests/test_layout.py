"""M9 AP2: node positions in the optional ``layout`` block (E2, E10)."""

import pytest

from app.adapters import files, settings
from app.errors import ModelError
from app.model import form, layout
from app.model.compile import compile_model, content_hash, model_hash
from app.model.graph import edges
from app.model.schema import Model
from app.model.yaml_io import model_from_yaml
from app.model.yaml_patch import load_data, patch
from app.present.structure import positions

BASE = """schema_version: 1
model: m
nodes:
  a: {type: constant, value: 1}
  z: {type: output, expr: "a"}
"""


def _model(extra: str = "") -> Model:
    return model_from_yaml(BASE + extra)


def test_layout_is_read_as_positions() -> None:
    model = _model("layout:\n  a: [0, 120]\n  z: [220.5, 0]\n")
    assert model.layout == {"a": (0.0, 120.0), "z": (220.5, 0.0)}


@pytest.mark.parametrize("bad", ["[1, 2, 3]", "[1]", "[a, 2]", "7"])
def test_a_position_is_two_numbers(bad: str) -> None:
    with pytest.raises(ModelError):
        _model(f"layout:\n  a: {bad}\n")


def test_layout_changes_no_hash() -> None:
    plain, placed = _model(), _model("layout:\n  a: [0, 120]\n")
    assert content_hash(plain) == content_hash(placed)
    assert model_hash(plain) == model_hash(placed)


def test_position_of_an_unknown_node_is_a_notice() -> None:
    compiled = compile_model(_model("layout:\n  gone: [1, 2]\n"))
    assert [(n.code, n.node_id) for n in compiled.notices] == [("layout.unknown_node", "gone")]


def test_move_writes_one_rounded_position() -> None:
    data = layout.move(load_data(BASE), "a", 10.4, -3.6)
    assert data["layout"] == {"a": [10, -4]}


def test_move_into_the_yaml_keeps_comments_and_writes_flow() -> None:
    text = "# Kopf\n" + BASE
    new = patch(text, layout.move(load_data(text), "z", 220, 0))
    assert new.startswith("# Kopf\n")
    assert "z: [220, 0]" in new
    assert model_from_yaml(new).layout["z"] == (220.0, 0.0)


def test_placed_keeps_stored_and_lays_out_the_rest() -> None:
    model = _model("layout:\n  a: [5, 7]\n")
    pos = layout.placed(model, positions(model, edges(model)))
    assert pos["a"] == (5.0, 7.0)
    assert pos["z"][0] > pos["a"][0] - 5  # a layer to the right of the auto origin


def test_arrange_sets_every_node_from_the_layered_layout() -> None:
    model = _model("layout:\n  a: [500, 500]\n")
    data = layout.arrange(load_data(BASE), positions(model, edges(model)))
    assert data["layout"] == {"a": [0, 0], "z": [layout.STEP_X, 0]}


def test_prune_drops_positions_of_unknown_nodes() -> None:
    data = load_data(BASE + "layout:\n  a: [1, 2]\n  gone: [3, 4]\n")
    assert layout.prune(data)["layout"] == {"a": [1, 2]}
    assert layout.unknown(data) == ["gone"]


def test_removing_a_node_removes_its_position() -> None:
    data = load_data(BASE + "layout:\n  a: [1, 2]\n  z: [3, 4]\n")
    data["nodes"]["z"]["expr"] = "1"
    assert form.remove_node(data, "a")["layout"] == {"z": [3, 4]}


@pytest.mark.parametrize(
    "name", ["t1_faltung", "t2_terminplan", "t3_bahn", "t4_portfolio", "t5_fusion"]
)
def test_every_tutorial_has_a_position_for_each_node(name: str) -> None:
    model = model_from_yaml(files.read_text(settings.examples_dir() / f"{name}.yaml"))
    assert set(model.layout) == set(model.nodes)
