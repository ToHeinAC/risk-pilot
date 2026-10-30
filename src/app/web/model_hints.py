"""Hints under the model page: notices and the edits they offer (M5: piecewise, CSV; M3: mark
unknown overrides inactive)."""

from collections.abc import Callable

from nicegui import events, ui

from app.adapters import files
from app.errors import InputError
from app.messages import render, t
from app.model import layout
from app.model.edits import to_empirical, to_piecewise
from app.model.scenarios import mark_unknown_inactive
from app.web.editing import ModelEdit


class Hints:
    def __init__(self, edit: ModelEdit, changed: Callable[[bool], None]) -> None:
        self.edit = edit
        self.changed = changed  # argument: redraw the node card too
        self.csv: bytes | None = None
        self.csv_note: tuple[bool, str] | None = None

    @ui.refreshable_method
    def build(self) -> None:
        result = self.edit.checked()
        readonly = self.edit.model.readonly
        if result.model is not None and result.model.illustrative:
            ui.label(t("lesson.illustrative")).classes("text-warning")
        for notice in result.notices:
            ui.label(notice).classes("rp-muted")
        self.fit_offers(readonly)
        if readonly:
            return
        if result.unknown_nodes:
            ui.button(t("scen.mark_inactive"), on_click=self.mark_inactive).props(
                "flat no-caps"
            ).mark("mark_inactive")
        self.prune_offer()
        self.csv_import()

    def fit_offers(self, readonly: bool) -> None:
        """Quantile fits that miss by more than 2 %: offer the piecewise distribution instead."""
        compiled = self.edit.checked().compiled
        if compiled is None:
            return
        for notice in compiled.notices:
            conflict = notice.code == "fit.conflict"
            ui.label(render(notice)).classes("text-warning" if conflict else "rp-muted")
            if conflict and not readonly and notice.node_id is not None:
                self.piecewise(notice.node_id)

    def piecewise(self, node_id: str) -> None:
        with ui.row().classes("items-center gap-2"):
            p0 = ui.number(t("model.p0")).props("dense outlined").mark(f"piecewise_p0_{node_id}")
            p100 = ui.number(t("model.p100")).props("dense outlined")
            p100.mark(f"piecewise_p100_{node_id}")

            def convert() -> None:
                lo, hi = p0.value, p100.value
                if lo is None or hi is None:
                    return
                self.edit.edit_model(lambda m: to_piecewise(m, node_id, lo, hi))
                self.changed(True)

            button = ui.button(t("model.to_piecewise"), on_click=convert).props("flat no-caps")
            button.mark(f"to_piecewise_{node_id}")
            # the user sets the bounds, the app does not
            button.bind_enabled_from(p0, "value", lambda _v: None not in (p0.value, p100.value))
            button.bind_enabled_from(p100, "value", lambda _v: None not in (p0.value, p100.value))

    def prune_offer(self) -> None:
        """Positions of unknown nodes stay until the user removes them (M9 E2)."""
        compiled = self.edit.checked().compiled
        if compiled is None or not any(n.code == "layout.unknown_node" for n in compiled.notices):
            return

        def prune() -> None:
            self.edit.change(layout.prune)
            self.changed(False)

        ui.button(t("model.prune_layout"), on_click=prune).props("flat no-caps").mark(
            "prune_layout"
        )

    def mark_inactive(self) -> None:
        self.edit.edit_model(mark_unknown_inactive)
        self.changed(True)

    async def uploaded(self, e: events.UploadEventArguments) -> None:
        self.csv, self.csv_note = await e.file.read(), None
        self.csv_part.refresh()

    def csv_import(self) -> None:
        model = self.edit.checked().model
        if model is None or not any(n.type == "uncertain" for n in model.nodes.values()):
            return
        busy = self.csv is not None or self.csv_note is not None
        with (
            ui.expansion(t("model.csv_title"), value=busy).classes("rp-panel w-full").props("dense")
        ):
            upload = ui.upload(label=t("model.csv_file"), on_upload=self.uploaded, auto_upload=True)
            upload.props("accept=.csv,.txt flat bordered").classes("w-full").mark("csv_file")
            self.csv_part()

    @ui.refreshable_method
    def csv_part(self) -> None:
        if self.csv_note is not None:
            done, text = self.csv_note
            ui.label(text).classes("text-positive" if done else "text-negative")
        if self.csv is None:
            return
        data = self.csv
        try:
            columns = files.csv_columns(data)
        except InputError as exc:
            ui.label(render(exc.issue)).classes("text-negative")
            return
        model = self.edit.checked().model
        nodes = model.nodes if model is not None else {}
        targets = [i for i, n in nodes.items() if n.type == "uncertain"]
        with ui.row().classes("items-center gap-2"):
            column = ui.select(columns, value=columns[0], label=t("model.csv_column"))
            column.props("dense outlined").classes("min-w-40").mark("csv_column")
            node = ui.select(
                targets, value=targets[0] if targets else None, label=t("model.csv_node")
            )
            node.props("dense outlined").classes("min-w-40").mark("csv_node")
            ui.button(
                t("model.csv_import"),
                on_click=lambda: self.import_csv(data, str(column.value), str(node.value)),
            ).props("unelevated no-caps").mark("csv_import")

    def import_csv(self, data: bytes, column: str, node_id: str) -> None:
        try:
            values, skipped = files.csv_column(data, column)
        except InputError as exc:
            self.csv_note = (False, render(exc.issue))
            self.csv_part.refresh()
            return
        if self.edit.edit_model(lambda m: to_empirical(m, node_id, values)):
            note = t("model.csv_done", n=len(values), skipped=skipped, node=node_id)
            self.csv, self.csv_note = None, (True, note)
        self.changed(True)
