"""Results of the last run, and saving it."""

import streamlit as st

from app.adapters import runs, settings
from app.analysis.stats import summary_to_dict
from app.messages import t
from app.present.text import number
from app.ui import state, views

LARGE = 100 * 1024 * 1024


def body() -> None:
    st.title(t("ui.page_ergebnisse"))
    run = state.get_run()
    if run is None:
        st.info(t("ui.no_run"))
        return
    views.render_run(run)
    size = sum(int(x.nbytes) for x in run.result.samples.values())
    if size > LARGE:
        st.warning(t("ui.run_large", mb=number(size / 1024 / 1024)))
    if st.button(t("ui.save_run"), key="save_run"):
        summaries = {k: summary_to_dict(v) for k, v in run.summaries.items()}
        extra = {"scenario": run.scenario}
        path = runs.save_run(
            settings.runs_dir(),
            run.result.meta,
            run.model_text,
            run.result.samples,
            summaries,
            extra,
        )
        st.success(t("ui.run_saved", name=path.name))


views.run_page(body)
