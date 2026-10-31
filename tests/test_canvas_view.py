"""M9 AP4: what the canvas draws, built from the raw draft (pure)."""

from typing import Any

import yaml

from app.adapters import files, settings
from app.messages import t
from app.model import layout, scenarios
from app.model.yaml_io import model_from_yaml
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


def test_the_link_dialog_says_the_result_in_plain_words() -> None:
    from app.model import canvas

    data = {**T2, "nodes": {**T2["nodes"], "ende": {**T2["nodes"]["ende"], "expr": "pfad1"}}}
    after = canvas.connect(data, "c", "ende", "max")
    assert canvas_view.describe(after, "c", "ende", "max", "") == (
        "Projektende = Maximum aus Pfad 1 und Vorgang C"
    )
    assert canvas_view.describe(after, "nacharbeit", "pfad1", "delay", "5") == (
        "Pfad 1 wird um 5 größer, wenn Nacharbeit an B eintritt"
    )
    assert canvas_view.describe(after, "a", "b", "param", "0.5", field="sd") == (
        "sd von Vorgang B = Vorgang A × 0.5"
    )
    assert canvas_view.describe(after, "a", "nacharbeit", "p", "") == (
        "Nacharbeit an B tritt mit Wahrscheinlichkeit Vorgang A ein"
    )
    assert canvas_view.describe(after, "a", "c", "corr", "0.3") == (
        "Vorgang A und Vorgang C sind rangkorreliert mit ρ = 0.3"
    )


def test_changed_nodes_are_marked_with_their_count() -> None:
    nodes, _ = canvas_view.view(T2, selected=None, marks={"b": 2})
    by_id = {n["id"]: n for n in nodes}
    assert "rp-changed" in by_id["b"]["class"]
    assert by_id["b"]["data"]["badge"] == "2"
    assert "badge" not in by_id["a"]["data"]


def test_the_analysis_graph_shows_each_value_and_fades_nodes_off_the_path() -> None:
    data = {**T2, "nodes": {**T2["nodes"], "extra": {"type": "constant", "value": 1}}}
    nodes, edges = canvas_view.analysis_view(data, {"a": 0.62, "b": 0.0}, "ende")
    by_id = {n["id"]: n for n in nodes}
    assert by_id["a"]["data"]["badge"] == "0,62"
    assert by_id["a"]["data"]["tint"].startswith("rgb")
    assert "badge" not in by_id["c"]["data"]
    assert "rp-faded" in by_id["extra"]["class"]
    assert "rp-faded" not in by_id["a"]["class"]
    assert edges


def _with_scenario(overrides: dict[str, Any]) -> dict[str, Any]:
    scenario = {"name": "Nur Pfad 2", "why": "Test", "overrides": overrides}
    return {**T2, "scenarios": {**T2["scenarios"], "nur_c": scenario}}


def test_a_scenario_is_drawn_with_its_own_expressions_and_unused_nodes_fade() -> None:
    data = _with_scenario({"ende": {"expr": "c"}})
    model = model_from_yaml(yaml.safe_dump(data, allow_unicode=True))
    nodes, edges = canvas_view.view({**data, **scenarios.effective_data(model, "nur_c")}, None)
    ids = {e["id"] for e in edges}
    assert "ausdruck:c->ende" in ids
    assert "ausdruck:pfad1->ende" not in ids
    by_id = {n["id"]: n for n in nodes}
    assert "rp-faded" in by_id["pfad1"]["class"]
    assert "rp-faded" in by_id["a"]["class"]
    assert "rp-faded" not in by_id["c"]["class"]
    base, _ = canvas_view.view(T2, None)
    assert not any("rp-faded" in n["class"] for n in base)


def test_a_node_hint_says_what_it_is_or_that_it_counts_nowhere() -> None:
    a = {**T2["nodes"]["a"], "description": "Rohbau bis Decke EG"}
    data = {**T2, "nodes": {**T2["nodes"], "a": a, "extra": {"type": "constant", "value": 1}}}
    by_id = {n["id"]: n for n in canvas_view.view(data, None)[0]}
    assert by_id["a"]["data"]["hint"] == "Rohbau bis Decke EG"
    assert by_id["extra"]["data"]["hint"] == t("canvas.unused")
    assert "hint" not in by_id["b"]["data"]
