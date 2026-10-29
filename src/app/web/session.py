"""State of one browser tab: the open model, the current run and the run cache.

No UI import: the pages build on these types, the logic stays testable without a browser.
"""

from dataclasses import dataclass, field
from pathlib import Path

from app.adapters import files, settings
from app.analysis.stats import Summary
from app.engine.simulate import SimulationResult
from app.errors import InputError
from app.messages import render, t
from app.model.compile import CompiledModel
from app.web.analysing import AnalysisState


@dataclass
class OpenModel:
    """The open model; ``draft`` is the edited text, ``file_text`` what is on disk."""

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


RunKey = tuple[str, int, int]  # (model hash, N, seed)


@dataclass
class CompareView:
    """Runs of the last comparison; ``text`` is the draft they were made from."""

    text: str
    ref: str
    runs: dict[str, RunView]


@dataclass
class LessonState:
    """Learning path of a tab; progress is not stored on disk (M4 E8)."""

    selected: str | None = None
    progress: dict[str, set[str]] = field(default_factory=dict[str, set[str]])  # seen, turned
    runs: dict[str, RunView] = field(default_factory=dict[str, RunView])  # id, "id:turned"
    predictions: dict[str, str] = field(default_factory=dict[str, str])
    knobs: dict[str, float] = field(default_factory=dict[str, float])


@dataclass
class Session:
    model: OpenModel | None = None
    run: RunView | None = None
    runs: dict[RunKey, RunView] = field(default_factory=dict[RunKey, RunView])
    compare: CompareView | None = None
    analysis: AnalysisState = field(default_factory=AnalysisState)
    lessons: LessonState = field(default_factory=LessonState)


def is_example(path: Path) -> bool:
    return settings.examples_dir().resolve() in path.resolve().parents


def open_model(session: Session, path: Path) -> None:
    """Open ``path``: tutorials read-only, the previous run is dropped."""
    session.model = OpenModel(str(path), files.read_text(path), readonly=is_example(path))
    session.run = None
    session.compare = None
    session.analysis = AnalysisState()


def save(model: OpenModel, force: bool) -> str | None:
    """Write the draft; refused (message) if the file changed since opening, unless forced."""
    expected = None if force else files.text_hash(model.file_text)
    try:
        files.save_model_text(Path(model.path), model.text, expected)
    except InputError as exc:
        return render(exc.issue)
    model.file_text = model.text
    return None


def copy_as(source: Path, new_id: str) -> tuple[bool, str]:
    """Copy a model as template under ``new_id``; never overwrites. (done, message)"""
    try:
        target = files.copy_model(source, settings.models_dir(), new_id.strip())
    except InputError as exc:
        return False, render(exc.issue)
    return True, t("ui.copied", name=target.stem)


def free_copy_id(source: Path) -> str:
    existing = {p.stem for p in files.list_models(settings.models_dir())}
    return files.suggest_id(f"{source.stem}_kopie", existing)
