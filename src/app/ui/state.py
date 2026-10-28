"""Typed access to ``st.session_state``."""

from dataclasses import dataclass, field
from typing import Any, cast

import streamlit as st

from app.analysis.stats import Summary
from app.engine.simulate import SimulationResult
from app.model.compile import CompiledModel

EDITOR = "editor"


@dataclass
class OpenModel:
    """The open model. ``draft`` lives outside the editor widget, because Streamlit drops a
    widget's state as soon as a page without that widget is shown."""

    path: str
    file_text: str
    readonly: bool
    draft: str = ""

    def __post_init__(self) -> None:
        self.draft = self.draft or self.file_text

    @property
    def text(self) -> str:
        return self.draft

    @property
    def dirty(self) -> bool:
        return not self.readonly and self.draft != self.file_text


@dataclass
class RunView:
    model_text: str
    compiled: CompiledModel
    result: SimulationResult
    summaries: dict[str, Summary]
    scenario: str
    template: str
    original_hash: str | None
    seconds: float = 0.0
    notices: list[str] = field(default_factory=list[str])
    scenario_id: str = "basis"


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
