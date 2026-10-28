"""Model: YAML editor with live validation."""

from pathlib import Path

import streamlit as st

from app.adapters import files, settings
from app.errors import InputError
from app.messages import render, t
from app.model.edits import to_empirical, to_piecewise
from app.model.scenarios import mark_unknown_inactive
from app.model.yaml_io import model_from_yaml
from app.present.validation import CheckResult, check_text
from app.ui import state, views


def _show_check(result: CheckResult) -> None:
    if result.hint:
        st.info(result.hint)
    elif result.rows:
        st.error(result.status)
        for row in result.rows:
            where = t("ui.at_line", line=row.line) if row.line else ""
            excerpt = f"\n\n`{row.excerpt}`" if row.excerpt else ""
            st.error(f"{row.message}{where}{excerpt}")
    else:
        st.success(result.status)
        headers = [
            t("ui.col_id"),
            t("ui.col_type"),
            t("ui.col_name"),
            t("ui.col_unit"),
            t("ui.col_detail"),
        ]
        rows = [
            (r.node, t(f"type.{r.type}"), r.name, r.unit, f"`{r.detail}`")
            for r in result.node_table
        ]
        st.markdown(views.table(headers, rows))


def _to_piecewise(node_id: str) -> None:
    model = state.get_model()
    assert model is not None
    p0 = float(st.session_state[f"piecewise_p0_{node_id}"])
    p100 = float(st.session_state[f"piecewise_p100_{node_id}"])
    try:
        views.rewrite(to_piecewise(model_from_yaml(model.draft), node_id, p0, p100))
    except InputError as exc:
        st.session_state["edit_error"] = render(exc.issue)


def _fit_offers(result: CheckResult, readonly: bool) -> None:
    """Quantile fits that miss by more than 2 %: offer the piecewise distribution instead."""
    if result.compiled is None or result.model is None:
        return
    for notice in result.compiled.notices:
        (st.warning if notice.code == "fit.conflict" else st.info)(render(notice))
        node_id = notice.node_id
        if notice.code != "fit.conflict" or readonly or node_id is None:
            continue
        left, right = st.columns(2)
        p0 = left.number_input(t("model.p0"), value=None, key=f"piecewise_p0_{node_id}")
        p100 = right.number_input(t("model.p100"), value=None, key=f"piecewise_p100_{node_id}")
        st.button(
            t("model.to_piecewise"),
            key=f"to_piecewise_{node_id}",
            on_click=_to_piecewise,
            args=(node_id,),
            disabled=p0 is None or p100 is None,  # the user sets the bounds, the app does not
        )


def _csv_import(result: CheckResult) -> None:
    """Values of a CSV column into an empirical distribution (own models only)."""
    if result.model is None:
        return
    targets = [i for i, n in result.model.nodes.items() if n.type == "uncertain"]
    if not targets:
        return
    with st.expander(t("model.csv_title")):
        upload = st.file_uploader(t("model.csv_file"), type=["csv", "txt"], key="csv_file")
        if upload is None:
            return
        data = upload.getvalue()
        try:
            columns = files.csv_columns(data)
        except InputError as exc:
            st.error(render(exc.issue))
            return
        column = st.selectbox(t("model.csv_column"), columns, key="csv_column")
        node_id = st.selectbox(t("model.csv_node"), targets, key="csv_node")
        st.button(
            t("model.csv_import"),
            key="csv_import",
            on_click=_import_csv,
            args=(data, str(column), str(node_id)),
        )
        done = st.session_state.pop("csv_done", None)
        if done:
            st.success(done)


def _import_csv(data: bytes, column: str, node_id: str) -> None:
    """Widget callback: it runs before the editor exists, so the draft may be rewritten."""
    model = state.get_model()
    assert model is not None
    try:
        values, skipped = files.csv_column(data, column)
        views.rewrite(to_empirical(model_from_yaml(model.draft), node_id, values))
    except InputError as exc:
        st.session_state["edit_error"] = render(exc.issue)
        return
    st.session_state["csv_done"] = t("model.csv_done", n=len(values), skipped=skipped, node=node_id)


def _hints(result: CheckResult, readonly: bool) -> None:
    """Validation, notices and the edits the notices offer."""
    if result.model is not None:
        views.illustrative(result.model)
    _show_check(result)
    for notice in result.notices:
        st.info(notice)
    error = st.session_state.pop("edit_error", None)
    if error:
        st.error(error)
    _fit_offers(result, readonly)
    if readonly:
        return
    _csv_import(result)
    if result.unknown_nodes:
        st.button(t("scen.mark_inactive"), key="mark_inactive", on_click=_mark_inactive)


def _mark_inactive() -> None:
    model = state.get_model()
    assert model is not None
    views.rewrite(mark_unknown_inactive(model_from_yaml(model.draft)))


def _save(model: state.OpenModel, path: Path, result: CheckResult, force: bool) -> None:
    expected = None if force else files.text_hash(model.file_text)
    try:
        files.save_model_text(path, model.text, expected)
    except InputError as exc:
        st.error(render(exc.issue))
        st.session_state["save_conflict"] = True
        return
    st.session_state["save_conflict"] = False
    model.file_text = model.text
    st.success(t("ui.saved"))
    if result.rows:
        st.warning(t("ui.saved_invalid"))


def _actions(model: state.OpenModel, path: Path, result: CheckResult) -> None:
    left, right = st.columns(2)
    if left.button(t("ui.save"), key="save_model", type="primary"):
        _save(model, path, result, force=False)
    if st.session_state.get("save_conflict") and st.button(t("ui.save_force"), key="save_force"):
        _save(model, path, result, force=True)
    if right.button(t("ui.discard"), key="discard_model", on_click=views.open_model, args=(path,)):
        st.rerun()


def body() -> None:
    model = state.get_model()
    if model is None:
        st.info(t("ui.no_model"))
        return
    path = Path(model.path)
    st.title(t("ui.page_modell"))
    st.caption(f"`{path.name}`" + (f" · {t('ui.readonly')}" if model.readonly else ""))
    explanation = path.with_suffix(".md")
    if explanation.is_file():
        with st.expander(t("ui.explanation"), expanded=False):
            st.markdown(files.read_text(explanation))
    if state.EDITOR not in st.session_state:
        st.session_state[state.EDITOR] = model.draft  # restore after visiting another page
    model.draft = st.text_area(
        t("ui.editor"), key=state.EDITOR, height=420, disabled=model.readonly
    )
    result = check_text(model.text)
    _hints(result, model.readonly)
    if model.dirty:
        st.warning(t("ui.unsaved"))
    if not model.readonly:
        _actions(model, path, result)
    with st.expander(t("ui.copy"), expanded=model.readonly):
        existing = {p.stem for p in files.list_models(settings.models_dir())}
        views.copy_form(path, "modell", files.suggest_id(f"{path.stem}_kopie", existing))
    st.page_link("pages/simulation.py", label=t("ui.to_simulation"))


views.run_page(body)
