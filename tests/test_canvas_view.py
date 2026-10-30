"""M9 AP4: what the canvas draws, built from the raw draft (pure)."""

from app.adapters import files, settings
from app.model import layout
from app.model.yaml_patch import load_data
from app.present import canvas_view

T2 = load_data(files.read_text(settings.examples_dir() / "t2_terminplan.yaml"))


def test_every_node_is_drawn_at_its_stored_position_with_name_and_type() -> None:
    nodes, _ = canvas_view.view(T2, selected="b")
    by_id = {n["id"]: n for n in nodes}
    assert list(by_id) == ["a", "b", "c", "nacharbeit", "pfad1", "ende"]
    assert by_id["pfad1"]["position"] == {"x": 220.0, "y": 165.0}
    assert by_id["a"]["data"] == {"label": "Vorgang A", "type": "Unsicher"}
    assert "rp-uncertain" in by_id["a"]["class"]
    assert "rp-selected" in by_id["b"]["class"]
    assert "rp-selected" not in by_id["a"]["class"]
    assert by_id["a"]["sourcePosition"] == "right"


def test_a_node_without_position_is_laid_out_automatically() -> None:
    data = {**T2, "layout": {}}
    nodes, _ = canvas_view.view(data, selected=None)
    by_id = {n["id"]: n["position"] for n in nodes}
    assert by_id["a"] == {"x": 0.0, "y": 0.0}
    assert by_id["ende"]["x"] == 2 * layout.STEP_X


def test_edges_carry_their_kind_and_correlations_have_no_arrow() -> None:
    data = {
        **T2,
        "correlations": {"g": {"nodes": ["a", "c"], "spearman": [[1, 0.3], [0.3, 1]]}},
    }
    _, edges = canvas_view.view(data, selected=None)
    by_id = {e["id"]: e for e in edges}
    assert by_id["ausdruck:a->pfad1"]["class"] == "rp-edge-ausdruck"
    assert by_id["ausdruck:a->pfad1"]["markerEnd"] == "arrowclosed"
    assert by_id["ausdruck:nacharbeit->pfad1"]["source"] == "nacharbeit"
    assert "markerEnd" not in by_id["korrelation:a->c"]


def test_an_edge_id_reads_back() -> None:
    assert canvas_view.edge_of("parameter:a->b") == ("a", "b", "parameter")
    assert canvas_view.edge_of("nonsense") is None
