"""Stored runs: list and reload."""

import json

import streamlit as st

from app.adapters import runs, settings
from app.analysis.stats import summary_to_dict
from app.errors import ModelError
from app.messages import t
from app.model.compile import compile_model
from app.model.scenarios import effective_model
from app.model.schema import BASIS
from app.model.yaml_io import model_from_yaml
from app.present.results import summaries_for
from app.ui import state, views


def _load(path_name: str) -> None:
    stored = runs.load_run(settings.runs_dir() / path_name)
    scenario_id = str(stored.meta.get("scenario_id", BASIS))
    compiled = compile_model(effective_model(model_from_yaml(stored.model_text), scenario_id))
    result = runs.as_result(stored)
    summaries = summaries_for(compiled, result)
    fresh = {k: summary_to_dict(v) for k, v in summaries.items()}
    notices = [] if json.dumps(fresh) == json.dumps(stored.summary) else [t("ui.run_mismatch")]
    scenario = str(stored.meta.get("scenario", t("ui.main_scenario")))
    template, original = views.template_and_hash(compiled, stored.model_text)
    state.set_run(
        state.RunView(
            stored.model_text,
            compiled,
            result,
            summaries,
            scenario,
            template,
            original,
            0.0,
            notices,
            scenario_id,
        )
    )


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
