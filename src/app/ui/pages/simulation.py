"""Simulation: N and seed, then run."""

import streamlit as st

from app.engine.simulate import N_MAX
from app.messages import t
from app.present.text import decimal, integer
from app.present.validation import check_text
from app.ui import state, views


def body() -> None:
    model = state.get_model()
    if model is None:
        st.info(t("ui.no_model"))
        return
    st.title(t("ui.page_simulation"))
    compiled = check_text(model.text).compiled
    if compiled is None:
        st.error(t("ui.sim_blocked"))
        return
    defaults = compiled.model.settings
    n = st.number_input(
        t("ui.n"), min_value=1, max_value=N_MAX, value=defaults.n, step=1000, key="sim_n"
    )
    seed = st.number_input(t("ui.seed"), min_value=0, value=defaults.seed, step=1, key="sim_seed")
    if st.button(t("ui.simulate"), key="sim_run", type="primary"):
        with st.spinner(t("ui.running")):
            run = views.run_model(compiled, model.text, int(n), int(seed), t("ui.main_scenario"))
        if run is not None:
            state.set_run(run)
            st.success(t("ui.sim_done", n=integer(int(n)), seconds=decimal(run.seconds, 2)))
    st.page_link("pages/ergebnisse.py", label=t("ui.to_results"))


views.run_page(body)
