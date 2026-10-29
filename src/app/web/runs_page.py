"""Stored runs: list them, load one; the loaded run becomes the current run."""

from functools import partial
from pathlib import Path

from nicegui import ui

from app.adapters import runs, settings
from app.errors import ModelError
from app.messages import t
from app.model.yaml_io import model_from_yaml
from app.web import results_view, running
from app.web.session import Session


def _model_id(session: Session) -> str | None:
    if session.model is None:
        return None
    try:
        return model_from_yaml(session.model.text).model
    except ModelError:
        return None


class RunsPage:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.message = ""
        self.loaded = False

    def load(self, path: Path) -> None:
        try:
            self.session.run = running.load(path)
        except Exception as exc:  # a broken folder must not break the page
            self.message = t("ui.unexpected", detail=f"{type(exc).__name__}: {exc}")
            self.loaded = False
        else:
            self.message, self.loaded = "", True
        self.body.refresh()

    @ui.refreshable_method
    def body(self) -> None:
        found = runs.list_runs(settings.runs_dir(), _model_id(self.session))
        if not found:
            ui.label(t("ui.no_runs")).classes("rp-muted")
            return
        with ui.row().classes("gap-2"):
            for index, path in enumerate(found):
                ui.button(path.name, icon="history", on_click=partial(self.load, path)).props(
                    "outline no-caps"
                ).mark(f"load_run_{index}")
        if self.message:
            ui.label(self.message).classes("text-negative")
        if self.loaded and self.session.run is not None:
            results_view.show(self.session.run)


def page(session: Session) -> None:
    RunsPage(session).body()
