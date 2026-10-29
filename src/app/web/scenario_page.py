"""Scenarios: tree, diff, create, override, duplicate, detach (M7 step 4)."""

from collections.abc import Callable

import yaml
from nicegui import ui

from app.adapters import files
from app.messages import t
from app.model import scenarios as sc
from app.model.schema import BASIS, Model
from app.present.validation import check_text
from app.web import results_view, scenario_edit
from app.web.session import OpenModel, Session


def _line(model: Model, sid: str, depth: int) -> None:
    with ui.row().classes("items-baseline gap-2").style(f"padding-left: {depth * 1.5}rem"):
        if sid == BASIS:
            ui.label(t("ui.main_scenario")).classes("font-semibold")
            ui.label(f"({BASIS})").classes("rp-muted text-sm")
            return
        s = model.scenarios[sid]
        extra = (
            t("scen.detached") if s.nodes is not None else t("scen.overrides", n=len(s.overrides))
        )
        ui.label(s.name).classes("font-semibold")
        ui.label(f"({sid}) · {extra}").classes("rp-muted text-sm")


def _diff(model: Model, sid: str) -> None:
    ui.markdown(t("scen.why", why=model.scenarios[sid].why))
    rows = [
        (r.node, r.field, str(r.before), str(r.after), r.why or "", r.status)
        for r in sc.diff(model, sid)
    ]
    if not rows:
        ui.label(t("scen.no_overrides")).classes("rp-muted")
        return
    headers = [
        t("scen.col_node"),
        t("scen.col_field"),
        t("scen.col_parent"),
        t("scen.col_value"),
        t("scen.col_why"),
        t("scen.col_status"),
    ]
    results_view.table(headers, rows).mark("scenario_diff")


def _field(label: str, marker: str) -> ui.input:
    return ui.input(label).props("outlined dense").classes("min-w-48").mark(marker)


class ScenarioPage:
    def __init__(self, model: OpenModel) -> None:
        self.model = model
        self.pick = BASIS
        self.message: str | None = None
        self.detach_pending = False

    def edit(self, change: Callable[[Model], Model]) -> bool:
        """Apply a change to the draft if the result is valid; otherwise explain and keep it."""
        text, self.message = scenario_edit.apply(self.model.text, change)
        self.model.draft = text
        self.body.refresh()
        return self.message is None

    def select(self, sid: str) -> None:
        self.pick, self.detach_pending = sid, False
        self.body.refresh()

    @ui.refreshable_method
    def body(self) -> None:
        model = check_text(self.model.text).model
        if model is None:
            ui.label(t("scen.invalid_model")).classes("text-negative")
            return
        if self.message:
            ui.label(self.message).classes("text-negative")
        ids = [sid for sid, _ in sc.tree(model)]
        self.pick = self.pick if self.pick in ids else BASIS
        with ui.row().classes("w-full gap-4 no-wrap max-lg:flex-wrap items-start"):
            with ui.column().classes("rp-panel p-4 gap-1 flex-[2] min-w-64"):
                for sid, depth in sc.tree(model):
                    _line(model, sid, depth)
            with ui.column().classes("flex-[3] min-w-0 gap-3"):
                self._detail(model, ids)

    def _detail(self, model: Model, ids: list[str]) -> None:
        names = {s: model.scenarios[s].name if s != BASIS else t("ui.main_scenario") for s in ids}
        ui.select(
            names, value=self.pick, label=t("scen.pick"), on_change=lambda e: self.select(e.value)
        ).props("outlined dense").classes("min-w-64").mark("scenario_pick")
        if self.pick != BASIS:
            _diff(model, self.pick)
        if self.model.readonly:
            ui.label(t("scen.readonly")).classes("rp-muted")
            return
        if self.pick != BASIS:
            self._override_form(model, ids)
        self._create_form(names)

    def _create_form(self, names: dict[str, str]) -> None:
        with ui.expansion(t("scen.new"), icon="add").classes("rp-panel w-full"):
            with ui.row().classes("items-end gap-3 p-2"):
                sid = _field(t("scen.new_id"), "scenario_new_id")
                name = _field(t("scen.new_name"), "scenario_new_name")
                why = _field(t("scen.new_why"), "scenario_new_why")
                parent = ui.select(names, value=self.pick, label=t("scen.new_parent"))
                parent.props("outlined dense").classes("min-w-48").mark("scenario_new_parent")

            def add() -> None:
                new = str(sid.value or "").strip()
                label = str(name.value or "").strip() or new
                reason = str(why.value or "").strip()
                if self.edit(lambda m: sc.add_scenario(m, new, label, str(parent.value), reason)):
                    self.select(new)

            ui.button(t("scen.add"), icon="add", on_click=add).props("unelevated no-caps").mark(
                "scenario_add"
            )

    def _override_form(self, model: Model, ids: list[str]) -> None:
        sid = self.pick
        if model.scenarios[sid].nodes is None:
            self._overrides(model, sid)
        with ui.row().classes("gap-2"):
            new_id = files.suggest_id(f"{sid}_kopie", set(ids))
            ui.button(
                t("scen.duplicate"),
                icon="content_copy",
                on_click=lambda: self.edit(lambda m: sc.duplicate(m, sid, new_id)),
            ).props("outline no-caps").mark("scenario_duplicate")
            ui.button(t("scen.detach"), icon="link_off", on_click=self._ask_detach).props(
                "outline no-caps"
            ).mark("scenario_detach")
        if self.detach_pending:
            ui.label(t("scen.detach_question")).classes("text-warning")
            ui.button(t("scen.detach_confirm"), color="negative", on_click=self._detach).props(
                "unelevated no-caps"
            ).mark("scenario_detach_confirm")

    def _ask_detach(self) -> None:
        self.detach_pending = True
        self.body.refresh()

    def _detach(self) -> None:
        self.detach_pending = False
        sid = self.pick
        self.edit(lambda m: sc.detach(m, sid))

    def _overrides(self, model: Model, sid: str) -> None:
        ui.label(t("scen.override")).classes("text-lg font-semibold")
        with ui.row().classes("items-end gap-3"):
            node = ui.select(list(model.nodes), value=next(iter(model.nodes)))
            node.props(f'outlined dense label="{t("scen.col_node")}"').mark("override_node")
            field = _field(t("scen.col_field"), "override_field")
            raw = _field(t("scen.value_hint"), "override_value")
            why = _field(t("scen.col_why"), "override_why")

        def set_override() -> None:
            text = str(raw.value or "").strip()
            new = yaml.safe_load(text) if text else None
            if new is None:
                self.message = t("scen.value_missing")
                self.body.refresh()
                return
            target, name = str(node.value), str(field.value or "").strip()
            reason = str(why.value or "").strip() or None
            self.edit(lambda m: sc.set_override(m, sid, target, name, new, reason))

        ui.button(t("scen.set"), on_click=set_override).props("unelevated no-caps").mark(
            "override_set"
        )
        existing = [f"{r.node}.{r.field}" for r in sc.diff(model, sid)]
        if existing:
            self._remove(sid, existing)

    def _remove(self, sid: str, existing: list[str]) -> None:
        with ui.row().classes("items-end gap-3"):
            pick = ui.select(existing, value=existing[0], label=t("scen.remove_pick"))
            pick.props("outlined dense").classes("min-w-48").mark("override_remove_pick")

            def remove() -> None:
                target, _, name = str(pick.value).partition(".")
                self.edit(lambda m: sc.remove_override(m, sid, target, name))

            ui.button(t("scen.remove"), icon="delete", on_click=remove).props(
                "outline no-caps"
            ).mark("override_remove")


def page(session: Session) -> None:
    ui.label(t("ui.page_szenarien")).classes("text-2xl font-semibold")
    if session.model is None:
        ui.label(t("ui.no_model")).classes("rp-muted")
        return
    ScenarioPage(session.model).body()
