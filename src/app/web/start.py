"""Start page: learning path, tutorials, own models (open, copy as template, new)."""

import functools
from collections.abc import Callable
from pathlib import Path

from nicegui import ui

from app.adapters import files, settings
from app.errors import InputError, ModelError
from app.messages import render, t
from app.web import session as sessions
from app.web.session import Session


def _title(path: Path) -> str:
    try:
        return _title_of(path, path.stat().st_mtime_ns)
    except OSError:
        return path.stem


@functools.lru_cache(maxsize=256)
def _title_of(path: Path, _mtime: int) -> str:
    """The model's title; cached per file version (the start page lists every model)."""
    try:
        model = files.load_model(path)
    except (ModelError, OSError, UnicodeDecodeError):
        return path.stem
    return model.title or model.model


class StartPage:
    def __init__(self, session: Session) -> None:
        self.session = session

    def opener(self, path: Path) -> Callable[[], None]:
        def open_it() -> None:
            sessions.open_model(self.session, path)
            ui.navigate.to("/modell")

        return open_it

    def card(self, path: Path) -> None:
        with ui.card().classes("rp-panel w-80 gap-2 p-4").props("flat"):
            ui.label(_title(path)).classes("font-semibold")
            ui.label(path.stem).classes("rp-muted text-xs font-mono")
            ui.button(t("ui.open"), on_click=self.opener(path)).props("unelevated no-caps").mark(
                f"open_{path.stem}"
            )
            self.copy_row(path, path.stem)

    def copy_row(self, path: Path, key: str) -> None:
        name = ui.input(t("ui.copy_name"), value=sessions.free_copy_id(path)).props(
            "dense outlined"
        )
        name.classes("w-full").mark(f"copy_id_{key}")
        note = ui.label().classes("text-sm")

        def copy() -> None:
            done, message = sessions.copy_as(path, str(name.value or ""))
            note.text = message
            note.classes(replace="text-sm " + ("text-positive" if done else "text-negative"))
            if done:
                self.own.refresh()

        ui.button(t("ui.copy"), on_click=copy).props("flat dense no-caps").mark(f"copy_{key}")

    def new_model(self) -> None:
        with ui.row().classes("items-start gap-2"):
            new_id = ui.input(t("ui.new_model_id")).props("dense outlined").mark("new_model_id")
            error = ui.label().classes("text-negative text-sm")

            def create() -> None:
                text = f"schema_version: 1\nmodel: {new_id.value}\nnodes: {{}}\n"
                try:
                    path = files.create_model_text(
                        settings.models_dir(), str(new_id.value or "").strip(), text
                    )
                except InputError as exc:
                    error.text = render(exc.issue)
                    return
                self.opener(path)()

            ui.button(t("ui.new_model_create"), on_click=create).props("unelevated no-caps").mark(
                "new_model_create"
            )

    @ui.refreshable_method
    def own(self) -> None:
        paths = files.list_models(settings.models_dir())
        if not paths:
            ui.label(t("ui.no_own_models")).classes("rp-muted")
        with ui.row().classes("gap-4"):
            for path in paths:
                self.card(path)


def page(session: Session) -> None:
    start = StartPage(session)
    with ui.column().classes("rp-panel p-4 gap-2 w-full"):
        ui.label(t("ui.page_lernpfad")).classes("text-lg font-semibold")
        ui.label(t("ui.lernpfad_intro")).classes("rp-muted")
        ui.button(t("ui.open_lernpfad"), on_click=lambda: ui.navigate.to("/lernpfad")).props(
            "flat no-caps"
        ).mark("open_lernpfad")
    ui.label(t("ui.tutorials")).classes("text-lg font-semibold")
    with ui.row().classes("gap-4"):
        for tutorial in sorted(settings.examples_dir().glob("t*.yaml")):
            start.card(tutorial)
    ui.label(t("ui.own_models")).classes("text-lg font-semibold")
    ui.label(t("ui.new_model")).classes("rp-kicker")
    start.new_model()
    start.own()
