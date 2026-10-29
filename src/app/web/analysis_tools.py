"""Tornado and sweep tabs of the analysis: each a run of its own, remembered with its settings."""

from typing import Any

from nicegui import run, ui

from app.analysis.sweep import DEFAULT_K, plan_sweep, run_sweep, sweep_params, sweep_values
from app.analysis.tornado import DEFAULT_N, MANY_RUNS, Metric, Tornado, run_count, tornado
from app.engine.simulate import N_MAX
from app.errors import SimulationError
from app.messages import render, t
from app.present import structure
from app.present.text import integer, number
from app.web import results_view, theme
from app.web.analysing import AnalysisState, Base


def _metric_select(options: list[str], marker: str) -> ui.select:
    labels = {m: t(f"analysis.metric_{m}") for m in options}
    select = ui.select(labels, value=options[0], label=t("analysis.metric"))
    return select.props("outlined dense").classes("min-w-56").mark(marker)


def _last(stored: tuple[object, object] | None, base: Base) -> tuple[Any, ...] | None:
    """The settings key of a stored tornado or sweep, if it belongs to this analysis."""
    if stored is None:
        return None
    key = stored[0]
    assert isinstance(key, tuple)
    settings: tuple[Any, ...] = key  # pyright: ignore[reportUnknownVariableType]
    return settings if settings[0] == base.key else None


def _error(area: ui.column, text: str) -> None:
    area.clear()
    with area:
        ui.markdown(text).classes("text-negative")


class TornadoTab:
    def __init__(self, base: Base, state: AnalysisState) -> None:
        self.base, self.state = base, state

    def build(self) -> None:
        runs = run_count(self.base.compiled)
        if runs == 0:
            results_view.note(t("analysis.no_uncertain"))
            return
        metrics: list[str] = ["mean", "median"]
        if self.base.compiled.nodes[self.base.output].target is not None:
            metrics.append("target")
        with ui.row().classes("items-end gap-4"):
            self.metric = _metric_select(metrics, "tornado_metric")
            self.n = ui.number(t("analysis.tornado_n"), value=DEFAULT_N, min=100, max=N_MAX)
            self.n.props("outlined dense").mark("tornado_n")
            button = ui.button(t("analysis.tornado_run"), on_click=self.run)
            button.props("unelevated no-caps").mark("tornado_run")
        last = _last(self.state.tornado, self.base)
        if last is not None:  # back on the page: the settings of the shown result
            self.metric.value, self.n.value = last[1], last[2]
        count = ui.label().classes("rp-muted text-sm")
        count.bind_text_from(
            self.n, "value", lambda n: t("analysis.tornado_runs", runs=runs, n=integer(int(n or 0)))
        )
        if runs > MANY_RUNS:
            results_view.note(t("analysis.tornado_many"), "warning")
        self.area = ui.column().classes("w-full gap-2")
        self.metric.on_value_change(self.show)
        self.n.on_value_change(self.show)
        self.show()

    def key(self) -> object:
        return (self.base.key, self.metric.value, int(self.n.value or DEFAULT_N))

    async def run(self) -> None:
        metric: Metric = self.metric.value
        key = self.key()
        try:
            result = await run.io_bound(
                tornado,
                self.base.compiled,
                self.base.output,
                metric=metric,
                n=int(self.n.value or DEFAULT_N),
                seed=self.base.key[4],
            )
        except SimulationError as exc:
            _error(self.area, render(exc.issue))
            return
        assert result is not None  # io_bound returns None only while the app shuts down
        self.state.tornado = (key, result)
        self.show()

    def show(self) -> None:
        self.area.clear()
        stored = self.state.tornado
        if stored is None or stored[0] != self.key():
            return
        result: Tornado = stored[1]
        names = self.base.names
        with self.area:
            base_text = structure.tornado_base(result)
            ui.label(t("analysis.tornado_caption", base=base_text)).classes("rp-muted text-sm")
            headers = [
                t("analysis.col_node"),
                t("analysis.col_p10"),
                t("analysis.col_p90"),
                t("analysis.at_p10"),
                t("analysis.at_p90"),
                t("analysis.col_swing"),
            ]
            rows = structure.tornado_rows(result, names)
            results_view.table(headers, rows).mark("ana_tornado_table")
            theme.plot(structure.tornado_figure(result, names), 360)


class SweepTab:
    def __init__(self, base: Base, state: AnalysisState) -> None:
        self.base, self.state = base, state
        self.params = {
            f"{node}.{field}": (node, field, value)
            for node, field, value in sweep_params(base.compiled.model)
        }

    def build(self) -> None:
        if not self.params:
            results_view.note(t("analysis.sweep_none"))
            return
        names = self.base.names
        labels = {
            p: f"{names[node]} · {field} = {number(value)}"
            for p, (node, field, value) in self.params.items()
        }
        first = next(iter(labels))
        self.param = ui.select(labels, value=first, label=t("analysis.sweep_param"))
        self.param.props("outlined dense").classes("min-w-72").mark("sweep_param")
        with ui.row().classes("items-end gap-4"):
            self.lo = ui.number(t("analysis.sweep_from")).props("outlined dense").mark("sweep_from")
            self.hi = ui.number(t("analysis.sweep_to")).props("outlined dense").mark("sweep_to")
            self.k = ui.number(t("analysis.sweep_k"), value=DEFAULT_K, min=2, max=50, step=1)
            self.k.props("outlined dense").mark("sweep_k")
        self._metric_row()
        ui.button(t("analysis.sweep_run"), on_click=self.run).props("unelevated no-caps").mark(
            "sweep_run"
        )
        self.area = ui.column().classes("w-full gap-2")
        last = _last(self.state.sweep, self.base)
        if last is None:
            self._range()
        else:  # back on the page: the settings of the shown result
            _base, self.param.value, self.lo.value, self.hi.value, self.k.value, self.q.value = last
        self.param.on_value_change(self._range)
        for widget in (self.lo, self.hi, self.k, self.metric, self.q):
            widget.on_value_change(self.show)
        self.show()

    def _metric_row(self) -> None:
        output = self.base.compiled.nodes[self.base.output]
        metrics = ["mean", "median", "quantile"]
        if output.target is not None:
            metrics.append("target")
        if output.vtype.kind == "bool":
            metrics = ["share"]
        with ui.row().classes("items-end gap-4"):
            self.metric = _metric_select(metrics, "sweep_metric")
            self.q = ui.number(t("analysis.sweep_q"), value=0.9, min=0.01, max=0.99, step=0.05)
            self.q.props("outlined dense").mark("sweep_q")
            self.q.set_visibility(metrics != ["share"])

    def _range(self) -> None:
        value = self.params[str(self.param.value)][2]
        lo, hi = (value * 0.5, value * 1.5) if value else (0.0, 1.0)
        self.lo.value, self.hi.value = lo, hi

    def key(self) -> object:
        values = (self.lo.value, self.hi.value, self.k.value, self.q.value)
        return (self.base.key, self.param.value, *values)

    async def run(self) -> None:
        node, field, _value = self.params[str(self.param.value)]
        lo, hi = float(self.lo.value or 0), float(self.hi.value or 0)
        values = sweep_values(lo, hi, int(self.k.value or DEFAULT_K))
        plan = plan_sweep(self.base.compiled.model, node, field, values)
        if plan.invalid:
            lines = [f"- {number(v)}: {render(issue)}" for v, issue in plan.invalid]
            _error(self.area, "\n".join([t("analysis.sweep_invalid"), *lines]))
            return
        key, base = self.key(), self.base
        try:
            result = await run.io_bound(
                run_sweep,
                plan,
                base.output,
                n=base.key[3],
                seed=base.key[4],
                quantile=float(self.q.value or 0.9),
            )
        except SimulationError as exc:
            _error(self.area, render(exc.issue))
            return
        assert result is not None  # io_bound returns None only while the app shuts down
        self.state.sweep = (key, result)
        self.show()

    def show(self) -> None:
        self.area.clear()
        stored = self.state.sweep
        if stored is None or stored[0] != self.key():
            return
        metric = str(self.metric.value)
        node, field, _value = self.params[str(self.param.value)]
        series = structure.sweep_series(stored[1], metric)
        share = metric in ("target", "share")
        headers = [t("analysis.col_value"), t("analysis.col_estimate"), t("analysis.col_interval")]
        x_title = f"{self.base.names[node]} · {field}"
        figure: Any = structure.sweep_figure(series, x_title, t(f"analysis.metric_{metric}"))
        with self.area:
            results_view.table(headers, structure.sweep_rows(series, share)).mark("ana_sweep_table")
            theme.plot(figure, 340)
