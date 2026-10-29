"""Evaluation block (M8 AK 2): question, reading example, chart, then reading and limit."""

from collections.abc import Callable

from nicegui import ui

from app.messages import t
from app.present.reading import Empty, Reading, Sentence


def reading(key: str, found: Reading) -> bool:
    """The reading example, or the reason the evaluation stays empty; True if there is a result."""
    if isinstance(found, Sentence):
        ui.label(found.text).classes("rp-answer").mark(f"reading_{key}")
        return True
    assert isinstance(found, Empty)
    ui.label(found.reason).classes("rp-muted").mark(f"empty_{key}")
    return False


def block(key: str, found: Reading | None, draw: Callable[[], None]) -> None:
    """``found`` None: the reading follows from a run inside ``draw`` (tornado, sweep)."""
    ui.label(t(f"explain.{key}.question")).classes("text-lg font-semibold")
    if found is None or reading(key, found):
        draw()
    with ui.expansion(t("explain.how_label"), icon="help_outline").classes("rp-panel w-full"):
        ui.markdown(t(f"explain.{key}.how")).classes("px-4")
