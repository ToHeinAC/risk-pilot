"""Typed access to ``st.session_state``."""

from typing import Any, cast

import streamlit as st

from app.web.session import OpenModel as OpenModel  # re-exported for the pages
from app.web.session import RunView as RunView

EDITOR = "editor"


def _get(key: str) -> Any:
    return st.session_state.get(key)


def get_model() -> OpenModel | None:
    return cast(OpenModel | None, _get("open_model"))


def set_model(model: OpenModel) -> None:
    st.session_state["open_model"] = model
    st.session_state[EDITOR] = model.file_text
    st.session_state.pop("run", None)


def get_run() -> RunView | None:
    return cast(RunView | None, _get("run"))


def set_run(run: RunView) -> None:
    st.session_state["run"] = run


def cache() -> dict[tuple[str, int, int], RunView]:
    """Runs by (model hash, N, seed): the same click does not compute twice."""
    return cast(dict[tuple[str, int, int], RunView], st.session_state.setdefault("run_cache", {}))
