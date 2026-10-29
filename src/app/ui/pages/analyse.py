"""Analysis: structure of one scenario – graph, criticality, tornado, sweep, Spearman, risks."""

from collections.abc import Mapping
from typing import Any, cast

import streamlit as st

from app.analysis.sweep import DEFAULT_K, plan_sweep, run_sweep, sweep_params, sweep_values
from app.analysis.tornado import DEFAULT_N, MANY_RUNS, Metric, Tornado, run_count, tornado
from app.engine.simulate import N_MAX
from app.errors import SimulationError
from app.messages import render, t
from app.model.compile import CompiledModel
from app.model.graph import edges
from app.present import structure
from app.present.text import integer, number
from app.present.validation import check_text, scenario_labels
from app.ui import state, views
from app.web import analysing
from app.web.analysing import MEMORY_HINT_MB, Base, Key

BASE = "analysis_base"
TORNADO = "analysis_tornado"
SWEEP = "analysis_sweep"


def _compute(key: Key, compiled: CompiledModel, output: str) -> Base | None:
    try:
        return analysing.compute(key, compiled, output)
    except SimulationError as exc:
        st.error(render(exc.issue))
        return None


def _graph_tab(base: Base) -> None:
    choices = {
        "sensitivity": t("analysis.color_sensitivity"),
        "criticality": t("analysis.color_criticality"),
        "why": t("analysis.color_why"),
    }
    mode = str(
        st.selectbox(
            t("analysis.color"), list(choices), format_func=lambda c: choices[c], key="graph_color"
        )
    )
    model = base.compiled.model
    colors: dict[str, float] = {
        "sensitivity": {r.node: abs(r.rho) for r in base.rho if r.rho is not None},
        "criticality": {node: p.p for node, p in base.crit.indices},
        "why": structure.missing_why(model),
    }[mode]
    figure = structure.graph_figure(model, edges(model), colors, choices[mode], base.output)
    views.chart(figure, "analysis_graph")
    st.caption(t("analysis.graph_caption"))


def _criticality_tab(base: Base) -> None:
    crit = base.crit
    if not crit.selects_path:
        st.info(t("analysis.crit_no_extremum"))
    for node, p in crit.indices:
        if base.compiled.nodes[node].type != "derived":
            st.markdown(structure.criticality_sentence(base.names[node], p))
    st.caption(t("analysis.crit_note"))
    headers = [t("analysis.col_node"), t("analysis.col_index")]
    st.markdown(views.table(headers, structure.criticality_rows(crit, base.names)))
    if crit.indices:
        views.chart(structure.criticality_figure(crit, base.names), "analysis_crit")
    st.subheader(t("analysis.constellations"))
    headers = [t("analysis.col_constellation"), t("analysis.col_share")]
    st.markdown(views.table(headers, structure.constellation_rows(crit, base.names)))


def _tornado_tab(base: Base) -> None:
    runs = run_count(base.compiled)
    if runs == 0:
        st.info(t("analysis.no_uncertain"))
        return
    metrics: list[Metric] = ["mean", "median"]
    if base.compiled.nodes[base.output].target is not None:
        metrics.append("target")
    metric: Metric = st.selectbox(
        t("analysis.metric"),
        metrics,
        format_func=lambda m: t(f"analysis.metric_{m}"),
        key="tornado_metric",
    )
    n = int(
        st.number_input(t("analysis.tornado_n"), 100, N_MAX, DEFAULT_N, step=1000, key="tornado_n")
    )
    st.caption(t("analysis.tornado_runs", runs=runs, n=integer(n)))
    if runs > MANY_RUNS:
        st.warning(t("analysis.tornado_many"))
    key = (base.key, metric, n)
    if st.button(t("analysis.tornado_run"), key="tornado_run"):
        try:
            st.session_state[TORNADO] = (
                key,
                tornado(base.compiled, base.output, metric=metric, n=n, seed=base.key[4]),
            )
        except SimulationError as exc:
            st.error(render(exc.issue))
    stored = st.session_state.get(TORNADO)
    if stored is not None and stored[0] == key:
        _tornado_result(cast(Tornado, stored[1]), base.names)


def _tornado_result(result: Tornado, names: Mapping[str, str]) -> None:
    base_text = structure.tornado_base(result)
    st.caption(t("analysis.tornado_caption", base=base_text))
    headers = [
        t("analysis.col_node"),
        t("analysis.col_p10"),
        t("analysis.col_p90"),
        t("analysis.at_p10"),
        t("analysis.at_p90"),
        t("analysis.col_swing"),
    ]
    st.markdown(views.table(headers, structure.tornado_rows(result, names)))
    views.chart(structure.tornado_figure(result, names), "analysis_tornado")


def _sweep_tab(base: Base) -> None:
    params = {
        f"{node}.{field}": (node, field, value)
        for node, field, value in sweep_params(base.compiled.model)
    }
    if not params:
        st.info(t("analysis.sweep_none"))
        return
    pick = str(
        st.selectbox(
            t("analysis.sweep_param"),
            list(params),
            format_func=lambda p: (
                f"{base.names[params[p][0]]} · {params[p][1]} = {number(params[p][2])}"
            ),
            key="sweep_param",
        )
    )
    node, field, value = params[pick]
    left, middle, right = st.columns(3)
    lo, hi = (value * 0.5, value * 1.5) if value else (0.0, 1.0)
    lo = float(left.number_input(t("analysis.sweep_from"), value=lo, key=f"sweep_from_{pick}"))
    hi = float(middle.number_input(t("analysis.sweep_to"), value=hi, key=f"sweep_to_{pick}"))
    k = int(right.number_input(t("analysis.sweep_k"), 2, 50, DEFAULT_K, key="sweep_k"))
    metric, q = _sweep_metric(base)
    key = (base.key, pick, lo, hi, k, q)
    if st.button(t("analysis.sweep_run"), key="sweep_run"):
        _run_sweep(base, node, field, sweep_values(lo, hi, k), key, q)
    stored = st.session_state.get(SWEEP)
    if stored is not None and stored[0] == key:
        _sweep_result(stored[1], metric, f"{base.names[node]} · {field}")


def _sweep_metric(base: Base) -> tuple[str, float]:
    if base.compiled.nodes[base.output].vtype.kind == "bool":
        return "share", 0.9
    metrics = ["mean", "median", "quantile"]
    if base.compiled.nodes[base.output].target is not None:
        metrics.append("target")
    metric = str(
        st.selectbox(
            t("analysis.metric"),
            metrics,
            format_func=lambda m: t(f"analysis.metric_{m}"),
            key="sweep_metric",
        )
    )
    q = float(st.number_input(t("analysis.sweep_q"), 0.01, 0.99, 0.9, key="sweep_q"))
    return metric, q


def _run_sweep(
    base: Base, node: str, field: str, values: tuple[float, ...], key: object, q: float
) -> None:
    plan = plan_sweep(base.compiled.model, node, field, values)
    if plan.invalid:
        lines = [f"- {number(v)}: {render(issue)}" for v, issue in plan.invalid]
        st.error("\n".join([t("analysis.sweep_invalid"), *lines]))
        return
    try:
        result = run_sweep(plan, base.output, n=base.key[3], seed=base.key[4], quantile=q)
    except SimulationError as exc:
        st.error(render(exc.issue))
        return
    st.session_state[SWEEP] = (key, result)


def _sweep_result(result: Any, metric: str, x_title: str) -> None:
    series = structure.sweep_series(result, metric)
    share = metric in ("target", "share")
    headers = [t("analysis.col_value"), t("analysis.col_estimate"), t("analysis.col_interval")]
    st.markdown(views.table(headers, structure.sweep_rows(series, share)))
    views.chart(
        structure.sweep_figure(series, x_title, t(f"analysis.metric_{metric}")), "analysis_sweep"
    )


def _rho_tab(base: Base) -> None:
    st.info(t("analysis.rho_caption"))
    headers = [t("analysis.col_node"), t("analysis.col_rho"), t("analysis.col_interval")]
    st.markdown(views.table(headers, structure.rho_rows(base.rho, base.names)))


def _risk_tab(base: Base) -> None:
    if not base.risks:
        st.info(t("analysis.no_events"))
        return
    st.warning(t("analysis.risk_caption"))
    unit = base.compiled.model.nodes[base.output].unit
    headers = [t("analysis.col_node"), t("analysis.col_p"), t("analysis.col_diff")]
    st.markdown(views.table(headers, structure.risk_rows(base.risks, base.names, unit)))
    views.chart(structure.risk_figure(base.risks, base.names, unit), "analysis_risk")


def _settings(compiled: CompiledModel, names: Mapping[str, str]) -> tuple[str, int, int]:
    outputs = [i for i, node in compiled.nodes.items() if node.type == "output"]
    output = str(
        st.selectbox(
            t("analysis.output"), outputs, format_func=lambda o: names[o], key="ana_output"
        )
    )
    defaults = compiled.model.settings
    n = int(st.number_input(t("ui.n"), 100, N_MAX, defaults.n, step=1000, key="ana_n"))
    seed = int(st.number_input(t("ui.seed"), min_value=0, value=defaults.seed, key="ana_seed"))
    mb = analysing.memory_mb(compiled, n)
    if mb > MEMORY_HINT_MB:
        st.warning(t("analysis.memory", nodes=len(compiled.nodes), mb=integer(round(mb))))
    return output, n, seed


def body() -> None:
    st.title(t("ui.page_analyse"))
    open_model = state.get_model()
    if open_model is None:
        st.info(t("ui.no_model"))
        return
    checked = check_text(open_model.draft)
    if checked.compiled is None:
        st.error(t("ui.sim_blocked"))
        return
    st.caption(t("analysis.intro"))
    with st.expander(t("analysis.guide_label")):
        st.markdown(t("analysis.guide"))
    labels = scenario_labels(checked)
    sid = str(
        st.selectbox(
            t("ui.scenario"),
            list(checked.scenarios),
            format_func=lambda s: labels[s],
            key="ana_scenario",
        )
    )
    compiled = checked.scenarios[sid][1]
    output, n, seed = _settings(compiled, analysing.names(compiled))
    key: Key = (open_model.draft, sid, output, n, seed)
    if st.button(t("analysis.run"), key="ana_run", type="primary"):
        st.session_state[BASE] = _compute(key, compiled, output)
    base = cast(Base | None, st.session_state.get(BASE))
    if base is None:
        return
    if base.key != key:
        st.info(t("analysis.stale"))
        return
    views.horizon_hint(base.compiled.model, base.output)
    _tabs(base)


TABS = ("graph", "crit", "tornado", "sweep", "rho", "risk")


def _tabs(base: Base) -> None:
    tabs = st.tabs([t(f"analysis.tab_{name}") for name in TABS])
    pages = (_graph_tab, _criticality_tab, _tornado_tab, _sweep_tab, _rho_tab, _risk_tab)
    for tab, name, page in zip(tabs, TABS, pages, strict=True):
        with tab:
            with st.expander(t("analysis.help_label")):
                st.markdown(t(f"analysis.help_{name}"))
            page(base)


views.run_page(body)
