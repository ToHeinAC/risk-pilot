"""Learning path: explain, predict, simulate, turn the knob, compare."""

from typing import cast

import numpy as np
import streamlit as st

from app.adapters import files, settings
from app.errors import InputError
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
from app.present.text import number
from app.ui import state, views

LESSONS = settings.examples_dir() / "lernpfad"


def _progress() -> dict[str, set[str]]:
    """Lesson ID -> steps done in this session ("seen", "turned"); not stored on disk (E8)."""
    return cast(dict[str, set[str]], st.session_state.setdefault("lesson_progress", {}))


def _runs() -> dict[str, state.RunView]:
    return cast(dict[str, state.RunView], st.session_state.setdefault("lesson_runs", {}))


def _label(lesson: Lesson) -> str:
    steps = _progress().get(lesson.id, set())
    mark = t("lesson.done") if "turned" in steps else t("lesson.seen") if steps else ""
    return f"{lesson.title}{mark}"


def _scenario(lesson: Lesson, value: float) -> str:
    return t("lesson.knob_scenario", label=lesson.knob.label, value=number(value))


def _run(model: Model, n: int, scenario: str) -> state.RunView | None:
    return views.run_model(
        compile_model(model), model_to_yaml(model), n, model.settings.seed, scenario
    )


def _checks(lesson: Lesson, run: state.RunView) -> list[Check]:
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
        (st.success if check.passed else st.error)(f"{text} – {status}")
    return checks


def _reference_curves(checks: list[Check], x: np.ndarray) -> list[Curve]:
    grid = np.linspace(float(np.min(x)), float(np.max(x)), 400)
    return [
        Curve(t("ref.analytic"), grid, check.cdf(grid)) for check in checks if check.cdf is not None
    ]


def _explain(lesson: Lesson) -> None:
    st.markdown(files.read_text(LESSONS / lesson.text))
    with st.expander(t("lesson.model_yaml")):
        st.code(files.read_text(LESSONS / lesson.model), language="yaml")
    st.markdown(t("lesson.sources") + "\n" + "\n".join(f"- {SOURCES[k]}" for k in lesson.sources))
    st.caption(t("lesson.illustrative"))


def _compare(lesson: Lesson, before: state.RunView, after: state.RunView) -> None:
    out = lesson.output
    unit = after.compiled.model.nodes[out].unit
    b, a = before.summaries[out], after.summaries[out]
    views.validity(after)
    st.markdown(
        views.table(
            [t("ui.metric"), t("lesson.before"), t("lesson.after"), t("lesson.diff")],
            compare_rows(b, a, unit),
        )
    )
    prediction = st.session_state.get(f"prediction_{lesson.id}")
    result = change_sentence(lesson.question.metric, b, a, unit)
    if prediction:
        st.markdown(t("lesson.prediction", prediction=prediction, result=result))
    else:
        st.markdown(t("lesson.result", result=result))
    st.info(t("lesson.rule", rule=lesson.rule))
    checks = _checks(lesson, after)
    if b.kind == "num":
        samples = {
            t("lesson.before"): before.result.samples[out],
            t("lesson.after"): after.result.samples[out],
        }
        curves = _reference_curves(checks, after.result.samples[out])
        views.chart(figures.compare_cdfs(samples, unit, curves), "lesson_compare")


def _copy(lesson: Lesson, model: Model) -> None:
    new_id = st.text_input(t("ui.copy_name"), value=f"{lesson.id}_eigen", key="lesson_copy_id")
    if st.button(t("ui.copy"), key="lesson_copy"):
        try:
            target = files.create_model_text(
                settings.models_dir(), new_id.strip(), model_to_yaml(model)
            )
        except InputError as exc:
            st.error(render(exc.issue))
        else:
            st.success(t("ui.copied", name=target.stem))


def _load(lesson: Lesson) -> Model | None:
    """The lesson model, if the lesson files exist and fit the manifest; problems are shown."""
    missing = [name for name in (lesson.model, lesson.text) if not (LESSONS / name).is_file()]
    if missing:
        st.error(t("lesson.missing", files=", ".join(missing)))
        return None
    base = files.load_model(LESSONS / lesson.model)
    problems = lesson_problems(lesson, base)
    for problem in problems:
        st.error(t("lesson.invalid", problem=problem))
    return None if problems else base


def _turn(lesson: Lesson, base: Model, n: int, before: state.RunView) -> None:
    st.subheader(t("lesson.turn"))
    start = current_value(base, lesson.knob.node, lesson.knob.field)
    value = float(
        st.select_slider(
            lesson.knob.label, options=lesson.knob.choices(), value=start, key=f"knob_{lesson.id}"
        )
    )
    runs = _runs()
    if st.button(t("lesson.turn_run"), key="lesson_turn"):
        turned = _run(
            with_value(base, lesson.knob.node, lesson.knob.field, value),
            n,
            _scenario(lesson, value),
        )
        if turned is not None:
            runs[f"{lesson.id}:turned"] = turned
            _progress().setdefault(lesson.id, set()).add("turned")
    after = runs.get(f"{lesson.id}:turned")
    if after is not None:
        _compare(lesson, before, after)


def _lesson(lesson: Lesson, base: Model) -> None:
    _progress().setdefault(lesson.id, set()).add("seen")
    _explain(lesson)
    st.subheader(t("lesson.predict"))
    st.radio(
        lesson.question.text, lesson.question.options, index=None, key=f"prediction_{lesson.id}"
    )
    st.subheader(t("lesson.simulate"))
    n = int(
        st.number_input(
            t("ui.n"),
            min_value=1000,
            max_value=2_000_000,
            value=base.settings.n,
            step=1000,
            key="lesson_n",
        )
    )
    start = current_value(base, lesson.knob.node, lesson.knob.field) or 0.0
    runs = _runs()
    if st.button(t("lesson.run"), key="lesson_run", type="primary"):
        run = _run(base, n, _scenario(lesson, start))
        if run is not None:
            runs[lesson.id] = run
            runs.pop(f"{lesson.id}:turned", None)
    before = runs.get(lesson.id)
    if before is not None:
        views.validity(before)
        views.render_output(before, lesson.output)
        _checks(lesson, before)
        _turn(lesson, base, n, before)
    st.subheader(t("lesson.copy"))
    knob_value = st.session_state.get(f"knob_{lesson.id}", start)
    _copy(lesson, with_value(base, lesson.knob.node, lesson.knob.field, float(knob_value)))


def body() -> None:
    st.title(t("ui.page_lernpfad"))
    manifest = manifest_from_yaml(files.read_text(LESSONS / "lernpfad.yaml"))
    lessons = {lesson.id: lesson for lesson in manifest.lessons}
    lesson_id = st.selectbox(
        t("lesson.choose"), list(lessons), format_func=lambda i: lessons[i].title, key="lesson"
    )
    lesson = lessons[str(lesson_id)]
    base = _load(lesson)
    if base is not None:
        _lesson(lesson, base)
    done = sum(1 for steps in _progress().values() if "turned" in steps)
    st.sidebar.markdown("\n".join(f"- {_label(item)}" for item in lessons.values()))
    st.sidebar.caption(t("lesson.progress", done=done, total=len(lessons)))
    st.caption(t("lesson.progress", done=done, total=len(lessons)))


views.run_page(body)
