"""Comparison of scenarios: same seed, paired differences (M7 step 4)."""

from typing import Any

from nicegui import run, ui

from app.analysis.compare import compare
from app.engine.simulate import N_MAX
from app.errors import SimulationError
from app.messages import render, t
from app.model.schema import BASIS, OutputNode
from app.present import figures
from app.present.compare import better_sentence, compare_rows, d_rows, direction_sentence
from app.present.text import number, validity_line
from app.present.validation import CheckResult, check_text
from app.web import results_view, running, theme
from app.web.session import CompareView, OpenModel, RunView, Session

MAX_OTHERS = 3


def _horizon_hint(base: RunView, output: str) -> None:
    """Comparison works on raw values, also beyond an output's horizon."""
    node = base.compiled.model.nodes[output]
    if isinstance(node, OutputNode) and node.horizon is not None:
        name = node.name or output
        results_view.note(t("result.horizon_raw", name=name, horizon=number(node.horizon)))


def _pair(base: RunView, other: RunView, sid: str, output: str) -> str:
    """One B-against-A block; returns the kind of the comparison (num or bool)."""
    node = base.compiled.model.nodes[output]
    unit = node.unit
    better = node.better if isinstance(node, OutputNode) else None
    c = compare(
        base.result.samples[output],
        other.result.samples[output],
        target=base.compiled.nodes[output].target,
        better=better,
    )
    ui.label(t("compare.pair", b=other.scenario, a=base.scenario)).classes("text-lg font-semibold")
    headers = [t("ui.metric"), base.scenario, other.scenario, t("compare.diff")]
    results_view.table(headers, compare_rows(c, unit)).mark(f"compare_{output}_{sid}")
    sentence = better_sentence(c, base.scenario, other.scenario)
    ui.label(sentence or direction_sentence(c, base.scenario, other.scenario)).classes("rp-answer")
    if c.kind == "num":
        ui.label(t("compare.d_table")).classes("rp-kicker")
        results_view.table([t("ui.metric"), t("ui.value")], d_rows(c, unit)).mark(
            f"compare_d_{output}_{sid}"
        )
        ui.label(t("compare.d_caption")).classes("rp-muted text-sm")
        theme.plot(figures.histogram(c.d, unit, []), 260)
    return c.kind


def _output(view: CompareView, output: str) -> None:
    base = view.runs[view.ref]
    _horizon_hint(base, output)
    for sid, other in view.runs.items():
        if sid != view.ref:
            with ui.column().classes("rp-panel p-4 w-full gap-2"):
                _pair(base, other, sid, output)
    if base.summaries[output].kind == "num":
        samples = {r.scenario: r.result.samples[output] for r in view.runs.values()}
        unit = base.compiled.model.nodes[output].unit
        theme.plot(figures.compare_cdfs(samples, unit), 320)


def show(view: CompareView) -> None:
    base = view.runs[view.ref]
    ui.label(validity_line(base.result.meta, base.scenario)).classes("rp-muted text-sm")
    outputs = list(base.summaries)
    if len(outputs) == 1:
        _output(view, outputs[0])
        return
    with ui.tabs().props("dense no-caps align=left").classes("w-full") as tabs:
        heads = [ui.tab(base.compiled.model.nodes[o].name or o) for o in outputs]
    with ui.tab_panels(tabs, value=heads[0]).classes("w-full bg-transparent"):
        for head, output in zip(heads, outputs, strict=True):
            with ui.tab_panel(head).classes("p-0 gap-4"):
                _output(view, output)


class ComparePage:
    def __init__(self, session: Session, model: OpenModel, checked: CheckResult) -> None:
        self.session = session
        self.model = model
        self.scenarios = checked.scenarios
        self.names = {sid: name for sid, (name, _compiled) in self.scenarios.items()}

    def build(self) -> None:
        ids = list(self.scenarios)
        settings = self.scenarios[BASIS][1].model.settings
        with ui.row().classes("rp-panel p-4 items-end gap-4 w-full"):
            self.ref = ui.select(self.names, value=ids[0], label=t("compare.ref"))
            self.ref.props("outlined dense").classes("min-w-48").mark("compare_ref")
            self.others = ui.select(
                self._choices(), value=[], multiple=True, label=t("compare.others")
            )
            self.others.props(f"outlined dense use-chips max-values={MAX_OTHERS}")
            self.others.classes("min-w-64").mark("compare_others")
            self.n = ui.number(t("ui.n"), value=settings.n, min=100, max=N_MAX, step=1000)
            self.n.props("outlined dense").mark("compare_n")
            self.seed = ui.number(t("ui.seed"), value=settings.seed, min=0, step=1)
            self.seed.props("outlined dense").mark("compare_seed")
            self.button = ui.button(t("compare.run"), icon="compare_arrows", on_click=self.run)
            self.button.props("unelevated no-caps").mark("compare_run")
        ui.label(t("compare.same_seed")).classes("rp-muted text-sm")
        self.ref.on_value_change(self._ref_changed)
        self.others.on_value_change(self._others_changed)
        self._others_changed()
        self.status = ui.row().classes("items-center gap-2")
        self.results()

    def _choices(self) -> dict[str, str]:
        ref = self.ref.value
        return {sid: name for sid, name in self.names.items() if sid != ref}

    def _picked(self) -> list[str]:
        raw: list[Any] = list(self.others.value or [])
        return [str(s) for s in raw if s != self.ref.value]

    def _ref_changed(self) -> None:
        picked = self._picked()
        self.others.set_options(self._choices(), value=picked)  # pyright: ignore[reportUnknownMemberType]

    def _others_changed(self) -> None:
        self.button.set_enabled(bool(self.others.value))

    async def run(self) -> None:
        sids = [str(self.ref.value), *self._picked()[:MAX_OTHERS]]
        n, seed, text = int(self.n.value or 100), int(self.seed.value or 0), self.model.text
        self.status.clear()
        with self.status:
            ui.spinner(size="sm")
            ui.label(t("ui.running")).classes("rp-muted")
        self.button.disable()
        try:
            runs = {sid: await self._one(sid, text, n, seed) for sid in sids}
        except SimulationError as exc:
            self.status.clear()
            with self.status:
                ui.label(render(exc.issue)).classes("text-negative")
            return
        finally:
            self.button.enable()
        self.status.clear()
        self.session.compare = CompareView(text, sids[0], runs)
        self.results.refresh()

    async def _one(self, sid: str, text: str, n: int, seed: int) -> RunView:
        name, compiled = self.scenarios[sid]
        done = await run.io_bound(
            running.compute_run, self.session.runs, compiled, text, n, seed, name, sid
        )
        assert done is not None  # io_bound returns None only while the app shuts down
        return done

    @ui.refreshable_method
    def results(self) -> None:
        view = self.session.compare
        if view is None:
            return
        if view.text != self.model.text:  # the model changed since: old results no longer apply
            ui.label(t("compare.stale")).classes("rp-muted")
            return
        show(view)


def page(session: Session) -> None:
    ui.label(t("ui.page_vergleich")).classes("text-2xl font-semibold")
    model = session.model
    if model is None:
        ui.label(t("ui.no_model")).classes("rp-muted")
        return
    checked = check_text(model.text)
    if len(checked.scenarios) < 2:
        ui.label(t("compare.need_two")).classes("rp-muted")
        return
    ComparePage(session, model, checked).build()
