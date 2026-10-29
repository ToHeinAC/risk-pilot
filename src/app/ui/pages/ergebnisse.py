"""Results of the last run, and saving it."""

import streamlit as st

from app.adapters import export as export_adapter
from app.adapters import runs, settings
from app.analysis.stats import summary_to_dict
from app.messages import t
from app.model.compile import content_hash
from app.present import export
from app.present.text import number
from app.ui import state, views

LARGE = 100 * 1024 * 1024


def _exports(run: state.RunView) -> None:
    """Downloads; the files are built only on click (E9: nothing is written to data/)."""
    report = export.Report(
        run.compiled, run.result, run.summaries, run.scenario, run.model_text, run.scenario_id
    )

    def name(kind: str) -> str:
        return export.file_name(run.compiled.model.model, run.scenario_id, kind)

    st.subheader(t("export.title"))
    left, middle, right = st.columns(3)
    left.download_button(
        t("export.csv"),
        lambda: export.metrics_csv(report),
        name("kennzahlen.csv"),
        "text/csv",
        key="export_csv",
        on_click="ignore",
    )
    middle.download_button(
        t("export.parquet"),
        lambda: export_adapter.samples_parquet(run.result, run.scenario_id),
        name("stichproben.parquet"),
        "application/vnd.apache.parquet",
        key="export_parquet",
        on_click="ignore",
    )
    right.download_button(
        t("export.html"),
        lambda: export.report_html(report),
        name("bericht.html"),
        "text/html",
        key="export_html",
        on_click="ignore",
    )


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
        extra = {
            "scenario": run.scenario,
            "scenario_id": run.scenario_id,
            "scenario_name": run.scenario,
            "effective_hash": content_hash(run.compiled.model),
            "correlations": {g: m.tolist() for g, m in run.result.correlations.items()},
        }
        path = runs.save_run(
            settings.runs_dir(),
            run.result.meta,
            run.model_text,
            run.result.samples,
            summaries,
            extra,
        )
        st.success(t("ui.run_saved", name=path.name))
    _exports(run)


views.run_page(body)
