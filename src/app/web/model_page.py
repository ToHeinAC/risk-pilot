"""Model page: workbench (form) and YAML editor on one draft, check, save, hints, copy."""

from pathlib import Path

from nicegui import ui

from app.adapters import files
from app.messages import t
from app.web import session as sessions
from app.web.editing import ModelEdit
from app.web.model_hints import Hints
from app.web.session import OpenModel, Session
from app.web.workbench import Workbench


class ModelPage:
    def __init__(self, model: OpenModel) -> None:
        self.model = model
        self.path = Path(model.path)
        self.edit = ModelEdit(model)
        self.hints = Hints(self.edit, self.changed)
        self.workbench = Workbench(self.edit, self.changed)
        self.conflict = False
        self.save_note: tuple[str, str] | None = None  # (text, colour class)
        self.editor: ui.codemirror | None = None

    def changed(self, card: bool) -> None:
        """The form or a hint changed the draft: everything but the field in use redraws."""
        self.workbench.refresh(card)
        self.after_change()
        if self.editor is not None:
            self.editor.value = self.edit.text  # its change event finds nothing new

    def yaml_changed(self, text: str) -> None:
        if text == self.edit.text:
            return
        readable = self.edit.data() is not None
        self.edit.set_text(text)
        if readable and self.edit.data() is not None:
            self.workbench.refresh(card=True)
        else:
            self.form.refresh()  # the form locks or unlocks with the YAML's readability
        self.after_change()

    def after_change(self) -> None:
        self.save_note = None
        for part in (self.bar, self.check, self.hints.build):
            part.refresh()

    @ui.refreshable_method
    def bar(self) -> None:
        if self.model.dirty:
            ui.badge(t("ui.unsaved"), color="warning").props("outline")
        if self.model.readonly:
            ui.badge(t("ui.readonly"), color="grey-7").props("outline")
            return
        ui.button(t("ui.save"), icon="save", on_click=lambda: self.save(False)).props(
            "unelevated no-caps"
        ).mark("save_model")
        if self.conflict:
            ui.button(t("ui.save_force"), on_click=lambda: self.save(True)).props(
                "outline no-caps color=negative"
            ).mark("save_force")
        ui.button(t("ui.discard"), on_click=self.discard).props("flat no-caps").mark(
            "discard_model"
        )
        if self.save_note is not None:
            ui.label(self.save_note[0]).classes(self.save_note[1])

    def save(self, force: bool) -> None:
        refused = sessions.save(self.model, force)
        self.conflict = refused is not None
        if refused is not None:
            self.save_note = (refused, "text-negative")
        elif self.edit.checked().rows:
            self.save_note = (t("ui.saved_invalid"), "text-warning")
        else:
            self.save_note = (t("ui.saved"), "text-positive")
        self.bar.refresh()

    def discard(self) -> None:
        self.edit.discard(files.read_text(self.path))
        self.conflict = False
        self.changed(card=True)

    @ui.refreshable_method
    def check(self) -> None:
        result = self.edit.checked()
        if result.hint:
            ui.label(result.hint).classes("rp-muted")
        elif result.rows:
            ui.label(result.status).classes("text-negative font-semibold")
            for row in result.rows:
                where = t("ui.at_line", line=row.line) if row.line else ""
                ui.label(f"{row.message}{where}").classes("text-negative")
                if row.excerpt:
                    ui.label(row.excerpt).classes("font-mono text-xs rp-muted")
        else:
            with ui.row().classes("items-center gap-2"):
                ui.icon("check_circle", color="positive")
                ui.label(result.status).classes("text-positive")
                if self.edit.trial_ms is not None:
                    ui.label(t("web.trial", ms=f"{self.edit.trial_ms:.0f}")).classes(
                        "rp-muted text-sm"
                    )

    @ui.refreshable_method
    def form(self) -> None:
        self.workbench.build()

    def yaml(self) -> None:
        editor = ui.codemirror(self.edit.text, language="YAML", on_change=self._typed)
        editor.classes("w-full h-[560px] rp-panel").mark("editor")
        editor.set_enabled(not self.model.readonly)
        self.editor = editor

    def _typed(self, e: object) -> None:
        self.yaml_changed(str(getattr(e, "value", "") or ""))

    def copy(self) -> None:
        with ui.expansion(t("ui.copy"), value=self.model.readonly).classes("rp-panel w-full"):
            name = ui.input(t("ui.copy_name"), value=sessions.free_copy_id(self.path))
            name.props("dense outlined").mark("copy_id_modell")
            note = ui.label()

            def copy() -> None:
                note.text = sessions.copy_as(self.path, str(name.value or ""))[1]

            ui.button(t("ui.copy"), on_click=copy).props("flat no-caps").mark("copy_modell")

    def build(self) -> None:
        with ui.row().classes("w-full items-center gap-3"):
            ui.label(self.path.name).classes("rp-muted font-mono")
            ui.space()
            self.bar()
        explanation = self.path.with_suffix(".md")
        if explanation.is_file():
            with ui.expansion(t("ui.explanation")).classes("rp-panel w-full"):
                ui.markdown(files.read_text(explanation))
        with ui.column().classes("w-full gap-1"):
            self.check()
        with ui.tabs().classes("w-full justify-start").props("dense no-caps align=left") as tabs:
            form_tab = ui.tab(t("model.tab_form"))
            yaml_tab = ui.tab(t("model.tab_yaml"))
        with ui.tab_panels(tabs, value=form_tab).classes("w-full bg-transparent"):
            with ui.tab_panel(form_tab).classes("p-0 gap-4"):
                self.form()
            with ui.tab_panel(yaml_tab).classes("p-0"):
                self.yaml()
        with ui.column().classes("w-full gap-2"):
            self.hints.build()
        self.copy()
        ui.button(t("ui.to_simulation"), on_click=lambda: ui.navigate.to("/simulation")).props(
            "flat no-caps icon-right=arrow_forward"
        )


def page(session: Session) -> None:
    if session.model is None:
        ui.label(t("ui.no_model")).classes("rp-muted")
        ui.button(t("ui.page_start"), on_click=lambda: ui.navigate.to("/")).props("flat no-caps")
        return
    ModelPage(session.model).build()
