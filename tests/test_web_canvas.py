"""M9 AP4: the canvas on the model page: draw, move into the YAML, pick a node."""

from pathlib import Path
from typing import Any

from nicegui.testing import User
from web_util import drive, element, open_model, put, until, value

from app.adapters import files, settings
from app.web.canvas import FlowCanvas

T2 = Path(__file__).resolve().parent.parent / "examples" / "t2_terminplan.yaml"


def _canvas(user: User) -> FlowCanvas:
    found = element(user, "canvas")
    assert isinstance(found, FlowCanvas)
    return found


def _x(user: User, node_id: str) -> float:
    return next(n["position"]["x"] for n in _canvas(user).props["nodes"] if n["id"] == node_id)


def test_moving_a_node_writes_its_position_and_keeps_the_view() -> None:
    files.copy_model(T2, settings.models_dir(), "plan")

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        canvas = _canvas(user)
        user.find(marker="canvas").trigger("move", {"id": "c", "x": 12.4, "y": 400})
        await user.should_see(marker="discard_model")
        assert "c: [12, 400]" in str(value(user, "editor"))
        assert _canvas(user) is canvas  # redrawn in place, the viewport stays
        assert _x(user, "c") == 12

    drive(steps)


def test_a_tutorial_is_drawn_but_not_moved() -> None:
    async def steps(user: User) -> None:
        await open_model(user, "t2_terminplan")
        assert _canvas(user).props["readonly"] is True
        user.find(marker="canvas").trigger("move", {"id": "c", "x": 1, "y": 1})
        assert _x(user, "c") == 0
        assert "c: [1, 1]" not in str(value(user, "editor"))

    drive(steps)


def test_arrange_lays_out_every_node_and_an_invalid_draft_is_still_drawn() -> None:
    files.copy_model(T2, settings.models_dir(), "plan")

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        user.find(marker="canvas").trigger("move", {"id": "ende", "x": 900, "y": 900})
        user.find(marker="canvas_arrange").click()
        assert "ende: [440, 165]" in str(value(user, "editor"))
        user.find(marker="canvas").trigger("pick", "pfad1")
        await user.should_see(marker="form.pfad1.expr")
        text = str(value(user, "editor")).replace('expr: "max(pfad1, c)"', 'expr: "max(pfad1, c"')
        put(user, "editor", text)  # invalid expression, readable YAML
        assert {n["id"] for n in _canvas(user).props["nodes"]} >= {"ende", "pfad1"}

    drive(steps)


def _plan() -> None:
    files.copy_model(T2, settings.models_dir(), "plan")


def test_connecting_opens_the_link_dialog_with_presets_and_writes_the_expression() -> None:
    _plan()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        assert _canvas(user).props["connectable"] is True
        user.find(marker="canvas").trigger("connect", {"source": "a", "target": "ende"})
        await user.should_see(marker="link_take")
        assert value(user, "link_preset") == "max"  # the current preset first
        await user.should_see("Projektende = Maximum aus Pfad 1, Vorgang C und Vorgang A")
        user.find(marker="link_take").click()
        await user.should_see(marker="form.ende.expr")
        assert 'expr: "max(pfad1, c, a)"' in str(value(user, "editor"))

    drive(steps)


def test_a_parameter_link_and_a_refused_cycle() -> None:
    _plan()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        user.find(marker="canvas").trigger("connect", {"source": "ende", "target": "a"})
        await user.should_see("ergäbe einen Kreis")
        user.find(marker="canvas").trigger("connect", {"source": "b", "target": "c"})
        await user.should_see(marker="link_take")
        put(user, "link_field", "sd")
        put(user, "link_value", "0.5")
        await user.should_see("sd von Vorgang C = Vorgang B × 0.5")
        user.find(marker="link_take").click()
        await user.should_see(marker="form.c.param.mean")
        assert "sd: b * 0.5" in str(value(user, "editor"))

    drive(steps)


def test_deleting_an_edge_removes_an_argument_or_opens_a_free_expression() -> None:
    _plan()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        user.find(marker="canvas").trigger("disconnect", "ausdruck:c->ende")
        await user.should_see(marker="discard_model")
        assert 'expr: "pfad1"' in str(value(user, "editor"))
        user.find(marker="canvas").trigger("disconnect", "ausdruck:nacharbeit->pfad1")
        await user.should_see("frei formuliert")
        await user.should_see(marker="form.pfad1.expr")
        assert "where(nacharbeit, 5, 0)" in str(value(user, "editor"))

    drive(steps)


def test_a_node_from_the_palette_lands_at_the_drop_point_with_a_suggested_id() -> None:
    _plan()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        user.find(marker="canvas").trigger("drop", {"type": "event", "x": 30, "y": 500})
        await user.should_see(marker="new_take")
        put(user, "new_name", "Lieferverzug Ä")
        await until(lambda: value(user, "new_id") == "lieferverzug_ae")
        put(user, "new_unit", "")
        user.find(marker="new_take").click()
        await user.should_see(marker="form.lieferverzug_ae.p")
        text = str(value(user, "editor"))
        assert "lieferverzug_ae: [30, 500]" in text
        assert 'name: "Lieferverzug Ä"' in text or "name: Lieferverzug Ä" in text

    drive(steps)


def _node(user: User, node_id: str) -> dict[str, Any]:
    return next(n for n in _canvas(user).props["nodes"] if n["id"] == node_id)


def test_in_a_scenario_the_structure_is_locked_and_changed_nodes_are_marked() -> None:
    _plan()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        put(user, "canvas_scenario", "nacharbeit")
        await until(lambda: _canvas(user).props["connectable"] is False)
        assert _canvas(user).props["palette"] == []
        assert _node(user, "nacharbeit")["data"]["badge"] == "1"
        assert "rp-changed" not in _node(user, "c")["class"]
        user.find(marker="canvas").trigger("connect", {"source": "a", "target": "ende"})
        await user.should_see("ist die Struktur gesperrt")
        put(user, "canvas_scenario", "basis")
        await until(lambda: _canvas(user).props["connectable"] is True)

    drive(steps)


def test_a_click_in_a_scenario_opens_the_override_dialog() -> None:
    _plan()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        put(user, "canvas_scenario", "nacharbeit")
        await until(lambda: _canvas(user).props["connectable"] is False)
        user.find(marker="canvas").trigger("pick", "c")
        await user.should_see(marker="ov_take")
        put(user, "ov_field", "mean")
        await user.should_see("Wert im Elternszenario: 24")
        put(user, "ov_value", "20")
        put(user, "ov_why", "Engpass")
        user.find(marker="ov_take").click()
        await until(lambda: _node(user, "c")["data"].get("badge") == "1")
        assert "c: {mean: 20, why: Engpass}" in str(value(user, "editor"))
        user.find(marker="canvas").trigger("pick", "nacharbeit")
        await user.should_see(marker="ov_remove")
        user.find(marker="ov_remove").click()
        await until(lambda: "badge" not in _node(user, "nacharbeit")["data"])

    drive(steps)


def test_a_new_sub_scenario_starts_from_the_selected_one() -> None:
    _plan()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        put(user, "canvas_scenario", "nacharbeit")
        user.find(marker="canvas_new_scenario").click()
        await user.should_see(marker="scen_take")
        put(user, "scen_name", "Schlimmer")
        await until(lambda: value(user, "scen_id") == "schlimmer")
        put(user, "scen_why", "Zweite Nacharbeit")
        user.find(marker="scen_take").click()
        await until(lambda: value(user, "canvas_scenario") == "schlimmer")
        assert "parent: nacharbeit" in str(value(user, "editor"))

    drive(steps)


def test_a_click_on_an_edge_changes_the_kind_or_removes_it() -> None:
    _plan()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        user.find(marker="canvas").trigger("edge", "ausdruck:c->ende")
        await user.should_see(marker="edge_take")
        assert value(user, "edge_preset") == "max"
        put(user, "edge_preset", "sum")
        await user.should_see("Projektende = Summe aus Pfad 1 und Vorgang C")
        user.find(marker="edge_take").click()
        await user.should_see(marker="form.ende.expr")
        assert 'expr: "pfad1 + c"' in str(value(user, "editor"))
        user.find(marker="canvas").trigger("edge", "ausdruck:c->ende")
        await user.should_see(marker="edge_remove")
        user.find(marker="edge_remove").click()
        await until(lambda: 'expr: "pfad1"' in str(value(user, "editor")))

    drive(steps)


def test_a_free_expression_edge_opens_the_card() -> None:
    _plan()

    async def steps(user: User) -> None:
        await open_model(user, "plan")
        user.find(marker="canvas").trigger("edge", "ausdruck:nacharbeit->pfad1")
        await user.should_see("frei formuliert")
        await user.should_see(marker="form.pfad1.expr")

    drive(steps)


CORR = """schema_version: 1
model: eigen
nodes:
  a: {type: uncertain, dist: normal, mean: 10, sd: 2}
  b: {type: uncertain, dist: normal, mean: 5, sd: 1}
  y: {type: output, expr: "a + b"}
correlations:
  a_b:
    nodes: [a, b]
    spearman: [[1.0, 0.3], [0.3, 1.0]]
"""


def test_a_correlation_edge_changes_rho() -> None:
    files.create_model_text(settings.models_dir(), "eigen", CORR)

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        user.find(marker="canvas").trigger("edge", "korrelation:a->b")
        await user.should_see(marker="edge_take")
        assert value(user, "edge_value") == "0.3"
        put(user, "edge_value", "0.6")
        await user.should_see("rangkorreliert mit ρ = 0.6")
        user.find(marker="edge_take").click()
        await until(lambda: "0.6" in str(value(user, "editor")))

    drive(steps)


def test_a_parameter_edge_opens_the_card_of_its_target() -> None:
    files.create_model_text(settings.models_dir(), "eigen", CORR.replace("mean: 5", 'mean: "a"'))

    async def steps(user: User) -> None:
        await open_model(user, "eigen")
        user.find(marker="canvas").trigger("edge", "parameter:a->b")
        await user.should_see("ein Parameter hängt von a ab")
        await user.should_see(marker="form.b.param.mean")

    drive(steps)
