"""Streamlit building blocks shared by several pages."""

import time
from collections.abc import Callable
from pathlib import Path

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from app.adapters import files, process, settings
from app.engine.simulate import simulate
from app.errors import InputError, ModelError, SimulationError
from app.messages import render, t
from app.model.compile import CompiledModel, content_hash
from app.present import figures
from app.present.references import Curve, has_reference, tutorial_reference
from app.present.results import summaries_for
from app.present.text import (
    metric_rows,
    precision_hints,
    quantile_sentence,
    share_sentence,
    target_sentence,
    validity_line,
)
from app.ui import state


def chart(figure: object, key: str, target: DeltaGenerator | None = None) -> None:
    """Show a plotly figure; plotly is untyped, so the call is wrapped once here."""
    place = target if target is not None else st.container()
    place.plotly_chart(figure, key=key)  # pyright: ignore[reportUnknownMemberType]


def table(headers: list[str], rows: list[tuple[str, ...]]) -> str:
    """A Markdown table (text the tests and screen readers can read)."""
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines)


def is_example(path: Path) -> bool:
    return settings.examples_dir().resolve() in path.resolve().parents


def open_model(path: Path) -> None:
    state.set_model(state.OpenModel(str(path), files.read_text(path), readonly=is_example(path)))


def run_page(body: Callable[[], None]) -> None:
    """Run a page; an unexpected error becomes a German message, the app keeps running.

    Streamlit's own control flow (st.stop, st.rerun, st.switch_page) derives from
    BaseException and passes through untouched.
    """
    sidebar_exit()
    try:
        body()
    except Exception as exc:  # last line of defence, shown to the user
        st.error(t("ui.unexpected", detail=f"{type(exc).__name__}: {exc}"))


def template_and_hash(compiled: CompiledModel, text: str) -> tuple[str, str | None]:
    """The tutorial this model is (a copy of) and that tutorial's content hash, if any."""
    template = files.template_of(text) or compiled.model.model
    path = settings.examples_dir() / f"{template}.yaml"
    if not path.is_file():
        return template, None
    try:
        return template, content_hash(files.load_model(path))
    except ModelError:
        return template, None


def run_model(
    compiled: CompiledModel, text: str, n: int, seed: int, scenario: str
) -> state.RunView | None:
    """Simulate (or reuse the cached run); errors are shown, never raised."""
    key = (compiled.model_hash, n, seed)
    cached = state.cache().get(key)
    if cached is not None and cached.scenario == scenario:
        return cached
    started = time.perf_counter()
    try:
        result = simulate(compiled, n=n, seed=seed)
    except SimulationError as exc:
        st.error(render(exc.issue))
        return None
    seconds = time.perf_counter() - started
    template, original = template_and_hash(compiled, text)
    summaries = summaries_for(compiled, result)
    run = state.RunView(text, compiled, result, summaries, scenario, template, original, seconds)
    state.cache()[key] = run
    return run


def copy_form(source: Path, key: str, default: str) -> None:
    """Text field for the new name plus "copy as template"; never overwrites."""
    new_id = st.text_input(t("ui.copy_name"), value=default, key=f"copy_id_{key}")
    if st.button(t("ui.copy"), key=f"copy_{key}"):
        try:
            target = files.copy_model(source, settings.models_dir(), new_id.strip())
        except InputError as exc:
            st.error(render(exc.issue))
        else:
            st.success(t("ui.copied", name=target.stem))


def _output_name(run: state.RunView, output: str) -> tuple[str, str | None]:
    node = run.compiled.model.nodes[output]
    return node.name or output, node.unit


def _reference_block(run: state.RunView, output: str) -> tuple[list[Curve], list[Curve]]:
    own_hash = content_hash(run.compiled.model)
    reference = tutorial_reference(run.template, own_hash, run.original_hash, run.result.samples)
    if reference is None:
        if has_reference(run.template):
            st.info(t("ref.changed"))
        return [], []
    if reference.output != output:
        return [], []
    ks_text = t(
        "ref.ks",
        ks=f"{reference.ks:.4f}".replace(".", ","),
        n=f"{run.result.samples[output].size:,}".replace(",", " "),
        eps=f"{reference.eps:.4f}".replace(".", ","),
    )
    (st.success if reference.passed else st.error)(ks_text)
    for note in reference.notes:
        st.markdown(note)
    return reference.pdf, reference.cdf


def render_output(run: state.RunView, output: str) -> None:
    summary = run.summaries[output]
    _, unit = _output_name(run, output)
    x = run.result.samples[output]
    if summary.share is not None:
        st.markdown(share_sentence(summary.share))
        st.markdown(table([t("ui.metric"), t("ui.value")], metric_rows(summary, unit)))
        chart(figures.share_bar(x), f"share_{output}")
        return
    pdf_curves, cdf_curves = _reference_block(run, output)
    target = run.compiled.nodes[output].target
    if target is not None and summary.target is not None:
        st.markdown(target_sentence(target, summary.target, unit))
    for q in summary.quantiles:
        st.markdown(quantile_sentence(q, unit, summary.conf))
    st.markdown(table([t("ui.metric"), t("ui.value")], metric_rows(summary, unit)))
    for hint in precision_hints(summary):
        st.warning(hint)
    left, right = st.columns(2)
    chart(figures.histogram(x, unit, pdf_curves), f"hist_{output}", left)
    chart(figures.cdf(x, unit, cdf_curves), f"cdf_{output}", right)


def validity(run: state.RunView) -> None:
    st.caption(validity_line(run.result.meta, run.scenario))


def render_run(run: state.RunView) -> None:
    validity(run)
    for notice in run.result.warnings:
        st.warning(render(notice))
    for text in run.notices:
        st.warning(text)
    outputs = list(run.summaries)
    tabs = st.tabs([_output_name(run, o)[0] for o in outputs])
    for tab, output in zip(tabs, outputs, strict=True):
        with tab:
            render_output(run, output)


def sidebar_exit() -> None:
    """Exit button: asks first, then sends SIGTERM to this process only."""
    with st.sidebar:
        if st.button(t("ui.exit"), key="exit"):
            st.session_state["confirm_exit"] = True
        if not st.session_state.get("confirm_exit"):
            return
        model = state.get_model()
        if model is not None and model.dirty:
            st.warning(t("ui.exit_unsaved"))
        st.warning(t("ui.exit_question"))
        if st.button(t("ui.exit_confirm"), key="exit_confirm", type="primary"):
            st.info(t("ui.exit_done"))
            process.shutdown()
        if st.button(t("ui.exit_cancel"), key="exit_cancel"):
            st.session_state["confirm_exit"] = False
            st.rerun()
