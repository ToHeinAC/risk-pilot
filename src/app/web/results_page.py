"""Results of the last run: the run on screen, saving it, downloads."""

from collections.abc import Callable

from nicegui import ui

from app.adapters import export as export_adapter
from app.messages import t
from app.present import export
from app.present.text import number
from app.web import results_view, running
from app.web.session import RunView, Session

LARGE = 100 * 1024 * 1024


def _download(label: str, build: Callable[[], bytes], file: str, marker: str) -> None:
    """The file is built only on click (M6 E9: nothing is written to data/)."""
    ui.button(label, icon="download", on_click=lambda: ui.download.content(build(), file)).props(
        "outline no-caps"
    ).mark(marker)


def _exports(run: RunView) -> None:
    report = export.Report(
        run.compiled, run.result, run.summaries, run.scenario, run.model_text, run.scenario_id
    )

    def name(kind: str) -> str:
        return export.file_name(run.compiled.model.model, run.scenario_id, kind)

    ui.label(t("export.title")).classes("text-lg font-semibold")
    with ui.row().classes("gap-2"):
        _download(
            t("export.csv"),
            lambda: export.metrics_csv(report).encode("utf-8"),
            name("kennzahlen.csv"),
            "export_csv",
        )
        _download(
            t("export.parquet"),
            lambda: export_adapter.samples_parquet(run.result, run.scenario_id),
            name("stichproben.parquet"),
            "export_parquet",
        )
        _download(
            t("export.html"),
            lambda: export.report_html(report).encode("utf-8"),
            name("bericht.html"),
            "export_html",
        )


def _save(run: RunView) -> None:
    size = sum(int(x.nbytes) for x in run.result.samples.values())
    if size > LARGE:
        results_view.note(t("ui.run_large", mb=number(size / 1024 / 1024)), "warning")
    with ui.row().classes("items-center gap-3"):
        saved = ui.label()

        def save() -> None:
            saved.text = t("ui.run_saved", name=running.save(run).name)

        ui.button(t("ui.save_run"), icon="save", on_click=save).props("unelevated no-caps").mark(
            "save_run"
        )
        saved.move(target_index=-1)


def page(session: Session) -> None:
    ui.label(t("ui.page_ergebnisse")).classes("text-2xl font-semibold")
    run = session.run
    if run is None:
        ui.label(t("ui.no_run")).classes("rp-muted")
        ui.button(t("ui.page_simulation"), on_click=lambda: ui.navigate.to("/simulation")).props(
            "flat no-caps"
        )
        return
    results_view.show(run)
    _save(run)
    _exports(run)
