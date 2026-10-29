"""Form editor on the model page (M6): model header, node table, one node card at a time.

Every widget writes through a callback: the form values go into ``form.apply``, the result is
patched into the YAML draft (comments stay). Widget keys are stable; when the draft changed
elsewhere (YAML tab, scenarios page) the form's widget state is dropped and rebuilt from it.
"""

from collections.abc import Callable
from typing import Any

import streamlit as st

from app.adapters import files
from app.dists.registry import families, get_family
from app.errors import InputError
from app.messages import render, t
from app.model import form
from app.model.yaml_patch import Data, load_data
from app.present import preview
from app.present.validation import CheckResult
from app.ui import state, views

PREFIX = "form."  # widget keys rebuilt from the draft
SEEN = "form_seen"
ERROR = "form_error"
PICK = "form_pick"
TYPES = ("uncertain", "constant", "event", "choice", "derived", "output")
LONG = ("description", "why", "expr")


def key(field: str, node_id: str = "") -> str:
    return f"{PREFIX}{node_id}.{field}" if node_id else f"{PREFIX}{field}"


def _draft() -> str:
    """The editor's text when it exists: in a callback it may be newer than ``model.draft``."""
    model = state.get_model()
    assert model is not None
    editor = st.session_state.get(state.EDITOR)
    if isinstance(editor, str) and not model.readonly:
        model.draft = editor
    return model.draft


def _data() -> Data:
    return load_data(_draft())


def _sync() -> None:
    """Drop the form's widget state when the draft no longer is what the widgets show."""
    model = state.get_model()
    assert model is not None
    seen = f"{model.path}:{files.text_hash(_draft())}"  # another model with equal text too
    if st.session_state.get(SEEN) != seen:
        for name in [k for k in st.session_state if str(k).startswith(PREFIX)]:
            del st.session_state[name]
        st.session_state[SEEN] = seen
        st.session_state[ERROR] = None  # an old form error no longer applies


def write(change: Callable[[Data], Data]) -> None:
    """Widget callback: change the data, patch it into the draft, or keep it and explain."""
    try:
        views.rewrite_data(change(_data()))
    except InputError as exc:
        st.session_state[ERROR] = render(exc.issue)
        return
    st.session_state[ERROR] = None
    st.session_state["form_written"] = True  # the YAML tab shows the new text (last change wins)


def widget_values(fields: list[str], node_id: str = "") -> dict[str, Any]:
    return {
        f: st.session_state[key(f, node_id)] for f in fields if key(f, node_id) in st.session_state
    }


def _on_header() -> None:
    write(lambda d: form.apply_header(d, widget_values(list(form.header_values(d)))))


def _header(data: Data, disabled: bool) -> None:
    values = form.header_values(data)
    with st.expander(t("form.header", model=data.get("model", "")), expanded=False):
        for name in ("title", "description", "n", "seed"):
            st.text_input(
                t(f"form.f_{name}"),
                value=values[name],
                key=key(name),
                on_change=_on_header,
                disabled=disabled,
            )
        st.checkbox(
            t("form.f_illustrative"),
            value=values["illustrative"],
            key=key("illustrative"),
            on_change=_on_header,
            disabled=disabled,
        )


def _node_rows(data: Data) -> list[tuple[str, ...]]:
    rows: list[tuple[str, ...]] = []
    for node_id in form.node_ids(data):
        v = form.values(data, node_id)
        why = t("form.yes") if v["why"] else t("form.no")
        rows.append((f"`{node_id}`", t(f"type.{v['type']}"), v["name"], v["unit"], why))
    return rows


def _table(data: Data) -> None:
    headers = [
        t("ui.col_id"),
        t("ui.col_type"),
        t("ui.col_name"),
        t("ui.col_unit"),
        t("form.col_why"),
    ]
    rows = _node_rows(data)
    st.markdown(views.table(headers, rows) if rows else t("form.no_nodes"))


def body(readonly: bool) -> tuple[Data, str] | None:
    """The form tab's upper part: header, node table, add; returns the data and picked node."""
    try:
        data = _data()
    except InputError as exc:
        st.warning(render(exc.issue))
        return None
    _sync()
    error = st.session_state.get(ERROR)
    if error:
        st.error(error)
    if st.session_state.pop("form_written", False):
        st.caption(t("form.written"))
    _header(data, readonly)
    _table(data)
    if not readonly:
        _add()
    nodes = form.node_ids(data)
    if not nodes:
        return None
    if st.session_state.get(PICK) not in nodes:
        st.session_state[PICK] = nodes[0]
    return data, str(st.selectbox(t("form.pick"), nodes, key=PICK))


def _on_add() -> None:
    node_id = str(st.session_state.get("form_new_id", "")).strip()
    node_type = str(st.session_state.get("form_new_type", TYPES[0]))
    write(lambda d: form.add_node(d, node_id, node_type))
    if not st.session_state.get(ERROR):
        st.session_state[PICK] = node_id


def _add() -> None:
    with st.expander(t("form.add")):
        left, right = st.columns(2)
        left.text_input(t("form.new_id"), key="form_new_id")
        right.selectbox(
            t("form.new_type"), TYPES, key="form_new_type", format_func=lambda x: t(f"type.{x}")
        )
        st.button(t("form.add_button"), key="form_add", on_click=_on_add)


def preview_block(result: CheckResult, node_id: str, unit: str | None) -> None:
    """Preview of an uncertain node; needs a model that compiles."""
    if result.compiled is None or node_id not in result.compiled.model.nodes:
        reason = result.rows[0].message if result.rows else result.status
        st.info(t("form.preview_needs_valid", reason=reason))
        return
    cache: dict[tuple[str, str], Any] = st.session_state.setdefault("preview_cache", {})
    for old in [s for s in cache if s[0] != result.compiled.model_hash]:
        del cache[old]  # only the current model version is kept
    slot = (result.compiled.model_hash, node_id)
    if slot not in cache:
        try:
            cache[slot] = preview.node_preview(result.compiled, node_id)
        except preview.PreviewError as exc:
            cache[slot] = str(exc)
    shown = cache[slot]
    if isinstance(shown, str):
        st.warning(t("form.preview_failed", reason=shown))
        return
    st.markdown(
        views.table([t("form.col_metric"), t("form.col_value")], preview.preview_rows(shown, unit))
    )
    density, cdf = preview.preview_figures(shown, unit)
    left, right = st.columns(2)
    views.chart(density, f"preview_density_{node_id}", left)
    views.chart(cdf, f"preview_cdf_{node_id}", right)


def dist_choices(current: str) -> list[str]:
    known = families()
    return known if current in known else [current, *known]  # "" while none is chosen


def mode_choices(dist: str) -> list[str]:
    family = get_family(dist)
    return list(family.modes) if family else ["params"]
