"""The card of one node in the form editor (M6): its fields, delete, preview."""

from typing import Any

import streamlit as st

from app.messages import t
from app.model import form
from app.model.yaml_patch import Data
from app.present.validation import CheckResult
from app.ui import form as ui
from app.ui.form import key

SELECTS = {
    "target_op": ("", *form.TARGET_OPS),
    "better": ("", "lower", "higher"),
}
AREAS = ("description", "why", "expr", "options")
FIRST = ("name", "unit")
LAST = ("description", "why", "tags", "bounds_min", "bounds_max", "track")


def _options_text(rows: list[tuple[str, str]]) -> str:
    return "\n".join(f"{label}: {weight}" for label, weight in rows)


def _options_rows(text: str) -> list[tuple[str, str]]:
    rows = [line.rpartition(":") for line in text.splitlines() if line.strip()]
    return [
        (label.strip(), weight.strip()) if sep else (weight.strip(), "")
        for label, sep, weight in rows
    ]


def _collect(node_id: str, fields: list[str]) -> dict[str, Any]:
    values = ui.widget_values(fields, node_id)
    if "options" in values:
        values["options"] = _options_rows(str(values["options"]))
    return values


def _on_node(node_id: str, fields: list[str]) -> None:
    ui.write(lambda d: form.apply(d, node_id, _collect(node_id, fields)))


def _on_dist(node_id: str) -> None:
    dist = str(st.session_state[key("dist", node_id)])
    mode = str(st.session_state.get(key("input", node_id)) or "params")
    modes = ui.mode_choices(dist)
    ui.write(lambda d: form.set_dist(d, node_id, dist, mode if mode in modes else modes[0]))


def _label(field: str) -> str:
    return field.removeprefix("param.") if field.startswith("param.") else t(f"form.f_{field}")


def _select(node_id: str, field: str, value: Any, disabled: bool, dist: str) -> None:
    """Distribution and input mode: changing them keeps only the parameters that fit."""
    choices = ui.dist_choices(str(value)) if field == "dist" else ui.mode_choices(dist)
    st.selectbox(
        _label(field),
        choices,
        index=choices.index(value) if value in choices else 0,
        key=key(field, node_id),
        disabled=disabled,
        on_change=_on_dist,
        args=(node_id,),
    )


def _field(
    node_id: str, field: str, value: Any, fields: list[str], disabled: bool, dist: str
) -> None:
    if field in ("dist", "input"):
        _select(node_id, field, value, disabled, dist)
        return
    name, label, args = key(field, node_id), _label(field), (node_id, fields)
    if field == "track":
        st.checkbox(label, bool(value), key=name, disabled=disabled, on_change=_on_node, args=args)
    elif field in SELECTS:
        options = SELECTS[field]
        index = options.index(value) if value in options else 0
        st.selectbox(
            label, options, index, key=name, disabled=disabled, on_change=_on_node, args=args
        )
    elif field in AREAS:
        text = _options_text(value) if field == "options" else str(value)
        st.text_area(label, text, 80, key=name, disabled=disabled, on_change=_on_node, args=args)
    else:
        st.text_input(label, str(value), key=name, disabled=disabled, on_change=_on_node, args=args)


def _on_delete(node_id: str) -> None:
    ui.write(lambda d: form.remove_node(d, node_id))


def _delete(node_id: str) -> None:
    sure = st.checkbox(t("form.delete_confirm"), key=key("delete_confirm", node_id))
    st.button(
        t("form.delete", node=node_id),
        key=key("delete", node_id),
        disabled=not sure,
        on_click=_on_delete,
        args=(node_id,),
    )


def card(data: Data, node_id: str, result: CheckResult, readonly: bool) -> None:
    """Fields of ``node_id`` by its type; uncertain nodes get the distribution preview."""
    values = form.values(data, node_id)
    middle = [f for f in values if f not in ("type", *FIRST, *LAST)]
    fields = [*FIRST, *middle, *LAST]
    with st.container(border=True):
        type_label = t(f"type.{values['type']}")
        st.markdown(f"**`{node_id}`** · {type_label}")
        for field in fields:
            _field(node_id, field, values[field], fields, readonly, str(values.get("dist", "")))
        if not readonly:
            _delete(node_id)
    if values["type"] == "uncertain":
        st.markdown(f"**{t('form.preview')}**")
        ui.preview_block(result, node_id, values["unit"] or None)
