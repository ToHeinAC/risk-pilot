"""The card of one node (M6 form fields, M7 look): fields by type, delete, preview."""

# plotly ships without type stubs; its members are untyped for pyright.
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false
from collections.abc import Callable
from typing import Any

from nicegui import ui

from app.dists.registry import families, get_family
from app.messages import t
from app.model import form
from app.model.yaml_patch import Data
from app.present import preview as previews
from app.present import structure
from app.web import theme
from app.web.editing import ModelEdit

SELECTS: dict[str, tuple[str, ...]] = {
    "target_op": ("", *form.TARGET_OPS),
    "better": ("", "lower", "higher"),
}
AREAS = ("description", "why", "expr", "options")
FIRST = ("name", "unit")
LAST = ("description", "why", "tags", "bounds_min", "bounds_max", "track")
DEBOUNCE = "debounce=400"


def text_field(label: str, value: str, put: Callable[[str], None], marker: str) -> ui.input:
    field = ui.input(label, value=value, on_change=lambda e: put(str(e.value or "")))
    return field.props(f"{DEBOUNCE} dense outlined").classes("flex-1 min-w-40").mark(marker)


def options_text(rows: list[tuple[str, str]]) -> str:
    return "\n".join(f"{label}: {weight}" for label, weight in rows)


def options_rows(text: str) -> list[tuple[str, str]]:
    rows = [line.rpartition(":") for line in text.splitlines() if line.strip()]
    return [
        (label.strip(), weight.strip()) if sep else (weight.strip(), "")
        for label, sep, weight in rows
    ]


def dist_choices(current: str) -> list[str]:
    known = families()
    return known if current in known else [current, *known]  # "" while none is chosen


def mode_choices(dist: str) -> list[str]:
    family = get_family(dist)
    return list(family.modes) if family else ["params"]


def _label(field: str) -> str:
    return field.removeprefix("param.") if field.startswith("param.") else t(f"form.f_{field}")


class NodeCard:
    def __init__(self, edit: ModelEdit, node_id: str, changed: Callable[[bool], None]) -> None:
        self.edit = edit
        self.node_id = node_id
        self.changed = changed
        self.readonly = edit.model.readonly

    def put(self, field: str) -> Callable[[Any], None]:
        def set_value(value: Any) -> None:
            new = options_rows(str(value)) if field == "options" else value
            node_id = self.node_id
            self.edit.change(
                lambda d: form.apply(d, node_id, {**form.values(d, node_id), field: new})
            )
            self.changed(False)

        return set_value

    def set_dist(self, dist: str, mode: str) -> None:
        modes = mode_choices(dist)
        node_id = self.node_id
        self.edit.change(
            lambda d: form.set_dist(d, node_id, dist, mode if mode in modes else modes[0])
        )
        self.changed(True)  # the parameter fields change with the family

    def select(self, field: str, value: Any, values: dict[str, Any]) -> None:
        marker = f"form.{self.node_id}.{field}"
        if field in ("dist", "input"):
            dist = str(values.get("dist", ""))
            choices = dist_choices(str(value)) if field == "dist" else mode_choices(dist)
            mode = str(values.get("input") or "params")

            def changed(new: Any) -> None:
                if field == "dist":
                    self.set_dist(str(new), mode)
                else:
                    self.set_dist(dist, str(new))

            on_change: Callable[[Any], None] = changed
        else:
            choices = list(SELECTS[field])
            on_change = self.put(field)
        box = ui.select(
            choices, value=value if value in choices else choices[0], label=_label(field)
        )
        box.on_value_change(lambda e: on_change(e.value))
        box.props("dense outlined").classes("flex-1 min-w-40").mark(marker)
        box.set_enabled(not self.readonly)

    def field(self, field: str, value: Any, values: dict[str, Any]) -> None:
        marker = f"form.{self.node_id}.{field}"
        if field in ("dist", "input") or field in SELECTS:
            self.select(field, value, values)
        elif field == "track":
            box = ui.checkbox(_label(field), value=bool(value)).mark(marker)
            box.on_value_change(lambda e: self.put(field)(bool(e.value)))
            box.set_enabled(not self.readonly)
        elif field in AREAS:
            text = options_text(value) if field == "options" else str(value)
            put = self.put(field)
            area = ui.textarea(
                _label(field), value=text, on_change=lambda e: put(str(e.value or ""))
            )
            area.props(f"{DEBOUNCE} dense outlined autogrow").classes("w-full").mark(marker)
            if field == "expr":
                area.classes("font-mono")
            area.set_enabled(not self.readonly)
        else:
            text_field(_label(field), str(value), self.put(field), marker).set_enabled(
                not self.readonly
            )

    def delete(self) -> None:
        node_id = self.node_id
        sure = ui.checkbox(t("form.delete_confirm")).mark(f"form.{node_id}.delete_confirm")
        sure.classes("text-sm")

        def remove() -> None:
            self.edit.change(lambda d: form.remove_node(d, node_id))
            self.changed(True)

        button = ui.button(t("form.delete", node=node_id), icon="delete", on_click=remove)
        button.props("flat dense no-caps color=negative").mark(f"form.{node_id}.delete")
        button.bind_enabled_from(sure, "value")

    def build(self, data: Data, preview: Callable[[], None]) -> None:
        values = form.values(data, self.node_id)
        main = [f for f in values if f not in ("type", *FIRST, *LAST)]
        ui.label(values["name"] or self.node_id).classes("text-xl font-semibold")
        with ui.row().classes("items-center gap-2"):
            ui.badge(structure.type_label(str(values["type"])), color="grey-7").props("outline")
            ui.label(self.node_id).classes("rp-muted text-xs font-mono")
        with ui.row().classes("w-full gap-2"):
            for field in (*FIRST, *main):
                self.field(field, values[field], values)
        with ui.expansion(t("web.more_fields")).classes("w-full").props("dense"):
            for field in LAST:
                self.field(field, values[field], values)
        if values["type"] == "uncertain":
            ui.separator()
            ui.label(t("form.preview")).classes("rp-kicker")
            preview()
        if not self.readonly:
            ui.separator()
            self.delete()


def preview(edit: ModelEdit, node_id: str) -> None:
    """Preview of an uncertain node from the trial run; needs a model that compiles."""
    result = edit.checked()
    compiled = result.compiled
    if compiled is None or node_id not in compiled.model.nodes:
        reason = result.rows[0].message if result.rows else result.status
        ui.label(t("form.preview_needs_valid", reason=reason)).classes("rp-muted text-sm")
        return
    if edit.trial_error is not None or node_id not in edit.trial:
        ui.label(t("form.preview_failed", reason=edit.trial_error or "")).classes("text-warning")
        return
    if compiled.model.nodes[node_id].type != "uncertain":
        return
    shown = previews.preview_of(compiled, node_id, edit.trial[node_id])
    unit = compiled.model.nodes[node_id].unit
    density, cdf = previews.preview_figures(shown, unit)
    for fig in (density, cdf):
        fig.update_layout(margin={"l": 30, "r": 10, "t": 30, "b": 30})
        theme.plot(fig, 190)
    with ui.grid(columns=2).classes("w-full gap-x-4 gap-y-0 text-sm"):
        for metric, shown_value in previews.preview_rows(shown, unit):
            ui.label(metric).classes("rp-muted")
            ui.label(shown_value).classes("rp-num text-right")
