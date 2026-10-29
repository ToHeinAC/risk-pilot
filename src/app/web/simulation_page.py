"""Simulation: scenario, N and seed, then run without blocking the page."""

from nicegui import run, ui

from app.engine.simulate import N_MAX
from app.errors import SimulationError
from app.messages import render, t
from app.present.text import decimal, integer
from app.present.validation import check_text, scenario_labels
from app.web import running
from app.web.session import Session


def page(session: Session) -> None:
    model = session.model
    if model is None:
        ui.label(t("ui.no_model")).classes("rp-muted")
        return
    checked = check_text(model.text)
    if checked.compiled is None:
        ui.label(t("ui.sim_blocked")).classes("text-negative")
        return
    labels = scenario_labels(checked)
    first = next(iter(labels))
    defaults = checked.scenarios[first][1].model.settings
    with ui.row().classes("rp-panel p-4 items-end gap-4 w-full"):
        scenario = ui.select(labels, value=first, label=t("ui.scenario")).props("outlined dense")
        scenario.classes("min-w-64").mark("sim_scenario")
        n = ui.number(t("ui.n"), value=defaults.n, min=1, max=N_MAX, step=1000, format="%d")
        n.props("outlined dense").mark("sim_n")
        seed = ui.number(t("ui.seed"), value=defaults.seed, min=0, step=1, format="%d")
        seed.props("outlined dense").mark("sim_seed")
        button = ui.button(t("ui.simulate"), icon="play_arrow").props("unelevated no-caps")
        button.mark("sim_run")
    status = ui.row().classes("items-center gap-2")

    async def simulate() -> None:
        sid = str(scenario.value)
        name, compiled = checked.scenarios[sid]
        hints = checked.scenario_notices.get(sid, [])
        count, start = int(n.value or defaults.n), int(seed.value or 0)
        status.clear()
        with status:
            ui.spinner(size="sm")
            ui.label(t("ui.running")).classes("rp-muted")
        button.disable()
        try:
            done = await run.io_bound(
                running.compute_run,
                session.runs,
                compiled,
                model.text,
                count,
                start,
                name,
                sid,
                hints,
            )
        except SimulationError as exc:
            message, colour = render(exc.issue), "text-negative"
        else:
            assert done is not None  # io_bound returns None only while the app shuts down
            session.run = done
            seconds = decimal(done.seconds, 2)
            message, colour = t("ui.sim_done", n=integer(count), seconds=seconds), "text-positive"
        finally:
            button.enable()
        status.clear()
        with status:
            ui.label(message).classes(colour)

    button.on_click(simulate)
    ui.button(t("ui.to_results"), on_click=lambda: ui.navigate.to("/ergebnisse")).props(
        "flat no-caps icon-right=arrow_forward"
    ).mark("to_results")
