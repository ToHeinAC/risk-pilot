"""Stored runs: list and reload."""

import streamlit as st

from app.adapters import runs, settings
from app.errors import ModelError
from app.messages import t
from app.model.yaml_io import model_from_yaml
from app.ui import state, views
from app.web import running


def _load(path_name: str) -> None:
    state.set_run(running.load(settings.runs_dir() / path_name))


def _current_model_id() -> str | None:
    model = state.get_model()
    if model is None:
        return None
    try:
        return model_from_yaml(model.text).model
    except ModelError:
        return None


def body() -> None:
    st.title(t("ui.page_laeufe"))
    found = runs.list_runs(settings.runs_dir(), _current_model_id())
    if not found:
        st.info(t("ui.no_runs"))
    for index, path in enumerate(found):
        if st.button(path.name, key=f"load_run_{index}"):
            _load(path.name)
            st.session_state["loaded_run"] = True
    run = state.get_run()
    if run is not None and st.session_state.get("loaded_run"):
        views.render_run(run)


views.run_page(body)
