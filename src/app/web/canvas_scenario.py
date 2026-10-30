"""Scenario dialogs of the canvas (M9 AP6): override one node, derive a new sub-scenario.

Changes go through ``scenario_edit.apply`` like on the scenario page: kept only if the model
stays valid, otherwise the dialog shows why.
"""

from collections.abc import Callable
from typing import Any

import yaml
from nicegui import ui

from app.messages import t
from app.model import canvas
from app.model import scenarios as sc
from app.model.schema import Model
from app.web import scenario_edit
from app.web.editing import ModelEdit

Done = Callable[[str], None]


def _write(edit: ModelEdit, change: Callable[[Model], Model]) -> str | None:
    """Apply ``change`` to the draft; the reason if it was refused."""
    text, refused = scenario_edit.apply(edit.text, change)
    if refused is None:
        edit.set_text(text)
    return refused


def _shown(value: Any) -> str:
    if value is None:
        return "–"
    return (
        yaml.safe_dump(value, default_flow_style=True, allow_unicode=True)
        .strip()
        .removesuffix("\n...")
    )


class Override:
    """Override one field of ``node`` in ``sid``: field, parent value, new value, reason."""

    def __init__(self, edit: ModelEdit, sid: str, node: str, done: Done) -> None:
        self.edit, self.sid, self.node, self.done = edit, sid, node, done
        model = edit.checked().model
        assert model is not None  # scenarios exist only on a valid model
        self.model = model
        self.own: dict[str, Any] = dict(model.scenarios[sid].overrides.get(node, {}))

    def open(self) -> None:
        fields = sc.overridable(self.model, self.sid, self.node)
        first = next((f for f in fields if f in self.own), fields[0])
        with ui.dialog() as self.dialog, ui.card().classes("min-w-[28rem] gap-3"):
            title = t("canvas.override_title", node=self.node, scenario=self.sid)
            ui.label(title).classes("text-lg font-semibold")
            self.field = ui.select(fields, value=first, label=t("scen.col_field"))
            self.field.props("outlined dense").mark("ov_field")
            self.parent = ui.label().classes("rp-muted")
            self.value = ui.input(t("scen.value_hint")).props("outlined dense").mark("ov_value")
            why = self.own.get("why") or ""
            self.why = ui.input(t("scen.col_why"), value=why).props("outlined dense")
            self.why.mark("ov_why")
            self.error = ui.label().classes("text-negative")
            with ui.row().classes("w-full justify-end gap-2"):
                self.remove = ui.button(t("canvas.override_remove"), on_click=self.drop)
                self.remove.props("flat no-caps color=negative").mark("ov_remove")
                ui.button(t("canvas.cancel"), on_click=self.dialog.close).props("flat no-caps")
                ui.button(t("canvas.take"), on_click=self.take).props("unelevated no-caps").mark(
                    "ov_take"
                )
            self.field.on_value_change(self.show)
            self.show()
        self.dialog.open()

    def show(self) -> None:
        name = str(self.field.value)
        before = sc.parent_value(self.model, self.sid, self.node, name)
        self.parent.text = t("canvas.parent_value", value=_shown(before))
        self.value.value = _shown(self.own[name]) if name in self.own else ""
        self.remove.set_visibility(name in self.own)

    def finish(self, refused: str | None) -> None:
        if refused is not None:
            self.error.text = refused
            return
        self.dialog.close()
        self.done(self.node)

    def take(self) -> None:
        text = str(self.value.value or "").strip()
        new = yaml.safe_load(text) if text else None
        if new is None:
            self.error.text = t("scen.value_missing")
            return
        sid, node, name = self.sid, self.node, str(self.field.value)
        why = str(self.why.value or "").strip() or None
        self.finish(_write(self.edit, lambda m: sc.set_override(m, sid, node, name, new, why)))

    def drop(self) -> None:
        sid, node, name = self.sid, self.node, str(self.field.value)
        self.finish(_write(self.edit, lambda m: sc.remove_override(m, sid, node, name)))


def override(edit: ModelEdit, sid: str, node: str, done: Done) -> None:
    Override(edit, sid, node, done).open()


def new_scenario(edit: ModelEdit, parent: str, done: Done) -> None:
    """A sub-scenario of ``parent``: name, ID (suggested from the name), reason."""
    model = edit.checked().model
    taken = list(model.scenarios) if model is not None else []
    with ui.dialog() as dialog, ui.card().classes("min-w-[24rem] gap-3"):
        ui.label(t("canvas.new_scenario_title", parent=parent)).classes("text-lg font-semibold")
        name = ui.input(t("form.f_name")).props("outlined dense autofocus").mark("scen_name")
        sid = ui.input(t("canvas.new_id"), value="").props("outlined dense").mark("scen_id")
        why = ui.input(t("scen.col_why")).props("outlined dense").mark("scen_why")
        error = ui.label().classes("text-negative")
        name.on_value_change(lambda e: sid.set_value(canvas.suggest_id(str(e.value), taken)))

        def take() -> None:
            new, label, reason = (str(x.value or "").strip() for x in (sid, name, why))
            refused = _write(edit, lambda m: sc.add_scenario(m, new, label, parent, reason))
            if refused is not None:
                error.text = refused
                return
            dialog.close()
            done(new)

        with ui.row().classes("w-full justify-end gap-2"):
            ui.button(t("canvas.cancel"), on_click=dialog.close).props("flat no-caps")
            ui.button(t("canvas.create"), on_click=take).props("unelevated no-caps").mark(
                "scen_take"
            )
    dialog.open()
