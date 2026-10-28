"""Streamlit building blocks shared by several pages."""

import dataclasses
import time
from collections.abc import Callable
from pathlib import Path

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from app.adapters import files, process, settings
from app.engine.simulate import simulate
from app.errors import InputError, ModelError, SimulationError
from app.messages import render, t
from app.model.compile import CompiledModel, content_hash, model_hash
from app.model.scenarios import effective_model, tree
from app.model.schema import BASIS, Model, OutputNode
from app.model.yaml_io import model_from_yaml, model_to_yaml
from app.present import figures
from app.present.references import Curve, has_reference, tutorial_reference
from app.present.results import correlation_rows, summaries_for
from app.present.text import (
    beyond_sentence,
    metric_rows,
    multimodal_hint,
    number,
    precision_hints,
    quantile_sentence,
    share_sentence,
    target_sentence,
    validity_line,
)
from app.present.validation import CheckResult
from app.ui import state

INFO_NOTICES = frozenset({"fit.deviation"})  # hints, not warnings (fit within 2 %)


def chart(figure: object, key: str, target: DeltaGenerator | None = None) -> None:
    """Show a plotly figure; plotly is untyped, so the call is wrapped once here."""
    place = target if target is not None else st.container()
    place.plotly_chart(figure, key=key)  # pyright: ignore[reportUnknownMemberType]


def table(headers: list[str], rows: list[tuple[str, ...]]) -> str:
    """A Markdown table (text the tests and screen readers can read); ``|`` in cells is escaped."""

    def line(cells: tuple[str, ...] | list[str]) -> str:
        return "| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |"

    lines = [line(headers), "|" + "---|" * len(headers)]
    lines += [line(row) for row in rows]
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
        return template, content_hash(effective_model(files.load_model(path), BASIS))
    except ModelError:
        return template, None


def _full_hash(text: str, compiled: CompiledModel) -> str:
    """Hash of the whole model text (with scenarios); the effective model's if unparsable."""
    try:
        return model_hash(model_from_yaml(text))
    except ModelError:
        return compiled.model_hash


def run_model(
    compiled: CompiledModel,
    text: str,
    n: int,
    seed: int,
    scenario: str,
    scenario_id: str = BASIS,
    notices: list[str] | None = None,
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
    meta = {
        **result.meta,
        "model_hash": _full_hash(text, compiled),
        "effective_hash": content_hash(compiled.model),
    }
    result = dataclasses.replace(result, meta=meta)
    template, original = template_and_hash(compiled, text)
    summaries = summaries_for(compiled, result)
    run = state.RunView(
        text,
        compiled,
        result,
        summaries,
        scenario,
        template,
        original,
        seconds,
        list(notices or []),
        scenario_id,
    )
    state.cache()[key] = run
    return run


def scenario_labels(checked: CheckResult) -> dict[str, str]:
    """Scenario names indented by their depth in the tree (for select boxes)."""
    if checked.model is None:
        return {sid: name for sid, (name, _) in checked.scenarios.items()}
    depth = dict(tree(checked.model))
    return {
        sid: "\u2003" * depth.get(sid, 0) + name for sid, (name, _) in checked.scenarios.items()
    }


def rewrite(model: Model) -> None:
    """Write an edited model back into the open model's draft (keeps the template comment).

    Call from widget callbacks only: they run before the editor widget exists in this run.
    """
    open_model = state.get_model()
    assert open_model is not None
    text = model_to_yaml(model)
    template = files.template_of(open_model.draft)
    if template:
        text = f"# Kopie von {template}\n{text}"
    open_model.draft = text
    st.session_state[state.EDITOR] = text


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
    if summary.horizon is not None and summary.beyond is not None:
        st.markdown(beyond_sentence(summary.horizon, summary.beyond, unit))
    for q in summary.quantiles:
        st.markdown(quantile_sentence(q, unit, summary.conf, summary.horizon))
    hint = multimodal_hint(x, summary, unit)
    if hint is not None:
        st.info(hint)
    if summary.beyond is not None and summary.beyond.p == 1.0:
        st.info(t("result.all_beyond"))
    st.markdown(table([t("ui.metric"), t("ui.value")], metric_rows(summary, unit)))
    for hint in precision_hints(summary):
        st.warning(hint)
    left, right = st.columns(2)
    chart(figures.histogram(x, unit, pdf_curves), f"hist_{output}", left)
    chart(figures.cdf(x, unit, cdf_curves), f"cdf_{output}", right)


def validity(run: state.RunView) -> None:
    st.caption(validity_line(run.result.meta, run.scenario))


def illustrative(model: Model) -> None:
    if model.illustrative:
        st.info(t("lesson.illustrative"))


def horizon_hint(model: Model, output: str) -> None:
    """Comparison and analysis work on raw values, also beyond an output's horizon."""
    node = model.nodes[output]
    if isinstance(node, OutputNode) and node.horizon is not None:
        name = node.name or output
        st.caption(t("result.horizon_raw", name=name, horizon=number(node.horizon)))


def correlations(run: state.RunView) -> None:
    """Target against achieved rank correlation of every group (M5 AK 1)."""
    rows = correlation_rows(run.compiled, run.result.correlations)
    if rows:
        st.subheader(t("result.corr_title"))
        headers = [
            t("result.corr_group"),
            t("result.corr_pair"),
            t("result.corr_target"),
            t("result.corr_achieved"),
        ]
        st.markdown(table(headers, rows))


def render_run(run: state.RunView) -> None:
    validity(run)
    illustrative(run.compiled.model)
    for notice in run.result.warnings:
        (st.info if notice.code in INFO_NOTICES else st.warning)(render(notice))
    for text in run.notices:
        st.warning(text)
    correlations(run)
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
