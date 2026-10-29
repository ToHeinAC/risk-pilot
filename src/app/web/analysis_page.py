"""Analysis: structure of one scenario – graph, criticality, tornado, sweep, Spearman, risks."""

from collections.abc import Callable

from nicegui import run, ui

from app.engine.simulate import N_MAX
from app.errors import SimulationError
from app.messages import render, t
from app.model.compile import CompiledModel
from app.model.graph import edges
from app.present import structure
from app.present.text import integer
from app.present.validation import CheckResult, check_text, scenario_labels
from app.web import analysing, results_view, theme
from app.web.analysing import MEMORY_HINT_MB, AnalysisState, Base, Key
from app.web.analysis_tools import SweepTab, TornadoTab
from app.web.session import OpenModel, Session

TABS = ("graph", "crit", "tornado", "sweep", "rho", "risk")


def _graph_tab(base: Base, _state: AnalysisState) -> None:
    choices = {
        "sensitivity": t("analysis.color_sensitivity"),
        "criticality": t("analysis.color_criticality"),
        "why": t("analysis.color_why"),
    }
    model = base.compiled.model
    colourings: dict[str, dict[str, float]] = {
        "sensitivity": {r.node: abs(r.rho) for r in base.rho if r.rho is not None},
        "criticality": {node: p.p for node, p in base.crit.indices},
        "why": structure.missing_why(model),
    }
    select = ui.select(
        choices, value="sensitivity", label=t("analysis.color"), on_change=lambda: draw()
    )
    select.props("outlined dense").classes("min-w-64").mark("graph_color")
    area = ui.column().classes("w-full")

    def draw() -> None:
        mode = str(select.value)
        area.clear()
        with area:
            figure = structure.graph_figure(
                model, edges(model), colourings[mode], choices[mode], base.output
            )
            theme.plot(figure, 440).mark("ana_graph")

    draw()
    ui.label(t("analysis.graph_caption")).classes("rp-muted text-sm")


def _criticality_tab(base: Base, _state: AnalysisState) -> None:
    crit = base.crit
    if not crit.selects_path:
        results_view.note(t("analysis.crit_no_extremum"))
    for node, p in crit.indices:
        if base.compiled.nodes[node].type != "derived":
            ui.label(structure.criticality_sentence(base.names[node], p)).classes("rp-answer")
    ui.label(t("analysis.crit_note")).classes("rp-muted text-sm")
    headers = [t("analysis.col_node"), t("analysis.col_index")]
    results_view.table(headers, structure.criticality_rows(crit, base.names))
    if crit.indices:
        theme.plot(structure.criticality_figure(crit, base.names), 320)
    ui.label(t("analysis.constellations")).classes("text-lg font-semibold")
    headers = [t("analysis.col_constellation"), t("analysis.col_share")]
    results_view.table(headers, structure.constellation_rows(crit, base.names))


def _rho_tab(base: Base, _state: AnalysisState) -> None:
    results_view.note(t("analysis.rho_caption"))
    headers = [t("analysis.col_node"), t("analysis.col_rho"), t("analysis.col_interval")]
    results_view.table(headers, structure.rho_rows(base.rho, base.names))


def _risk_tab(base: Base, _state: AnalysisState) -> None:
    if not base.risks:
        results_view.note(t("analysis.no_events"))
        return
    results_view.note(t("analysis.risk_caption"), "warning")
    unit = base.compiled.model.nodes[base.output].unit
    headers = [t("analysis.col_node"), t("analysis.col_p"), t("analysis.col_diff")]
    rows = structure.risk_rows(base.risks, base.names, unit)
    results_view.table(headers, rows).mark("ana_risk_table")
    theme.plot(structure.risk_figure(base.risks, base.names, unit), 380)


Tab = Callable[[Base, AnalysisState], None]
BUILDERS: dict[str, Tab] = {
    "graph": _graph_tab,
    "crit": _criticality_tab,
    "tornado": lambda base, state: TornadoTab(base, state).build(),
    "sweep": lambda base, state: SweepTab(base, state).build(),
    "rho": _rho_tab,
    "risk": _risk_tab,
}


def _tabs(base: Base, state: AnalysisState) -> None:
    with ui.tabs().props("dense no-caps align=left").classes("w-full").mark("ana_tabs") as tabs:
        heads = [ui.tab(t(f"analysis.tab_{name}")) for name in TABS]
    with ui.tab_panels(tabs, value=heads[0]).classes("w-full bg-transparent"):
        for head, name in zip(heads, TABS, strict=True):
            with ui.tab_panel(head).classes("p-0 gap-3"):
                with ui.expansion(t("analysis.help_label"), icon="help_outline").classes(
                    "rp-panel w-full"
                ):
                    ui.markdown(t(f"analysis.help_{name}")).classes("px-4")
                BUILDERS[name](base, state)


class AnalysisPage:
    def __init__(self, session: Session, model: OpenModel, checked: CheckResult) -> None:
        self.state = session.analysis
        self.model = model
        self.scenarios = checked.scenarios
        self.labels = scenario_labels(checked)

    def build(self) -> None:
        with ui.expansion(t("analysis.guide_label"), icon="map").classes("rp-panel w-full"):
            ui.markdown(t("analysis.guide")).classes("px-4")
        sid, output, n, seed = self._start()
        with ui.row().classes("rp-panel p-4 items-end gap-4 w-full"):
            self.scenario = ui.select(self.labels, value=sid, label=t("ui.scenario"))
            self.scenario.props("outlined dense").classes("min-w-56").mark("ana_scenario")
            self.output = ui.select({output: output}, value=output, label=t("analysis.output"))
            self.output.props("outlined dense").classes("min-w-48").mark("ana_output")
            self.n = ui.number(t("ui.n"), value=n, min=100, max=N_MAX, step=1000)
            self.n.props("outlined dense").mark("ana_n")
            self.seed = ui.number(t("ui.seed"), value=seed, min=0, step=1)
            self.seed.props("outlined dense").mark("ana_seed")
            self.button = ui.button(t("analysis.run"), icon="troubleshoot", on_click=self.run)
            self.button.props("unelevated no-caps").mark("ana_run")
        self.hint = ui.label().classes("text-warning")
        self.status = ui.row().classes("items-center gap-2")
        self.results()
        self._outputs()
        self.scenario.on_value_change(self._outputs)
        for widget in (self.output, self.n, self.seed):
            widget.on_value_change(self._changed)
        self._changed()

    def _start(self) -> tuple[str, str | None, int, int]:
        """The settings of the last analysis of this draft, else the model's defaults."""
        base = self.state.base
        if base is not None and base.key[0] == self.model.text and base.key[1] in self.labels:
            _text, sid, output, n, seed = base.key
            return sid, output, n, seed
        first = next(iter(self.labels))
        defaults = self.scenarios[first][1].model.settings
        return first, None, defaults.n, defaults.seed

    def _compiled(self) -> CompiledModel:
        return self.scenarios[str(self.scenario.value)][1]

    def _outputs(self) -> None:
        compiled = self._compiled()
        names = analysing.names(compiled)
        outputs = {o: names[o] for o in analysing.outputs(compiled)}
        keep = self.output.value if self.output.value in outputs else next(iter(outputs))
        self.output.set_options(outputs, value=keep)  # pyright: ignore[reportUnknownMemberType]
        self._changed()

    def _changed(self) -> None:
        compiled = self._compiled()
        mb = analysing.memory_mb(compiled, int(self.n.value or 0))
        big = mb > MEMORY_HINT_MB
        self.hint.text = (
            t("analysis.memory", nodes=len(compiled.nodes), mb=integer(round(mb))) if big else ""
        )
        self.results.refresh()

    def key(self) -> Key:
        n, seed = int(self.n.value or 100), int(self.seed.value or 0)
        return (self.model.text, str(self.scenario.value), str(self.output.value), n, seed)

    async def run(self) -> None:
        key, compiled = self.key(), self._compiled()
        self.status.clear()
        with self.status:
            ui.spinner(size="sm")
            ui.label(t("ui.running")).classes("rp-muted")
        self.button.disable()
        try:
            base = await run.io_bound(analysing.compute, key, compiled, key[2])
        except SimulationError as exc:
            self.status.clear()
            with self.status:
                ui.label(render(exc.issue)).classes("text-negative")
            return
        finally:
            self.button.enable()
        assert base is not None  # io_bound returns None only while the app shuts down
        self.status.clear()
        self.state.base = base
        self.results.refresh()

    @ui.refreshable_method
    def results(self) -> None:
        base = self.state.base
        if base is None:
            return
        if base.key != self.key():
            ui.label(t("analysis.stale")).classes("rp-muted")
            return
        results_view.horizon_hint(base.compiled.model, base.output)
        _tabs(base, self.state)


def page(session: Session) -> None:
    model = session.model
    if model is None:
        ui.label(t("ui.no_model")).classes("rp-muted")
        return
    checked = check_text(model.text)
    if checked.compiled is None:
        ui.label(t("ui.sim_blocked")).classes("text-negative")
        return
    AnalysisPage(session, model, checked).build()
