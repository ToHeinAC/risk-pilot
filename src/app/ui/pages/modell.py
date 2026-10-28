"""Model: YAML editor with live validation."""

from pathlib import Path

import streamlit as st

from app.adapters import files, settings
from app.errors import InputError
from app.messages import render, t
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
    _show_check(result)
    if model.dirty:
        st.warning(t("ui.unsaved"))
    if not model.readonly:
        _actions(model, path, result)
    with st.expander(t("ui.copy"), expanded=model.readonly):
        existing = {p.stem for p in files.list_models(settings.models_dir())}
        views.copy_form(path, "modell", files.suggest_id(f"{path.stem}_kopie", existing))
    st.page_link("pages/simulation.py", label=t("ui.to_simulation"))


views.run_page(body)
