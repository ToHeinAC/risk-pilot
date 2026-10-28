"""Analytic references of the lessons hold at the start and at a turned knob (M2 AK 10)."""

import pytest

from app.adapters.files import load_model, read_text
from app.adapters.settings import examples_dir
from app.engine.simulate import simulate
from app.lessons.catalog import Lesson, manifest_from_yaml
from app.lessons.knob import current_value, with_value
from app.lessons.reference import REFERENCES
from app.model.compile import compile_model

LESSON_DIR = examples_dir() / "lernpfad"
LESSONS = [
    lesson
    for lesson in manifest_from_yaml(read_text(LESSON_DIR / "lernpfad.yaml")).lessons
    if lesson.reference is not None
]


def knob_values(lesson: Lesson) -> list[float]:
    model = load_model(LESSON_DIR / lesson.model)
    start = current_value(model, lesson.knob.node, lesson.knob.field)
    assert start is not None
    # The largest other value: the smallest is often degenerate (p = 0, one path, no common cause).
    turned = max(v for v in lesson.knob.choices() if v != start)
    return [start, turned]


CASES = [(lesson, value) for lesson in LESSONS for value in knob_values(lesson)]


@pytest.mark.parametrize(
    ("lesson", "value"), CASES, ids=[f"{lesson.id}={value}" for lesson, value in CASES]
)
def test_reference_criterion_holds(lesson: Lesson, value: float) -> None:
    base = load_model(LESSON_DIR / lesson.model)
    model = with_value(base, lesson.knob.node, lesson.knob.field, value)
    samples = simulate(compile_model(model), n=100_000).samples[lesson.output]
    assert lesson.reference is not None
    checks = REFERENCES[lesson.reference](model, samples)
    assert checks
    for check in checks:
        assert check.passed, (check.kind, check.expected, check.observed)


def test_every_pattern_lesson_has_reference() -> None:
    assert len(LESSONS) == 10
