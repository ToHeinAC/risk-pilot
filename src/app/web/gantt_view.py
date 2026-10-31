"""The schedule (Gantt) view beside a graph: the Graph | Zeitplan switch and the chart."""

from collections.abc import Mapping
from typing import Any

from nicegui import ui
from numpy.typing import NDArray

from app.analysis.schedule import Bar, bars, schedule
from app.engine.simulate import simulate
from app.errors import ModelError, SimulationError
from app.messages import render, t
from app.model.compile import CompiledModel, compile_model
from app.model.scenarios import effective_model
from app.model.schema import BASIS
from app.present import gantt
from app.present.preview import PREVIEW_N
from app.web import theme
from app.web.editing import ModelEdit


def switch(marker: str) -> ui.toggle:
    views = {"graph": t("gantt.view_graph"), "gantt": t("gantt.view_gantt")}
    view = ui.toggle(views, value="graph").props("dense no-caps unelevated size=sm")
    return view.mark(marker)


def outputs(compiled: CompiledModel) -> list[str]:
    return [i for i, node in compiled.nodes.items() if node.type == "output"]


def rows(compiled: CompiledModel, samples: Mapping[str, NDArray[Any]], output: str) -> list[Bar]:
    names = {i: node.name or i for i, node in compiled.model.nodes.items()}
    return bars(schedule(compiled, samples, output), names)


def chart(plan: list[Bar], unit: str | None, marker: str) -> None:
    theme.plot(gantt.figure(plan, unit), gantt.height(plan)).mark(marker)
    ui.label(t("gantt.caption")).classes("rp-muted text-sm")


def drafted(
    edit: ModelEdit, scenario: str
) -> tuple[CompiledModel, Mapping[str, NDArray[Any]]] | str:
    """The compiled draft in ``scenario`` and a small run of it; else why there is none."""
    checked = edit.checked()
    if checked.compiled is None or checked.model is None:
        return checked.rows[0].message if checked.rows else checked.status
    if scenario == BASIS or scenario not in checked.model.scenarios:
        if edit.trial_error is not None or not edit.trial:
            return edit.trial_error or ""
        return checked.compiled, edit.trial
    try:
        compiled = compile_model(effective_model(checked.model, scenario))
        return compiled, simulate(compiled, n=PREVIEW_N, keep="all").samples
    except (ModelError, SimulationError) as exc:
        issues = exc.issues if isinstance(exc, ModelError) else [exc.issue]
        return render(issues[0])


def draft_chart(edit: ModelEdit, scenario: str, marker: str) -> None:
    """The schedule of the draft in ``scenario`` up to its first output, or why there is none."""
    found = drafted(edit, scenario)
    if isinstance(found, str):
        ui.label(t("gantt.unavailable", reason=found)).classes("rp-muted")
        return
    compiled, samples = found
    for output in outputs(compiled)[:1]:
        chart(rows(compiled, samples, output), compiled.model.nodes[output].unit, marker)
