"""State of one browser tab: the open model, the current run and the run cache.

No UI import; the Streamlit app (until M7 ends) and the NiceGUI pages share these types.
"""

from dataclasses import dataclass, field

from app.analysis.stats import Summary
from app.engine.simulate import SimulationResult
from app.model.compile import CompiledModel


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
class Session:
    model: OpenModel | None = None
    run: RunView | None = None
    runs: dict[RunKey, RunView] = field(default_factory=dict[RunKey, RunView])
