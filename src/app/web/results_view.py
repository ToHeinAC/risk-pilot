"""A run on screen (M7, Hex principle): the answer first as key-figure cards, then the reading
sentences next to the charts, then all metrics. Used by the results page and saved runs."""

# plotly ships without type stubs; its members are untyped for pyright.
# pyright: reportUnknownMemberType=false
from typing import Any

from nicegui import ui

from app.analysis.stats import Summary
from app.messages import render, t
from app.model.compile import content_hash
from app.model.schema import Model, OutputNode
from app.present import figures, reading
from app.present.references import Curve, has_reference, tutorial_reference
from app.present.results import correlation_rows
from app.present.text import (
    beyond_sentence,
    metric_rows,
    multimodal_hint,
    number,
    percent,
    precision_hints,
    quantile_sentence,
    share_sentence,
    target_sentence,
    validity_line,
)
from app.web import explain, theme
from app.web.session import RunView

INFO_NOTICES = frozenset({"fit.deviation"})  # hints, not warnings (fit within 2 %)


def note(text: str, kind: str = "info") -> None:
    """A hint line; ``kind`` is info, warning, error or success."""
    colour = {"info": "rp-muted", "warning": "text-warning", "error": "text-negative"}
    ui.label(text).classes(colour.get(kind, "text-positive"))


def horizon_hint(model: Model, output: str) -> None:
    """Comparison and analysis work on raw values, also beyond an output's horizon."""
    node = model.nodes[output]
    if isinstance(node, OutputNode) and node.horizon is not None:
        name = node.name or output
        note(t("result.horizon_raw", name=name, horizon=number(node.horizon)))


def metrics(rows: list[tuple[str, str]]) -> None:
    with ui.grid(columns=2).classes("w-full gap-x-6 gap-y-1 text-sm"):
        for label, shown in rows:
            explain.hint(ui.label(label).classes("rp-muted"), label)
            ui.label(shown).classes("rp-num text-right")


def card(kicker: str, value: str, caption: str = "") -> None:
    with ui.column().classes("rp-panel p-4 gap-1 flex-1 min-w-48"):
        explain.hint(ui.label(kicker).classes("rp-kicker"), kicker)
        ui.label(value).classes("rp-big")
        if caption:
            ui.label(caption).classes("rp-muted text-sm")


def table(headers: list[str], rows: list[tuple[str, ...]]) -> ui.table:
    columns = [
        {"name": str(i), "label": h, "field": str(i), "align": "left"}
        for i, h in enumerate(headers)
    ]
    data = [{str(i): cell for i, cell in enumerate(row)} for row in rows]
    shown = ui.table(columns=columns, rows=data, pagination=0)
    return shown.props("flat dense hide-pagination").classes("w-full")


def _unit(unit: str | None) -> str:
    return f" {unit}" if unit else ""


def _cards(summary: Summary, unit: str | None) -> None:
    with ui.row().classes("w-full gap-4"):
        if summary.target is not None:
            p = summary.target
            card(
                t("result.target_label"),
                percent(p.p),
                f"{number(p.lo * 100)} … {number(p.hi * 100)} %",
            )
        if summary.beyond is not None:
            card(t("result.beyond_label"), percent(summary.beyond.p))
        if summary.median is not None:
            card(t("result.median"), f"{number(summary.median)}{_unit(unit)}")
        if summary.quantiles:
            q = summary.quantiles[-1]
            label = t("result.quantile_label", pct=number(q.q * 100))
            card(label, f"{number(q.value)}{_unit(unit)}")


def _reference(run: RunView, output: str) -> tuple[list[Curve], list[Curve]]:
    own_hash = content_hash(run.compiled.model)
    reference = tutorial_reference(run.template, own_hash, run.original_hash, run.result.samples)
    if reference is None:
        if has_reference(run.template):
            note(t("ref.changed"))
        return [], []
    if reference.output != output:
        return [], []
    ks_text = t(
        "ref.ks",
        ks=f"{reference.ks:.4f}".replace(".", ","),
        n=f"{run.result.samples[output].size:,}".replace(",", " "),
        eps=f"{reference.eps:.4f}".replace(".", ","),
    )
    note(ks_text, "success" if reference.passed else "error")
    for line in reference.notes:
        ui.markdown(line)
    return reference.pdf, reference.cdf


def _sentences(run: RunView, output: str, summary: Summary, unit: str | None) -> None:
    target = run.compiled.nodes[output].target
    if target is not None and summary.target is not None:
        ui.label(target_sentence(target, summary.target, unit)).classes("rp-answer")
    if summary.horizon is not None and summary.beyond is not None:
        ui.label(beyond_sentence(summary.horizon, summary.beyond, unit)).classes("rp-answer")
    for q in summary.quantiles:
        ui.label(quantile_sentence(q, unit, summary.conf, summary.horizon)).classes("rp-answer")
    hint = multimodal_hint(run.result.samples[output], summary, unit)
    if hint is not None:
        note(hint)
    if summary.beyond is not None and summary.beyond.p == 1.0:
        note(t("result.all_beyond"))


def _charts(x: Any, unit: str | None, pdf: list[Curve], cdf: list[Curve]) -> None:
    with ui.row().classes("w-full gap-4 no-wrap max-lg:flex-wrap"):
        for fig in (figures.histogram(x, unit, pdf), figures.cdf(x, unit, cdf)):
            with ui.column().classes("rp-panel p-2 flex-1 min-w-0"):
                theme.plot(fig, 300)


def output(run: RunView, name: str) -> None:
    summary = run.summaries[name]
    unit = run.compiled.model.nodes[name].unit
    x = run.result.samples[name]
    found = reading.result(summary, run.compiled.model.nodes[name].name or name, unit)
    if summary.share is not None:
        share = summary.share
        card(t("result.share_label"), percent(share.p))

        def draw_share() -> None:
            ui.label(share_sentence(share)).classes("rp-answer")
            metrics(metric_rows(summary, unit))
            theme.plot(figures.share_bar(x), 260)

        explain.block("result", found, draw_share)
        return
    pdf, cdf = _reference(run, name)
    _cards(summary, unit)

    def draw() -> None:
        with ui.row().classes("w-full gap-4 no-wrap max-lg:flex-wrap items-start"):
            with ui.column().classes("flex-[3] min-w-0 gap-2"):
                ui.label(t("web.reading")).classes("rp-kicker")
                _sentences(run, name, summary, unit)
            with ui.column().classes("rp-panel p-4 flex-[2] min-w-64 gap-2"):
                ui.label(t("web.all_metrics")).classes("rp-kicker")
                metrics(metric_rows(summary, unit))
        for hint in precision_hints(summary):
            note(hint, "warning")
        _charts(x, unit, pdf, cdf)

    explain.block("result", found, draw)


def correlations(run: RunView) -> None:
    """Target against achieved rank correlation of every group (M5 AK 1)."""
    rows = correlation_rows(run.compiled, run.result.correlations)
    if rows:
        ui.label(t("result.corr_title")).classes("text-lg font-semibold")
        headers = [
            t("result.corr_group"),
            t("result.corr_pair"),
            t("result.corr_target"),
            t("result.corr_achieved"),
        ]
        table(headers, rows)


def show(run: RunView) -> None:
    ui.label(validity_line(run.result.meta, run.scenario)).classes("rp-muted text-sm")
    if run.compiled.model.illustrative:
        note(t("lesson.illustrative"), "warning")
    for notice in run.result.warnings:
        note(render(notice), "info" if notice.code in INFO_NOTICES else "warning")
    for text in run.notices:
        note(text, "warning")
    correlations(run)
    names = list(run.summaries)
    if len(names) == 1:
        output(run, names[0])
        return
    with ui.tabs().props("dense no-caps align=left").classes("w-full") as tabs:
        heads = [ui.tab(run.compiled.model.nodes[n].name or n) for n in names]
    with ui.tab_panels(tabs, value=heads[0]).classes("w-full bg-transparent"):
        for head, name in zip(heads, names, strict=True):
            with ui.tab_panel(head).classes("p-0 gap-4"):
                output(run, name)
