"""Scenarios: tree, diff, create, override, duplicate, detach."""

from collections.abc import Callable

import streamlit as st
import yaml

from app.adapters import files
from app.errors import ModelError
from app.messages import render, t
from app.model import scenarios as sc
from app.model.schema import BASIS, Model
from app.model.yaml_io import model_from_yaml, model_to_yaml
from app.present.validation import check_text
from app.ui import state, views

MESSAGE = "scenario_message"


def _model() -> Model:
    open_model = state.get_model()
    assert open_model is not None
    return model_from_yaml(open_model.draft)


def _edit(change: Callable[[Model], Model]) -> None:
    """Apply a change only if the result is a valid model; otherwise explain and keep the text."""
    try:
        changed = change(_model())
    except (ValueError, ModelError) as exc:
        issues = exc.issues if isinstance(exc, ModelError) else []
        st.session_state[MESSAGE] = "; ".join(render(i) for i in issues) or str(exc)
        return
    problems = check_text(model_to_yaml(changed)).rows
    if problems:
        st.session_state[MESSAGE] = "; ".join(row.message for row in problems)
        return
    views.rewrite(changed)
    st.session_state[MESSAGE] = None


def _value(key: str) -> str:
    return str(st.session_state.get(key, "")).strip()


def _add() -> None:
    sid = _value("scenario_new_id")
    parent = str(st.session_state.get("scenario_new_parent", BASIS))
    _edit(
        lambda m: sc.add_scenario(
            m, sid, _value("scenario_new_name") or sid, parent, _value("scenario_new_why")
        )
    )
    if not st.session_state.get(MESSAGE):
        st.session_state["scenario_pick"] = sid


def _set_override(sid: str) -> None:
    raw = _value("override_value")
    value = yaml.safe_load(raw) if raw else None
    if value is None:
        st.session_state[MESSAGE] = t("scen.value_missing")
        return
    node, field, why = (
        str(st.session_state["override_node"]),
        _value("override_field"),
        _value("override_why"),
    )
    _edit(lambda m: sc.set_override(m, sid, node, field, value, why or None))


def _remove_override(sid: str) -> None:
    node, _, field = str(st.session_state["override_remove_pick"]).partition(".")
    _edit(lambda m: sc.remove_override(m, sid, node, field))


def _duplicate(sid: str, ids: list[str]) -> None:
    new_id = files.suggest_id(f"{sid}_kopie", set(ids))
    _edit(lambda m: sc.duplicate(m, sid, new_id))


def _detach(sid: str) -> None:
    _edit(lambda m: sc.detach(m, sid))
    st.session_state["detach_pending"] = False


def _tree(model: Model) -> str:
    lines: list[str] = []
    for sid, depth in sc.tree(model):
        if sid == BASIS:
            lines.append(f"- **{t('ui.main_scenario')}** (`basis`)")
            continue
        s = model.scenarios[sid]
        extra = (
            t("scen.detached") if s.nodes is not None else t("scen.overrides", n=len(s.overrides))
        )
        lines.append("  " * depth + f"- **{s.name}** (`{sid}`) · {extra}")
    return "\n".join(lines)


def _diff(model: Model, sid: str) -> None:
    scenario = model.scenarios[sid]
    st.markdown(t("scen.why", why=scenario.why))
    rows = [
        (r.node, r.field, str(r.before), str(r.after), r.why or "", r.status)
        for r in sc.diff(model, sid)
    ]
    headers = [
        t("scen.col_node"),
        t("scen.col_field"),
        t("scen.col_parent"),
        t("scen.col_value"),
        t("scen.col_why"),
        t("scen.col_status"),
    ]
    st.markdown(views.table(headers, rows) if rows else t("scen.no_overrides"))


def _create_form(ids: list[str], pick: str) -> None:
    with st.expander(t("scen.new"), expanded=False):
        st.text_input(t("scen.new_id"), key="scenario_new_id")
        st.text_input(t("scen.new_name"), key="scenario_new_name")
        st.text_input(t("scen.new_why"), key="scenario_new_why")
        st.selectbox(t("scen.new_parent"), ids, index=ids.index(pick), key="scenario_new_parent")
        st.button(t("scen.add"), key="scenario_add", on_click=_add)


def _override_form(model: Model, sid: str, ids: list[str]) -> None:
    if model.scenarios[sid].nodes is None:
        st.subheader(t("scen.override"))
        st.selectbox(t("scen.col_node"), list(model.nodes), key="override_node")
        st.text_input(t("scen.col_field"), key="override_field")
        st.text_input(t("scen.value_hint"), key="override_value")
        st.text_input(t("scen.col_why"), key="override_why")
        st.button(t("scen.set"), key="override_set", on_click=_set_override, args=(sid,))
        existing = [f"{r.node}.{r.field}" for r in sc.diff(model, sid)]
        if existing:
            st.selectbox(t("scen.remove_pick"), existing, key="override_remove_pick")
            st.button(
                t("scen.remove"), key="override_remove", on_click=_remove_override, args=(sid,)
            )
    left, right = st.columns(2)
    left.button(t("scen.duplicate"), key="scenario_duplicate", on_click=_duplicate, args=(sid, ids))
    if right.button(t("scen.detach"), key="scenario_detach"):
        st.session_state["detach_pending"] = True
    if st.session_state.get("detach_pending"):
        st.warning(t("scen.detach_question"))
        st.button(
            t("scen.detach_confirm"), key="scenario_detach_confirm", on_click=_detach, args=(sid,)
        )


def body() -> None:
    st.title(t("ui.page_szenarien"))
    open_model = state.get_model()
    if open_model is None:
        st.info(t("ui.no_model"))
        return
    checked = check_text(open_model.draft)
    model = checked.model
    if model is None:
        st.error(t("scen.invalid_model"))
        return
    if st.session_state.get(MESSAGE):
        st.error(str(st.session_state[MESSAGE]))
    st.markdown(_tree(model))
    ids = [sid for sid, _ in sc.tree(model)]
    names = {
        sid: (model.scenarios[sid].name if sid != BASIS else t("ui.main_scenario")) for sid in ids
    }
    pick = str(
        st.selectbox(t("scen.pick"), ids, format_func=lambda s: names[s], key="scenario_pick")
    )
    if pick != BASIS:
        _diff(model, pick)
    if open_model.readonly:
        st.caption(t("scen.readonly"))
        return
    _create_form(ids, pick)
    if pick != BASIS:
        _override_form(model, pick, ids)


views.run_page(body)
