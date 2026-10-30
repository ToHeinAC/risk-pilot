"""M9 AP4: the canvas on the model page: draw, move into the YAML, pick a node."""

from pathlib import Path

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
