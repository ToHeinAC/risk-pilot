"""Comparison of scenarios: same seed, paired differences."""

from typing import cast

import streamlit as st

from app.analysis.compare import compare
from app.messages import t
from app.model.schema import BASIS, OutputNode
from app.present import figures
from app.present.compare import better_sentence, compare_rows, d_rows, direction_sentence
from app.present.validation import check_text
from app.ui import state, views

RUNS = "compare_runs"


def _output_tab(runs: dict[str, state.RunView], ref: str, output: str) -> None:
    base = runs[ref]
    node = base.compiled.model.nodes[output]
    unit = node.unit
    better = node.better if isinstance(node, OutputNode) else None
    a = base.result.samples[output]
    samples = {run.scenario: run.result.samples[output] for run in runs.values()}
    for sid, run in runs.items():
        if sid == ref:
            continue
        st.subheader(t("compare.pair", b=run.scenario, a=base.scenario))
        c = compare(
            a, run.result.samples[output], target=base.compiled.nodes[output].target, better=better
        )
        headers = [t("ui.metric"), base.scenario, run.scenario, t("compare.diff")]
        st.markdown(views.table(headers, compare_rows(c, unit)))
        sentence = better_sentence(c, base.scenario, run.scenario)
        st.markdown(sentence or direction_sentence(c, base.scenario, run.scenario))
        if c.kind == "num":
            st.caption(t("compare.d_table"))
            st.markdown(views.table([t("ui.metric"), t("ui.value")], d_rows(c, unit)))
            st.caption(t("compare.d_caption"))
            views.chart(figures.histogram(c.d, unit, []), f"d_{output}_{sid}")
    if base.summaries[output].kind == "num":
        views.chart(figures.compare_cdfs(samples, unit), f"cdfs_{output}")


def body() -> None:
    st.title(t("ui.page_vergleich"))
    open_model = state.get_model()
    if open_model is None:
        st.info(t("ui.no_model"))
        return
    checked = check_text(open_model.draft)
    scenarios = checked.scenarios
    if len(scenarios) < 2:
        st.info(t("compare.need_two"))
        return
    ids = list(scenarios)
    ref = str(
        st.selectbox(
            t("compare.ref"), ids, format_func=lambda s: scenarios[s][0], key="compare_ref"
        )
    )
    others = st.multiselect(
        t("compare.others"),
        [s for s in ids if s != ref],
        format_func=lambda s: scenarios[s][0],
        max_selections=3,
        key="compare_others",
    )
    settings = scenarios[BASIS][1].model.settings
    n = int(
        st.number_input(
            t("ui.n"),
            min_value=100,
            max_value=2_000_000,
            value=settings.n,
            step=1000,
            key="compare_n",
        )
    )
    seed = int(st.number_input(t("ui.seed"), min_value=0, value=settings.seed, key="compare_seed"))
    st.caption(t("compare.same_seed"))
    if st.button(t("compare.run"), key="compare_run", type="primary", disabled=not others):
        runs: dict[str, state.RunView] = {}
        for sid in [ref, *others]:
            name, compiled = scenarios[sid]
            run = views.run_model(compiled, open_model.draft, n, seed, name, sid)
            if run is None:
                return
            runs[sid] = run
        st.session_state[RUNS] = (open_model.draft, ref, runs)
    stored = st.session_state.get(RUNS)
    if stored is None:
        return
    draft, ref, runs = cast(tuple[str, str, dict[str, state.RunView]], stored)
    if draft != open_model.draft:  # the model changed since: old results no longer apply
        st.info(t("compare.stale"))
        return
    views.validity(runs[ref])
    outputs = list(runs[ref].summaries)
    tabs = st.tabs([runs[ref].compiled.model.nodes[o].name or o for o in outputs])
    for tab, output in zip(tabs, outputs, strict=True):
        with tab:
            _output_tab(runs, ref, output)


views.run_page(body)
