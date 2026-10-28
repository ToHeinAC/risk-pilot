"""Lesson manifest (``examples/lernpfad/lernpfad.yaml``): schema and consistency checks."""

from typing import Literal, Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from app.errors import InputError, Issue, ModelError
from app.lessons.knob import current_value, with_value
from app.lessons.reference import REFERENCES
from app.lessons.sources import SOURCES
from app.model.compile import compile_model
from app.model.schema import Model, OutputNode


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Question(_Strict):
    text: str
    options: list[str] = Field(min_length=2)
    answer: int
    metric: Literal["mean", "sd", "share", "target"]

    @model_validator(mode="after")
    def _answer_is_option(self) -> Self:
        if not 0 <= self.answer < len(self.options):
            raise ValueError("answer muss eine der Optionen bezeichnen")
        return self


class KnobRange(_Strict):
    min: float
    max: float
    step: float = Field(gt=0)


class Knob(_Strict):
    node: str
    field: str
    label: str
    values: list[float] | None = None
    range: KnobRange | None = None

    @model_validator(mode="after")
    def _one_kind(self) -> Self:
        if (self.values is None) == (self.range is None):
            raise ValueError("genau eines von values und range angeben")
        return self

    def choices(self) -> list[float]:
        if self.values is not None:
            return [float(v) for v in self.values]
        assert self.range is not None
        count = round((self.range.max - self.range.min) / self.range.step)
        return [round(self.range.min + i * self.range.step, 10) for i in range(count + 1)]


class Lesson(_Strict):
    id: str
    title: str
    model: str
    text: str
    output: str
    rule: str
    question: Question
    knob: Knob
    reference: str | None = None
    sources: list[str] = []


class Manifest(_Strict):
    schema_: Literal[1] = Field(alias="schema")
    lessons: list[Lesson]


def manifest_from_yaml(text: str) -> Manifest:
    try:
        return Manifest.model_validate(yaml.safe_load(text))
    except ValidationError as exc:
        first = exc.errors()[0]
        loc = ".".join(str(p) for p in first["loc"])
        raise InputError(Issue("model.schema", params={"loc": loc, "msg": first["msg"]})) from exc


def _knob_problems(lesson: Lesson, model: Model) -> list[str]:
    knob = lesson.knob
    start = current_value(model, knob.node, knob.field)
    if start is None:
        return [f"Stellschraube {knob.node}.{knob.field} ist keine literale Zahl im Modell"]
    problems: list[str] = []
    if start not in knob.choices():
        problems.append(f"Ausgangswert {start} ist kein Wert der Stellschraube")
    for value in knob.choices():
        try:
            compile_model(with_value(model, knob.node, knob.field, value))
        except (ModelError, ValidationError):
            problems.append(f"Stellschraubenwert {value} ist ungültig")
    return problems


def lesson_problems(lesson: Lesson, model: Model) -> list[str]:
    """Everything that does not fit between manifest and lesson model (empty = consistent)."""
    problems = _knob_problems(lesson, model)
    if not isinstance(model.nodes.get(lesson.output), OutputNode):
        problems.append(f"Ausgabe {lesson.output} fehlt im Modell")
    if lesson.reference is not None and lesson.reference not in REFERENCES:
        problems.append(f"Referenz {lesson.reference} ist unbekannt")
    problems += [f"Quelle {key} ist unbekannt" for key in lesson.sources if key not in SOURCES]
    return problems
