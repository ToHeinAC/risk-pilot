"""Dialogs of the canvas (M9 AP5): link with presets, new node from the palette.

Both compute the change with the pure canvas actions, show it before it is taken and write it
through ``ModelEdit.change``; a refused change stays in the dialog with its message.
"""

from collections.abc import Callable
from typing import Any

from nicegui import ui

from app.errors import InputError
from app.messages import render, t
from app.model import canvas, form
from app.model.yaml_patch import Data
from app.present import canvas_view
from app.web.editing import ModelEdit

Done = Callable[[str], None]  # the node to select after the change
VALUE_LABEL = {"param": "canvas.factor", "delay": "canvas.delay", "corr": "canvas.rho_label"}


def _changed(before: Data, after: Data, target: str) -> list[str]:
    """Changed fields of ``target`` in model language: ``ende.expr: max(a, b)``."""
    old: dict[str, Any] = before["nodes"][target]
    new: dict[str, Any] = after["nodes"][target]
    return [f"{target}.{k}: {v}" for k, v in new.items() if old.get(k) != v]


class Link:
    """Connect ``source`` to ``target``: preset, its field or value, plain words, then take."""

    def __init__(self, edit: ModelEdit, source: str, target: str, done: Done) -> None:
        self.edit, self.source, self.target, self.done = edit, source, target, done
        self.data = edit.data() or {}
        self.names = (canvas_view.name(self.data, source), canvas_view.name(self.data, target))

    def open(self, offered: list[str]) -> None:
        params = (
            [s.name for s in form.param_fields(self.data, self.target)]
            if "param" in offered
            else []
        )
        with ui.dialog() as self.dialog, ui.card().classes("min-w-[28rem] gap-3"):
            ui.label(" → ".join(self.names)).classes("text-lg font-semibold")
            options = {p: t(f"canvas.preset_{p}") for p in offered}
            self.preset = ui.select(options, value=offered[0], label=t("canvas.preset"))
            self.preset.props("outlined dense").mark("link_preset")
            self.field = ui.select(params, value=(params or [None])[0], label=t("canvas.field"))
            self.field.props("outlined dense").mark("link_field")
            self.field.bind_visibility_from(self.preset, "value", lambda v: v == "param")
            self.amount = ui.input(t("canvas.factor")).props("outlined dense").mark("link_value")
            self.amount.bind_visibility_from(self.preset, "value", lambda v: v in VALUE_LABEL)
            self.says = ui.label().classes("font-medium").mark("link_preview")
            self.code = ui.label().classes("font-mono text-sm rp-muted")
            with ui.row().classes("w-full justify-end gap-2"):
                ui.button(t("canvas.cancel"), on_click=self.dialog.close).props("flat no-caps")
                self.take = ui.button(t("canvas.take"), on_click=self.apply)
                self.take.props("unelevated no-caps").mark("link_take")
            for part in (self.preset, self.field, self.amount):
                part.on_value_change(self.show)
            self.show()
        self.dialog.open()

    def args(self) -> tuple[str, str, str]:
        return str(self.preset.value), str(self.field.value or ""), str(self.amount.value or "")

    def show(self) -> None:
        p, f, v = self.args()
        self.amount.label = t(VALUE_LABEL.get(p, "canvas.factor"))
        self.take.text = t("canvas.open_expr" if p == "edit" else "canvas.take")
        self.take.enable()
        if p == "edit":
            names = {"source": self.names[0], "target": self.names[1]}
            self.says.text, self.code.text = t("canvas.says_edit", **names), ""
            return
        try:
            after = canvas.connect(self.data, self.source, self.target, p, field=f, value=v)
        except InputError as exc:
            self.says.text, self.code.text = render(exc.issue), ""
            self.take.disable()
            return
        self.says.text = canvas_view.describe(after, self.source, self.target, p, v, field=f)
        changed = _changed(self.data, after, self.target) if p != "corr" else []
        self.code.text = "  ".join(changed)

    def apply(self) -> None:
        p, f, v = self.args()
        source, target = self.source, self.target
        if p == "edit" or self.edit.change(
            lambda d: canvas.connect(d, source, target, p, field=f, value=v)
        ):
            self.dialog.close()
            self.done(target)
        else:
            self.says.text = self.edit.error or ""


def link(edit: ModelEdit, source: str, target: str, offered: list[str], done: Done) -> None:
    Link(edit, source, target, done).open(offered)


class Edge:
    """A clicked edge: another kind for a preset expression, another ρ for a correlation, or
    remove it. Free expressions and parameters are not offered here (the card opens)."""

    def __init__(self, edit: ModelEdit, source: str, target: str, kind: str, done: Done) -> None:
        self.edit, self.source, self.target, self.kind, self.done = edit, source, target, kind, done
        self.data = edit.data() or {}
        self.names = (canvas_view.name(self.data, source), canvas_view.name(self.data, target))

    def open(self) -> None:
        with ui.dialog() as self.dialog, ui.card().classes("min-w-[28rem] gap-3"):
            title = t("canvas.edge_title", source=self.names[0], target=self.names[1])
            ui.label(title).classes("text-lg font-semibold")
            self.preset = self.value = None
            if self.kind == "korrelation":
                rho = canvas.rho(self.data, self.source, self.target)
                self.value = ui.input(
                    t("canvas.rho_label"), value=f"{rho:g}" if rho is not None else ""
                )
                self.value.props("outlined dense").mark("edge_value")
            else:
                expr = str(self.data["nodes"][self.target].get("expr", ""))
                current = canvas.shape(expr).preset
                order = sorted(canvas.JOINS, key=lambda p: p != current)
                options = {p: t(f"canvas.preset_{p}") for p in order}
                self.preset = ui.select(options, value=order[0], label=t("canvas.preset"))
                self.preset.props("outlined dense").mark("edge_preset")
            self.says = ui.label().classes("font-medium")
            self.code = ui.label().classes("font-mono text-sm rp-muted")
            with ui.row().classes("w-full justify-end gap-2"):
                ui.button(t("canvas.edge_remove"), on_click=self.remove).props(
                    "flat no-caps color=negative"
                ).mark("edge_remove")
                ui.button(t("canvas.cancel"), on_click=self.dialog.close).props("flat no-caps")
                self.take = ui.button(t("canvas.take"), on_click=self.apply)
                self.take.props("unelevated no-caps").mark("edge_take")
            for part in (self.preset, self.value):
                if part is not None:
                    part.on_value_change(self.show)
            self.show()
        self.dialog.open()

    def change(self, data: Data) -> Data:
        if self.value is not None:
            return canvas.connect(
                data, self.source, self.target, "corr", value=str(self.value.value or "")
            )
        return canvas.retype(data, self.target, str(self.preset.value if self.preset else ""))

    def show(self) -> None:
        try:
            after = self.change(self.data)
        except InputError as exc:
            self.says.text, self.code.text = render(exc.issue), ""
            self.take.disable()
            return
        self.take.enable()
        preset = "corr" if self.value is not None else str(self.preset.value if self.preset else "")
        amount = str(self.value.value or "") if self.value is not None else ""
        self.says.text = canvas_view.describe(after, self.source, self.target, preset, amount)
        self.code.text = (
            "  ".join(_changed(self.data, after, self.target)) if self.value is None else ""
        )

    def finish(self, change: Callable[[Data], Data]) -> None:
        if self.edit.change(change):
            self.dialog.close()
            self.done(self.target)
        else:
            self.says.text = self.edit.error or ""

    def apply(self) -> None:
        self.finish(self.change)

    def remove(self) -> None:
        source, target = self.source, self.target
        action = canvas.uncorrelate if self.kind == "korrelation" else canvas.disconnect
        self.finish(lambda d: action(d, source, target))


def edge(edit: ModelEdit, source: str, target: str, kind: str, done: Done) -> None:
    Edge(edit, source, target, kind, done).open()


def new_node(edit: ModelEdit, node_type: str, x: float, y: float, done: Done) -> None:
    """A palette item placed: name, ID (suggested from the name), unit."""
    taken = edit.node_ids()
    with ui.dialog() as dialog, ui.card().classes("min-w-[24rem] gap-3"):
        ui.label(t("canvas.new_title", type=t(f"type.{node_type}"))).classes(
            "text-lg font-semibold"
        )
        name = ui.input(t("form.f_name")).props("outlined dense autofocus").mark("new_name")
        node_id = ui.input(t("canvas.new_id"), value=canvas.suggest_id("", taken))
        node_id.props("outlined dense").mark("new_id")
        unit = ui.input(t("form.f_unit")).props("outlined dense").mark("new_unit")
        error = ui.label().classes("text-negative")
        name.on_value_change(lambda e: node_id.set_value(canvas.suggest_id(str(e.value), taken)))

        def apply() -> None:
            new = str(node_id.value or "").strip()
            label, u = str(name.value or ""), str(unit.value or "")
            if edit.change(lambda d: canvas.place(d, new, node_type, label, u, x, y)):
                dialog.close()
                done(new)
            else:
                error.text = edit.error or ""

        with ui.row().classes("w-full justify-end gap-2"):
            ui.button(t("canvas.cancel"), on_click=dialog.close).props("flat no-caps")
            ui.button(t("canvas.create"), on_click=apply).props("unelevated no-caps").mark(
                "new_take"
            )
    dialog.open()
