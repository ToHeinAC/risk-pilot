"""Pydantic models of the YAML model format (schema version 1)."""

import keyword
import re
from typing import Annotated, Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.expr.functions import function_names

ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_WORDS = frozenset({"true", "false"} | {k.lower() for k in keyword.kwlist})

ParamValue = float | str | list[float]
TargetOp = Literal["le", "lt", "ge", "gt"]


def id_problem(value: str) -> str | None:
    """Return why ``value`` is not a valid ID, or None if it is."""
    if not ID_PATTERN.match(value):
        return "erlaubt sind a bis z, 0 bis 9 und _, zuerst ein Buchstabe, höchstens 64 Zeichen"
    if value in _WORDS or value in function_names():
        return "das Wort ist reserviert"
    return None


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Why(_Strict):
    text: str
    links: list[str] = []
    date: str | None = None


class Bounds(_Strict):
    min: float | None = None
    max: float | None = None


class Target(_Strict):
    le: float | None = None
    lt: float | None = None
    ge: float | None = None
    gt: float | None = None

    @model_validator(mode="after")
    def _exactly_one(self) -> Self:
        if sum(v is not None for v in (self.le, self.lt, self.ge, self.gt)) != 1:
            raise ValueError("genau einer von le, lt, ge, gt ist anzugeben")
        return self

    @property
    def op(self) -> TargetOp:
        for name in ("le", "lt", "ge", "gt"):
            if getattr(self, name) is not None:
                return name
        raise AssertionError("unreachable")  # pragma: no cover

    @property
    def value(self) -> float:
        result: float | None = getattr(self, self.op)
        assert result is not None
        return result


class _NodeBase(_Strict):
    name: str | None = None
    unit: str | None = None
    description: str | None = None
    why: str | Why | None = None
    tags: list[str] = []
    bounds: Bounds | None = None
    track: bool = False


class ConstantNode(_NodeBase):
    type: Literal["constant"]
    value: float


class UncertainNode(_NodeBase):
    """A random variable; its distribution parameters are extra fields."""

    model_config = ConfigDict(extra="allow", frozen=True)
    type: Literal["uncertain"]
    dist: str
    input: str = "params"

    @model_validator(mode="after")
    def _params_are_values(self) -> Self:
        for key, value in (self.model_extra or {}).items():
            if not isinstance(value, int | float | str | list) or isinstance(value, bool):
                raise ValueError(f"Parameter {key}: Zahl, Ausdruck oder Zahlenliste erwartet")
        return self

    def params(self) -> dict[str, ParamValue]:
        """Distribution parameters as given (numbers, expression strings, number lists)."""
        return dict(self.model_extra or {})


class EventNode(_NodeBase):
    type: Literal["event"]
    p: float | str


class ChoiceOption(_Strict):
    label: str
    weight: float = Field(ge=0)


class ChoiceNode(_NodeBase):
    type: Literal["choice"]
    options: list[ChoiceOption]

    @field_validator("options")
    @classmethod
    def _valid_options(cls, options: list[ChoiceOption]) -> list[ChoiceOption]:
        if len(options) < 2:
            raise ValueError("mindestens zwei Optionen")
        if len({o.label for o in options}) != len(options):
            raise ValueError("Optionsnamen müssen eindeutig sein")
        if sum(o.weight for o in options) <= 0:
            raise ValueError("die Summe der Gewichte muss größer als 0 sein")
        return options


class DerivedNode(_NodeBase):
    type: Literal["derived"]
    expr: str


class OutputNode(_NodeBase):
    type: Literal["output"]
    expr: str
    target: Target | None = None
    better: Literal["lower", "higher"] | None = None  # comparison direction without a target


Node = Annotated[
    ConstantNode | UncertainNode | EventNode | ChoiceNode | DerivedNode | OutputNode,
    Field(discriminator="type"),
]


class Settings(_Strict):
    n: int = 10000
    seed: int = Field(default=0, ge=0)

    @field_validator("n", mode="before")
    @classmethod
    def _float_text_to_int(cls, value: object) -> object:
        if isinstance(value, str):
            try:
                number = float(value)
            except ValueError:
                return value
            return int(number) if number.is_integer() else value
        return value


BASIS = "basis"  # ID of the main scenario: the model's own nodes


class Scenario(_Strict):
    """A sub-scenario: overrides on top of its parent, or (detached) a full set of nodes."""

    name: str
    why: str = Field(min_length=1)
    parent: str = BASIS
    overrides: dict[str, dict[str, Any]] = {}
    nodes: dict[str, Node] | None = None
    detached_from: str | None = None
    correlations: dict[str, Any] | None = None  # reserved for M5


class Model(_Strict):
    schema_version: int
    model: str
    title: str | None = None
    description: str | None = None
    settings: Settings = Settings()
    nodes: dict[str, Node] = {}
    scenarios: dict[str, Scenario] = {}
