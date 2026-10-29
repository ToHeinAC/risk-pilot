"""Learning path: explain, predict, simulate, turn the knob, compare, copy (M7 step 6)."""

from functools import partial

import numpy as np
from nicegui import run, ui

from app.adapters import files, settings
from app.errors import InputError, SimulationError
from app.lessons.catalog import Lesson, lesson_problems, manifest_from_yaml
from app.lessons.knob import current_value, with_value
from app.lessons.reference import REFERENCES, Check
from app.lessons.sources import SOURCES
from app.messages import render, t
from app.model.compile import compile_model
from app.model.schema import Model
from app.model.yaml_io import model_to_yaml
from app.present import figures
from app.present.references import Curve
from app.present.results import change_sentence, compare_rows
from app.present.text import number, validity_line
from app.web import results_view, running, theme
from app.web.session import RunView, Session

LESSONS = settings.examples_dir() / "lernpfad"


def _step(title: str) -> ui.column:
    panel = ui.column().classes("rp-panel p-4 w-full gap-2")
    with panel:
        ui.label(title).classes("text-lg font-semibold")
    return panel


def _validity(run: RunView) -> None:
    ui.label(validity_line(run.result.meta, run.scenario)).classes("rp-muted text-sm")


def _checks(lesson: Lesson, run: RunView) -> list[Check]:
    if lesson.reference is None:
        return []
    checks = REFERENCES[lesson.reference](run.compiled.model, run.result.samples[lesson.output])
    for check in checks:
        status = t("lesson.passed") if check.passed else t("lesson.failed")
        text = t(
            f"lesson.check_{check.kind}",
            expected=number(check.expected, 4),
            observed=number(check.observed, 4),
        )
        results_view.note(f"{text} – {status}", "success" if check.passed else "error")
    return checks


def _curves(checks: list[Check], x: np.ndarray) -> list[Curve]:
    grid = np.linspace(float(np.min(x)), float(np.max(x)), 400)
    return [Curve(t("ref.analytic"), grid, c.cdf(grid)) for c in checks if c.cdf is not None]


def _explain(lesson: Lesson) -> None:
    ui.markdown(files.read_text(LESSONS / lesson.text))
    with ui.expansion(t("lesson.model_yaml"), icon="code").classes("rp-panel w-full"):
        ui.code(files.read_text(LESSONS / lesson.model), language="yaml").classes("w-full")
    sources = "\n".join(f"- {SOURCES[k]}" for k in lesson.sources)
    ui.markdown(f"{t('lesson.sources')}\n{sources}")
    results_view.note(t("lesson.illustrative"))


def _load(lesson: Lesson) -> Model | None:
    """The lesson model, if the lesson files exist and fit the manifest; problems are shown."""
    missing = [name for name in (lesson.model, lesson.text) if not (LESSONS / name).is_file()]
    if missing:
        results_view.note(t("lesson.missing", files=", ".join(missing)), "error")
        return None
    base = files.load_model(LESSONS / lesson.model)
    problems = lesson_problems(lesson, base)
    for problem in problems:
        results_view.note(t("lesson.invalid", problem=problem), "error")
    return None if problems else base


class LessonPage:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.state = session.lessons
        manifest = manifest_from_yaml(files.read_text(LESSONS / "lernpfad.yaml"))
        self.lessons = {lesson.id: lesson for lesson in manifest.lessons}
        if self.state.selected not in self.lessons:
            self.state.selected = next(iter(self.lessons))
        self.base: Model | None = None

    @property
    def lesson(self) -> Lesson:
        return self.lessons[str(self.state.selected)]

    def build(self) -> None:
        self.state.progress.setdefault(self.lesson.id, set()).add("seen")
        with ui.row().classes("w-full gap-4 no-wrap max-lg:flex-wrap items-start"):
            with ui.column().classes("rp-panel p-2 gap-0 w-72 shrink-0"):
                self.nav()
            with ui.column().classes("flex-1 min-w-0 gap-4"):
                self.body()

    def select(self, lesson_id: str) -> None:
        self.state.selected = lesson_id
        self.state.progress.setdefault(lesson_id, set()).add("seen")
        self.nav.refresh()
        self.body.refresh()

    @ui.refreshable_method
    def nav(self) -> None:
        for lesson in self.lessons.values():
            steps = self.state.progress.get(lesson.id, set())
            mark = t("lesson.done") if "turned" in steps else t("lesson.seen") if steps else ""
            active = " rp-current" if lesson.id == self.state.selected else ""
            item = ui.item(on_click=partial(self.select, lesson.id)).classes(f"rounded{active}")
            with item.mark(f"lesson/{lesson.id}"), ui.item_section():
                ui.item_label(lesson.title)
                if mark:
                    ui.item_label(mark.strip(" ·")).props("caption")
        done = sum(1 for steps in self.state.progress.values() if "turned" in steps)
        ui.label(t("lesson.progress", done=done, total=len(self.lessons))).classes(
            "rp-muted text-sm p-2"
        )

    @ui.refreshable_method
    def body(self) -> None:
        lesson = self.lesson
        self.base = _load(lesson)
        if self.base is None:
            return
        _explain(lesson)
        with _step(t("lesson.predict")):
            ui.radio(
                lesson.question.options,
                value=self.state.predictions.get(lesson.id),
                on_change=lambda e: self.state.predictions.__setitem__(lesson.id, e.value),
            ).mark(f"prediction_{lesson.id}")
            ui.label(lesson.question.text).classes("rp-muted").move(target_index=1)
        with _step(t("lesson.simulate")):
            with ui.row().classes("items-end gap-4"):
                self.n = ui.number(
                    t("ui.n"), value=self.base.settings.n, min=1000, max=2_000_000, step=1000
                )
                self.n.props("outlined dense").mark("lesson_n")
                ui.button(t("lesson.run"), icon="play_arrow", on_click=self.simulate).props(
                    "unelevated no-caps"
                ).mark("lesson_run")
            self.status = ui.row().classes("items-center gap-2")
            self.results()
        self._copy(lesson, self.base)

    def _start(self) -> float:
        knob = self.lesson.knob
        assert self.base is not None
        return current_value(self.base, knob.node, knob.field) or 0.0

    def _scenario(self, value: float) -> str:
        return t("lesson.knob_scenario", label=self.lesson.knob.label, value=number(value))

    async def _run(self, model: Model, value: float) -> RunView | None:
        n = int(self.n.value or model.settings.n)
        self.status.clear()
        with self.status:
            ui.spinner(size="sm")
        try:
            done = await run.io_bound(
                running.compute_run,
                self.session.runs,
                compile_model(model),
                model_to_yaml(model),
                n,
                model.settings.seed,
                self._scenario(value),
            )
        except SimulationError as exc:
            self.status.clear()
            with self.status:
                ui.label(render(exc.issue)).classes("text-negative")
            return None
        self.status.clear()
        return done

    async def simulate(self) -> None:
        assert self.base is not None
        lesson_id = self.lesson.id
        done = await self._run(self.base, self._start())
        if done is not None:
            self.state.runs[lesson_id] = done
            self.state.runs.pop(f"{lesson_id}:turned", None)
            self.results.refresh()

    async def turn(self) -> None:
        assert self.base is not None
        knob = self.lesson.knob
        value = self.state.knobs.get(self.lesson.id, self._start())
        done = await self._run(with_value(self.base, knob.node, knob.field, value), value)
        if done is not None:
            self.state.runs[f"{self.lesson.id}:turned"] = done
            self.state.progress.setdefault(self.lesson.id, set()).add("turned")
            self.nav.refresh()
            self.results.refresh()

    @ui.refreshable_method
    def results(self) -> None:
        lesson = self.lesson
        before = self.state.runs.get(lesson.id)
        if before is None:
            return
        _validity(before)
        results_view.output(before, lesson.output)
        _checks(lesson, before)
        with _step(t("lesson.turn")):
            ui.label(lesson.knob.label).classes("rp-kicker")
            choices = {v: number(v) for v in lesson.knob.choices()}
            ui.toggle(
                choices,
                value=self.state.knobs.get(lesson.id, self._start()),
                on_change=lambda e: self.state.knobs.__setitem__(lesson.id, float(e.value)),
            ).props("no-caps").mark(f"knob_{lesson.id}")
            ui.button(t("lesson.turn_run"), icon="tune", on_click=self.turn).props(
                "unelevated no-caps"
            ).mark("lesson_turn")
            after = self.state.runs.get(f"{lesson.id}:turned")
            if after is not None:
                self._compare(lesson, before, after)

    def _compare(self, lesson: Lesson, before: RunView, after: RunView) -> None:
        out = lesson.output
        unit = after.compiled.model.nodes[out].unit
        b, a = before.summaries[out], after.summaries[out]
        _validity(after)
        headers = [t("ui.metric"), t("lesson.before"), t("lesson.after"), t("lesson.diff")]
        results_view.table(headers, compare_rows(b, a, unit)).mark("lesson_compare")
        prediction = self.state.predictions.get(lesson.id)
        result = change_sentence(lesson.question.metric, b, a, unit)
        if prediction:
            sentence = t("lesson.prediction", prediction=prediction, result=result)
        else:
            sentence = t("lesson.result", result=result)
        ui.label(sentence).classes("rp-answer")
        results_view.note(t("lesson.rule", rule=lesson.rule))
        checks = _checks(lesson, after)
        if b.kind == "num":
            samples = {
                t("lesson.before"): before.result.samples[out],
                t("lesson.after"): after.result.samples[out],
            }
            curves = _curves(checks, after.result.samples[out])
            theme.plot(figures.compare_cdfs(samples, unit, curves), 320)

    def _copy(self, lesson: Lesson, base: Model) -> None:
        with _step(t("lesson.copy")), ui.row().classes("items-end gap-3"):
            name = ui.input(t("ui.copy_name"), value=f"{lesson.id}_eigen")
            name.props("outlined dense").mark(f"lesson_copy_id_{lesson.id}")
            done = ui.label()

            def copy() -> None:
                knob = lesson.knob
                value = self.state.knobs.get(lesson.id, self._start())
                model = with_value(base, knob.node, knob.field, value)
                try:
                    target = files.create_model_text(
                        settings.models_dir(),
                        str(name.value or "").strip(),
                        model_to_yaml(model),
                    )
                except InputError as exc:
                    done.text = render(exc.issue)
                else:
                    done.text = t("ui.copied", name=target.stem)

            ui.button(t("ui.copy"), icon="content_copy", on_click=copy).props(
                "outline no-caps"
            ).mark("lesson_copy")
            done.move(target_index=-1)


def page(session: Session) -> None:
    LessonPage(session).build()
