"""The card of one node (M6 form fields, M7 look): description first, what the node computes
(in the scenario on the canvas), fields by type, a long comment, delete, preview."""

# plotly ships without type stubs; its members are untyped for pyright.
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false
from collections.abc import Callable
from typing import Any

from nicegui import ui

from app.dists.families import QUANTILES
from app.dists.registry import families, get_family
from app.messages import UI, t
from app.model import form
from app.model import scenarios as sc
from app.model.schema import BASIS
from app.model.yaml_patch import Data
from app.present import preview as previews
from app.present import structure
from app.present.brief import brief
from app.web import canvas_scenario, theme
from app.web.editing import ModelEdit

SELECTS: dict[str, tuple[str, ...]] = {
    "target_op": ("", *form.TARGET_OPS),
    "better": ("", "lower", "higher"),
}
AREAS = ("why", "expr", "options")
FIRST = ("name", "unit")
LAST = ("why", "tags", "bounds_min", "bounds_max", "track")
OWN = ("description", "comment")  # each in its own place on the card
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
    key = f"form.f_{field.removeprefix('param.')}"
    return t(key) if key in UI["de"] else field.removeprefix("param.")


class NodeCard:
    def __init__(
        self, edit: ModelEdit, node_id: str, changed: Callable[[bool], None], scenario: str = BASIS
    ) -> None:
        self.edit = edit
        self.node_id = node_id
        self.changed = changed
        self.readonly = edit.model.readonly
        self.scenario = scenario  # the one on the canvas

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

    def about(self, description: str) -> None:
        """What the node is (its description) and what it computes in the canvas scenario."""
        put = self.put("description")
        area = ui.textarea(
            t("form.about"), value=description, on_change=lambda e: put(str(e.value or ""))
        )
        area.props(f"{DEBOUNCE} dense filled autogrow").classes("w-full")
        area.mark(f"form.{self.node_id}.description").set_enabled(not self.readonly)
        model = self.edit.checked().model
        if model is None:
            return
        sid = self.scenario if self.scenario in model.scenarios else BASIS
        nodes = model.nodes if sid == BASIS else sc.effective_model(model, sid).nodes
        if self.node_id in nodes and (what := brief(nodes[self.node_id])):
            does = ui.label(t("form.does", what=what)).classes("rp-muted text-sm font-mono")
            does.mark("card_does")

    def scenario_note(self) -> None:
        """In a sub-scenario: what it overrides here, and that the fields show the main one."""
        model = self.edit.checked().model
        if self.scenario == BASIS or model is None or self.scenario not in model.scenarios:
            return
        rows = [r for r in sc.diff(model, self.scenario) if r.node == self.node_id]
        name = model.scenarios[self.scenario].name
        with ui.column().classes("rp-scenario-note w-full gap-1").mark("card_scenario"):
            ui.label(t("form.in_scenario", scenario=name)).classes("font-semibold")
            for r in rows:
                why = f" – {r.why}" if r.why else ""
                before, after = canvas_scenario.shown(r.before), canvas_scenario.shown(r.after)
                ui.label(f"{_label(r.field)}: {before} → {after}{why}").classes("text-sm")
            if not rows:
                ui.label(t("form.scenario_same")).classes("text-sm")
            ui.label(t("form.scenario_basis")).classes("rp-muted text-xs")
            if not self.readonly and model.scenarios[self.scenario].nodes is None:
                ui.button(
                    t("form.scenario_override"), icon="edit_note", on_click=self.override
                ).props("flat dense no-caps").mark("card_override")

    def override(self) -> None:
        canvas_scenario.override(self.edit, self.scenario, self.node_id, self.overridden)

    def overridden(self, node_id: str) -> None:
        self.edit.selected = node_id
        self.changed(True)

    def comment(self, text: str) -> None:
        """The long comment: written as Markdown, read rendered; reading first once it exists."""
        node_id = self.node_id
        with ui.row().classes("w-full items-center"):
            ui.label(t("form.f_comment")).classes("rp-kicker")
            ui.space()
            modes = {"edit": t("form.comment_edit"), "view": t("form.comment_view")}
            first = "view" if text.strip() or self.readonly else "edit"
            mode = ui.toggle(modes, value=first).props("dense no-caps unelevated size=sm")
            mode.mark(f"form.{node_id}.comment_mode")
        put = self.put("comment")
        area = ui.textarea(
            placeholder=t("form.comment_hint"),
            value=text,
            on_change=lambda e: put(str(e.value or "")),
        )
        area.props(f"{DEBOUNCE} outlined autogrow input-style='min-height:7rem'")
        area.classes("w-full").mark(f"form.{node_id}.comment").set_enabled(not self.readonly)
        view = ui.markdown(text).classes("rp-comment w-full").mark(f"form.{node_id}.comment_view")

        def show() -> None:
            reading = mode.value == "view"
            if reading:
                data = self.edit.data()
                current = form.values(data, node_id)["comment"] if data else text
                view.content = current or t("form.comment_empty")
            area.set_visibility(not reading)
            view.set_visibility(reading)

        mode.on_value_change(show)
        show()

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
        main = [f for f in values if f not in ("type", *FIRST, *LAST, *OWN)]
        ui.label(values["name"] or self.node_id).classes("text-xl font-semibold")
        with ui.row().classes("items-center gap-2"):
            ui.badge(structure.type_label(str(values["type"])), color="grey-7").props("outline")
            ui.label(self.node_id).classes("rp-muted text-xs font-mono")
        self.about(str(values["description"]))
        self.scenario_note()
        with ui.row().classes("w-full gap-2"):
            for field in (*FIRST, *main):
                self.field(field, values[field], values)
        if values["type"] == "uncertain" and values.get("input") == QUANTILES:
            ui.label(t("form.range_hint")).classes("rp-muted text-sm").mark("range_hint")
        ui.separator()
        self.comment(str(values["comment"]))
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
