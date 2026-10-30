"""M9 AP4: the canvas on the model page: draw, move into the YAML, pick a node."""

from pathlib import Path

from nicegui.testing import User
from web_util import drive, element, open_model, put, value

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
