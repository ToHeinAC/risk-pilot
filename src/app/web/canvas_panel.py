"""The canvas part of the model page (M9): toolbar, scenario mode and the canvas events.

In the main scenario the canvas edits the structure (link dialog, edge delete, palette). In a
sub-scenario the structure is locked; changed nodes are marked and a click opens the override
dialog (E3). A detached scenario shows its own nodes, read only.
"""

from collections.abc import Callable
from typing import Any, cast

from nicegui import events, ui

from app.errors import InputError
from app.messages import render, t
from app.model import canvas, layout
from app.model import scenarios as sc
from app.model.schema import BASIS
from app.model.yaml_patch import Data
from app.present import canvas_view
from app.web import canvas_dialogs, canvas_scenario
from app.web.canvas import FlowCanvas
from app.web.editing import ModelEdit

TYPES = ("uncertain", "constant", "event", "choice", "derived", "output")
PALETTE = [{"type": k, "label": t(f"type.{k}"), "hint": t("canvas.palette_hint")} for k in TYPES]


class CanvasPanel:
    def __init__(
        self, edit: ModelEdit, changed: Callable[[bool], None], select: Callable[[str], None]
    ) -> None:
        self.edit = edit
        self.changed = changed  # argument: redraw the node card too
        self.select = select
        self.canvas: FlowCanvas | None = None
        self.scenario = BASIS

    # --- scenario mode -------------------------------------------------------------------

    def scenarios(self) -> dict[str, str]:
        model = self.edit.checked().model
        options = {BASIS: t("canvas.basis")}
        if model is not None:
            options |= {sid: f"{s.name} ({sid})" for sid, s in model.scenarios.items()}
        return options

    def detached(self) -> bool:
        model = self.edit.checked().model
        return (
            model is not None
            and self.scenario in model.scenarios
            and model.scenarios[self.scenario].nodes is not None
        )

    def locked(self) -> bool:
        """No structure edits: a tutorial, or any scenario but the main one."""
        return self.edit.model.readonly or self.scenario != BASIS

    def marks(self) -> dict[str, int]:
        model = self.edit.checked().model
        if model is None or self.scenario not in model.scenarios:
            return {}
        return sc.changed_nodes(model, self.scenario)

    def shown(self, data: Data) -> Data:
        """The draft as drawn: a detached scenario shows its own nodes."""
        if not self.detached():
            return data
        own = cast(dict[str, Any], data["scenarios"][self.scenario])
        return {**data, "nodes": own["nodes"], "correlations": {}}

    def pick_scenario(self, sid: str) -> None:
        self.scenario = sid if sid in self.scenarios() else BASIS
        if self.detached():
            ui.notify(t("canvas.detached"))
        self.redraw()

    @ui.refreshable_method
    def scenario_bar(self) -> None:
        options = self.scenarios()
        if self.scenario not in options:
            self.scenario = BASIS
        with ui.row().classes("w-full items-center gap-2 px-1"):
            pick = ui.select(options, value=self.scenario, label=t("canvas.scenario"))
            pick.props("outlined dense").classes("min-w-56").mark("canvas_scenario")
            pick.on_value_change(lambda e: self.pick_scenario(str(e.value)))
            if not self.edit.model.readonly and self.edit.checked().model is not None:
                ui.button(t("canvas.new_scenario"), icon="add", on_click=self.new_scenario).props(
                    "flat dense no-caps"
                ).mark("canvas_new_scenario")
            if self.scenario != BASIS:
                ui.label(t("canvas.scenario_mode")).classes("rp-muted text-xs")

    def new_scenario(self) -> None:
        canvas_scenario.new_scenario(self.edit, self.scenario, self.scenario_written)

    def scenario_written(self, sid: str) -> None:
        self.scenario = sid
        self.changed(False)

    # --- canvas -------------------------------------------------------------------------

    def build(self, data: Data) -> None:
        """Toolbar, scenario bar and the canvas, drawn from the raw draft (valid or not)."""
        readonly = self.edit.model.readonly
        with ui.row().classes("w-full items-center gap-1 px-1"):
            ui.label(t("canvas.caption")).classes("rp-muted text-xs")
            ui.space()
            if not readonly:
                ui.button(t("canvas.arrange"), icon="account_tree", on_click=self.arrange).props(
                    "flat dense no-caps"
                ).mark("canvas_arrange")
            ui.button(t("canvas.fit"), icon="fit_screen", on_click=self.fit).props(
                "flat dense no-caps"
            ).mark("canvas_fit")
        self.scenario_bar()
        nodes, edges = canvas_view.view(self.shown(data), self.edit.selected, self.marks())
        canvas = FlowCanvas(nodes, edges, readonly, PALETTE)
        canvas.classes("w-full h-[460px] rp-canvas").mark("canvas")
        canvas.on("move", self.on_move)
        canvas.on("pick", self.on_pick)
        canvas.on("connect", self.on_connect)
        canvas.on("disconnect", self.on_disconnect)
        canvas.on("drop", self.on_drop)
        self.canvas = canvas

    def redraw(self) -> None:
        data = self.edit.data()
        if self.canvas is None or data is None:
            return
        self.canvas.mode(not self.locked(), [] if self.locked() else PALETTE)
        self.canvas.draw(*canvas_view.view(self.shown(data), self.edit.selected, self.marks()))

    def refresh(self) -> None:
        self.scenario_bar.refresh()
        self.redraw()

    def fit(self) -> None:
        if self.canvas is not None:
            self.canvas.fit()

    def done(self, node_id: str) -> None:
        """A canvas change was written: open the node and redraw everything."""
        self.edit.selected = node_id
        self.changed(True)

    def refuse(self) -> bool:
        """In scenario mode the structure stays; say so and redraw the drawn line away."""
        if not self.locked():
            return False
        if not self.edit.model.readonly:
            ui.notify(t("canvas.locked"), type="warning")
        self.redraw()
        return True

    # --- events -------------------------------------------------------------------------

    def on_move(self, e: events.GenericEventArguments) -> None:
        if self.edit.model.readonly or self.detached():
            return
        node_id, x, y = str(e.args["id"]), float(e.args["x"]), float(e.args["y"])
        self.edit.change(lambda d: layout.move(d, node_id, x, y))
        self.changed(False)

    def on_pick(self, e: events.GenericEventArguments) -> None:
        node_id = str(e.args)
        self.select(node_id)
        if self.scenario != BASIS and not self.edit.model.readonly and not self.detached():
            canvas_scenario.override(self.edit, self.scenario, node_id, self.done)

    def on_connect(self, e: events.GenericEventArguments) -> None:
        source, target = str(e.args["source"]), str(e.args["target"])
        data = self.edit.data()
        if self.refuse() or data is None:
            return
        try:
            offered = canvas.presets(data, source, target)
        except InputError as exc:
            ui.notify(render(exc.issue), type="warning")
            self.redraw()  # drop the line Vue Flow drew
            return
        if offered == ["edit"]:
            names = {
                "source": canvas_view.name(data, source),
                "target": canvas_view.name(data, target),
            }
            ui.notify(t("canvas.says_edit", **names))
            self.done(target)
            return
        self.redraw()
        canvas_dialogs.link(self.edit, source, target, offered, self.done)

    def on_disconnect(self, e: events.GenericEventArguments) -> None:
        edge = canvas_view.edge_of(str(e.args))
        if edge is None or self.refuse():
            return
        source, target, kind = edge
        action = canvas.uncorrelate if kind == "korrelation" else canvas.disconnect
        if self.edit.change(lambda d: action(d, source, target)):
            self.done(target)
            return
        ui.notify(self.edit.error or "", type="warning", multi_line=True)
        self.edit.error = None
        self.done(target)  # the edge stays; its expression opens

    def on_drop(self, e: events.GenericEventArguments) -> None:
        if self.refuse():
            return
        kind, x, y = str(e.args["type"]), float(e.args["x"]), float(e.args["y"])
        canvas_dialogs.new_node(self.edit, kind, x, y, self.done)

    def arrange(self) -> None:
        self.edit.change(lambda d: layout.arrange(d, canvas_view.auto(d)))
        self.changed(False)
        self.fit()
