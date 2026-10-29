"""Editing state of the model page: one draft, written by the form and the YAML editor alike.

No UI import. Every change goes through ``set_text`` (YAML) or ``change`` (form, hints); both
update the draft, the check and the trial run, so the last change wins without any syncing.
"""

import time
from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import NDArray

from app.engine.simulate import simulate
from app.errors import InputError, SimulationError
from app.messages import render
from app.model import form
from app.model.schema import Model
from app.model.yaml_patch import Data, load_data, patch
from app.present.brief import Trace, trace
from app.present.preview import PREVIEW_N
from app.present.validation import CheckResult, check_text
from app.web.session import OpenModel


class ModelEdit:
    def __init__(self, model: OpenModel) -> None:
        self.model = model
        self.error: str | None = None  # the last form change that was refused, explained
        self.written = False  # the form changed the draft last
        self.trial: dict[str, NDArray[Any]] = {}
        self.traces: dict[str, Trace] = {}
        self.trial_ms: float | None = None
        self.trial_error: str | None = None
        self._checked: tuple[str, CheckResult] | None = None
        self._data: tuple[str, Data | None, str | None] | None = None
        self.selected: str | None = None
        self._run_trial()
        self.selected = self._first_output()

    @property
    def text(self) -> str:
        return self.model.text

    def checked(self) -> CheckResult:
        if self._checked is None or self._checked[0] != self.text:
            self._checked = (self.text, check_text(self.text))
        return self._checked[1]

    def _parsed(self) -> tuple[str, Data | None, str | None]:
        if self._data is None or self._data[0] != self.text:
            try:
                self._data = (self.text, load_data(self.text), None)
            except InputError as exc:
                self._data = (self.text, None, render(exc.issue))
        return self._data

    def data(self) -> Data | None:
        """The draft as raw data (read only; ``change`` parses afresh), None while unreadable."""
        return self._parsed()[1]

    def data_error(self) -> str | None:
        return self._parsed()[2]

    def set_text(self, text: str) -> None:
        """The YAML editor's text becomes the draft."""
        if self.model.readonly or text == self.text:
            return
        self.model.draft = text
        self.written, self.error = False, None
        self._after_change()

    def change(self, edit: Callable[[Data], Data]) -> bool:
        """A form change: patch it into the draft (comments stay) or keep the draft and explain."""
        try:
            text = patch(self.text, edit(load_data(self.text)))
        except InputError as exc:
            self.error = render(exc.issue)
            return False
        self.model.draft = text
        self.written, self.error = True, None
        self._after_change()
        return True

    def edit_model(self, edit: Callable[[Model], Model]) -> bool:
        """A change on the validated model (fit offers, CSV, mark inactive)."""
        model = self.checked().model
        if model is None:
            return False
        try:
            data = edit(model).model_dump(mode="json", exclude_unset=True)
        except InputError as exc:
            self.error = render(exc.issue)
            return False
        return self.change(lambda _old: data)

    def discard(self, file_text: str) -> None:
        self.model.file_text = file_text
        self.model.draft = file_text
        self.written, self.error = False, None
        self._after_change()

    def node_ids(self) -> list[str]:
        data = self.data()
        return form.node_ids(data) if data is not None else []

    def _first_output(self) -> str | None:
        data = self.data()
        if data is None:
            return None
        ids = form.node_ids(data)
        outputs = [i for i in ids if form.values(data, i)["type"] == "output"]
        return (outputs or ids or [None])[0]

    def _after_change(self) -> None:
        self._run_trial()
        if self.selected not in self.node_ids():
            self.selected = self._first_output()

    def _run_trial(self) -> None:
        """Every node's draws from one small run; the table, graph and preview read them."""
        self.trial, self.traces, self.trial_ms, self.trial_error = {}, {}, None, None
        compiled = self.checked().compiled
        if compiled is None:
            return
        started = time.perf_counter()
        try:
            result = simulate(compiled, n=PREVIEW_N, keep="all")
        except SimulationError as exc:
            self.trial_error = render(exc.issue)
            return
        self.trial_ms = (time.perf_counter() - started) * 1000
        self.trial = {k: np.asarray(v) for k, v in result.samples.items()}
        self.traces = trace(self.trial)
