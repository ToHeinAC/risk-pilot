"""Model workbench (M7, GoRules principle): canvas (M9), node table and node card in one place.

Guesstimate principle: every row shows the node's input in brief, its distribution in small
and P10/P50/P90 from the trial run, which reruns on every change.
"""

from collections.abc import Callable
from typing import Any

from nicegui import ui

from app.messages import t
from app.model import form
from app.model.schema import Model
from app.model.yaml_patch import Data
from app.present import structure
from app.present.brief import brief, spark_svg
from app.present.text import number, percent
from app.web import node_card
from app.web.canvas_panel import TYPES, CanvasPanel
from app.web.editing import ModelEdit

COLUMNS: list[dict[str, Any]] = [
    {"name": "name", "label": t("web.col_node"), "field": "name", "align": "left"},
    {"name": "type", "label": t("ui.col_type"), "field": "type", "align": "left"},
    {"name": "brief", "label": t("web.col_brief"), "field": "brief", "align": "left"},
    {"name": "spark", "label": t("web.col_spark"), "field": "spark", "align": "left"},
    {"name": "p10", "label": "P10", "field": "p10", "align": "right"},
    {"name": "p50", "label": "P50", "field": "p50", "align": "right"},
    {"name": "p90", "label": "P90", "field": "p90", "align": "right"},
    {"name": "why", "label": t("form.col_why"), "field": "why", "align": "left"},
]
ROW = """
<q-tr :props="props" class="cursor-pointer" :class="props.row.sel ? 'rp-selected' : ''"
      @click="() => $parent.$emit('pick', props.row.id)">
  <q-td key="name" :props="props"><div class="font-medium">{{ props.row.name }}</div>
    <div class="rp-muted text-xs font-mono">{{ props.row.id }}</div></q-td>
  <q-td key="type" :props="props"><q-badge outline color="grey-7" :label="props.row.type"/></q-td>
  <q-td key="brief" :props="props">{{ props.row.brief }}</q-td>
  <q-td key="spark" :props="props"><span class="rp-spark" v-html="props.row.spark"></span></q-td>
  <q-td key="p10" :props="props" class="rp-num">{{ props.row.p10 }}</q-td>
  <q-td key="p50" :props="props" class="rp-num">{{ props.row.p50 }}</q-td>
  <q-td key="p90" :props="props" class="rp-num">{{ props.row.p90 }}</q-td>
  <q-td key="why" :props="props" class="rp-muted">{{ props.row.why }}</q-td>
</q-tr>
"""


def _row(edit: ModelEdit, data: Data, node_id: str, model: Model | None) -> dict[str, Any]:
    v = form.values(data, node_id)
    row: dict[str, Any] = {
        "id": node_id,
        "name": v["name"] or node_id,
        "type": structure.type_label(str(v["type"])),
        "brief": brief(model.nodes[node_id]) if model and node_id in model.nodes else "",
        "spark": spark_svg(edit.trial[node_id]) if node_id in edit.trial else "",
        "p10": "",
        "p50": "",
        "p90": "",
        "why": t("form.yes") if v["why"] else t("form.no"),
        "sel": node_id == edit.selected,
    }
    tr = edit.traces.get(node_id)
    if tr is not None and v["type"] == "event":
        row["p50"] = percent(tr.mean)
    elif tr is not None:
        row.update(p10=number(tr.p10), p50=number(tr.p50), p90=number(tr.p90))
    return row


class Workbench:
    """The form side of the model page; each part redraws on its own, so a field being typed
    in keeps its focus. ``changed`` tells the page that the draft changed."""

    def __init__(self, edit: ModelEdit, changed: Callable[[bool], None]) -> None:
        self.edit = edit
        self.changed = changed  # argument: redraw the node card too
        self.panel = CanvasPanel(edit, changed, self.select)

    @ui.refreshable_method
    def notes(self) -> None:
        if self.edit.error:
            ui.label(self.edit.error).classes("text-negative").mark("form_error")
        elif self.edit.written:
            ui.label(t("form.written")).classes("rp-muted text-sm")

    @ui.refreshable_method
    def table(self) -> None:
        data = self.edit.data()
        if data is None:
            return
        ids = form.node_ids(data)
        if not ids:
            ui.label(t("form.no_nodes")).classes("rp-muted p-2")
            return
        model = self.edit.checked().model
        rows = [_row(self.edit, data, i, model) for i in ids]
        table = ui.table(columns=COLUMNS, rows=rows, row_key="id")
        table.props("flat dense hide-pagination :pagination='{rowsPerPage: 0}'")
        table.classes("w-full").mark("nodes")
        table.add_slot("body", ROW)
        table.on("pick", lambda e: self.select(str(e.args)))

    def header(self, data: Data) -> None:
        values = form.header_values(data)
        title = t("form.header", model=data.get("model", ""))
        box = ui.expansion(title).classes("rp-panel w-full").props("dense")
        with box, ui.row().classes("w-full gap-2 p-2"):
            for name in ("title", "description", "n", "seed"):
                node_card.text_field(
                    t(f"form.f_{name}"),
                    str(values[name]),
                    self.header_put(name),
                    f"form.{name}",
                ).set_enabled(not self.edit.model.readonly)
            check = ui.checkbox(t("form.f_illustrative"), value=bool(values["illustrative"]))
            check.on_value_change(lambda e: self.header_put("illustrative")(bool(e.value)))
            check.mark("form.illustrative").set_enabled(not self.edit.model.readonly)

    def header_put(self, name: str) -> Callable[[Any], None]:
        def put(value: Any) -> None:
            self.edit.change(lambda d: form.apply_header(d, {**form.header_values(d), name: value}))
            self.changed(False)

        return put

    def add_row(self) -> None:
        with ui.row().classes("w-full items-center gap-2 px-2 pb-2"):
            new_id = ui.input(t("form.new_id")).props("dense outlined").mark("form_new_id")
            options = {k: t(f"type.{k}") for k in TYPES}
            kind = ui.select(options, value=TYPES[0], label=t("form.new_type"))
            kind.props("dense outlined").classes("min-w-40").mark("form_new_type")

            def add() -> None:
                node_id = str(new_id.value or "").strip()
                if self.edit.change(lambda d: form.add_node(d, node_id, str(kind.value))):
                    self.edit.selected = node_id
                    new_id.value = ""
                self.changed(True)

            ui.button(t("form.add_button"), icon="add", on_click=add).props("flat no-caps").mark(
                "form_add"
            )

    def select(self, node_id: str) -> None:
        self.edit.selected = node_id
        self.panel.redraw()
        for part in (self.table, self.card):
            part.refresh()

    @ui.refreshable_method
    def card(self) -> None:
        data = self.edit.data()
        node_id = self.edit.selected
        if data is None or node_id is None or node_id not in form.node_ids(data):
            ui.label(t("web.pick_node")).classes("rp-muted")
            return
        card = node_card.NodeCard(self.edit, node_id, self.changed, self.panel.scenario)
        card.build(data, self.preview)

    @ui.refreshable_method
    def preview(self) -> None:
        if self.edit.selected is not None:
            node_card.preview(self.edit, self.edit.selected)

    def refresh(self, card: bool) -> None:
        self.panel.refresh()
        for part in (self.notes, self.table, self.preview):
            part.refresh()
        if card:
            self.card.refresh()

    def build(self) -> None:
        data = self.edit.data()
        if data is None:
            ui.label(self.edit.data_error() or "").classes("text-negative")
            return
        self.header(data)
        with ui.row().classes("w-full gap-4 no-wrap max-lg:flex-wrap items-start"):
            with ui.column().classes("rp-panel p-2 flex-[3] min-w-0 w-full gap-1"):
                self.panel.build(data)
            with ui.column().classes("rp-panel p-4 flex-[2] min-w-80 w-full gap-3"):
                self.card()
        with ui.column().classes("rp-panel p-2 w-full gap-1 min-w-0 overflow-hidden"):
            self.notes()
            self.table()
            if not self.edit.model.readonly:
                self.add_row()
