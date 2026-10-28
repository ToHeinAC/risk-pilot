"""Learning path manifest: schema and consistency with the lesson models (M2 AK 9)."""

from pathlib import Path

import pytest

from app.adapters.files import load_model, read_text
from app.adapters.settings import examples_dir
from app.errors import InputError
from app.lessons.catalog import Lesson, lesson_problems, manifest_from_yaml
from app.lessons.reference import REFERENCES
from app.lessons.sources import SOURCES
from app.model.compile import compile_model

LESSON_DIR = examples_dir() / "lernpfad"
PATTERNS = {
    "a01_serie",
    "a02_parallel_und",
    "a03_parallel_oder",
    "a04_k_von_n",
    "a05_verzweigung",
    "a06_schwelle",
    "a07_bedingt",
    "a08_kette",
    "a09_jensen",
    "a10_gemeinsame_ursache",
}


def lessons() -> list[Lesson]:
    return manifest_from_yaml(read_text(LESSON_DIR / "lernpfad.yaml")).lessons


def test_ten_patterns_and_capstone() -> None:
    ids = [lesson.id for lesson in lessons()]
    assert set(ids) == PATTERNS | {"a11_zusammenspiel"}
    assert ids == sorted(ids)


@pytest.mark.parametrize("lesson", lessons(), ids=lambda lesson: lesson.id)
def test_lesson_is_complete_and_consistent(lesson: Lesson) -> None:
    model = load_model(LESSON_DIR / lesson.model)
    compile_model(model)
    assert lesson_problems(lesson, model) == []
    assert read_text(LESSON_DIR / lesson.text).strip()
    assert lesson.rule.strip()
    assert lesson.sources
    assert lesson.reference is not None or lesson.id == "a11_zusammenspiel"
    assert "illustrativ" in read_text(LESSON_DIR / lesson.model)


def test_problems_detected() -> None:
    lesson = lessons()[1]
    model = load_model(LESSON_DIR / lesson.model)
    broken = lesson.model_copy(
        update={
            "knob": lesson.knob.model_copy(update={"node": "fehlt"}),
            "output": "fehlt",
            "reference": "unbekannt",
            "sources": ["niemand2000"],
        }
    )
    problems = lesson_problems(broken, model)
    assert len(problems) == 4


def test_start_value_must_be_a_choice() -> None:
    lesson = next(lesson for lesson in lessons() if lesson.id == "a05_verzweigung")
    model = load_model(LESSON_DIR / lesson.model)
    bad = lesson.model_copy(update={"knob": lesson.knob.model_copy(update={"values": [0.1, 0.5]})})
    assert any("Ausgangswert" in p for p in lesson_problems(bad, model))


def test_knob_value_must_compile() -> None:
    lesson = next(lesson for lesson in lessons() if lesson.id == "a05_verzweigung")
    model = load_model(LESSON_DIR / lesson.model)
    bad = lesson.model_copy(update={"knob": lesson.knob.model_copy(update={"values": [0.2, 1.5]})})
    assert any("1.5" in p for p in lesson_problems(bad, model))


@pytest.mark.parametrize(
    "text",
    [
        "schema: 2\nlessons: []\n",
        "schema: 1\nlessons: [{id: x}]\n",
        "schema: 1\nlessons: [{id: a, title: T, model: m.yaml, text: t.md, output: y, rule: r, "
        "question: {text: q, options: [a, b], answer: 0, metric: median}, knob: {node: k, "
        "field: value, label: K, values: [1]}}]\n",
        "- a\n",
        "schema: 1\nlessons: [{id: a, title: T, model: m.yaml, text: t.md, output: y, rule: r, "
        "question: {text: q, options: [a, b], answer: 5, metric: mean}, "
        "knob: {node: k, field: value, label: K, values: [1, 2]}}]\n",
        "schema: 1\nlessons: [{id: a, title: T, model: m.yaml, text: t.md, output: y, rule: r, "
        "question: {text: q, options: [a, b], answer: 0, metric: mean}, "
        "knob: {node: k, field: value, label: K}}]\n",
    ],
)
def test_invalid_manifest(text: str) -> None:
    with pytest.raises(InputError) as exc:
        manifest_from_yaml(text)
    assert exc.value.issue.code == "model.schema"


def test_range_knob_choices() -> None:
    text = (
        "schema: 1\nlessons: [{id: a, title: T, model: m.yaml, text: t.md, output: y, rule: r, "
        "question: {text: q, options: [a, b], answer: 1, metric: mean}, "
        "knob: {node: k, field: value, label: K, range: {min: 1, max: 2, step: 0.5}}}]\n"
    )
    assert manifest_from_yaml(text).lessons[0].knob.choices() == [1.0, 1.5, 2.0]


def test_registries_cover_manifest() -> None:
    for lesson in lessons():
        assert lesson.reference is None or lesson.reference in REFERENCES
        assert set(lesson.sources) <= set(SOURCES)


def test_lesson_dir_exists() -> None:
    assert isinstance(LESSON_DIR, Path)
    assert (LESSON_DIR / "lernpfad.yaml").is_file()
