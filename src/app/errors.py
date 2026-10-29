"""Error and notice types. Objects carry stable codes and parameters, never text."""

from collections.abc import Mapping
from dataclasses import dataclass
from dataclasses import field as dc_field

# Code -> names of the parameters its message template uses.
CODES: dict[str, tuple[str, ...]] = {
    "yaml.syntax": ("problem",),
    "yaml.duplicate_key": ("key",),
    "model.schema": ("loc", "msg"),
    "model.schema_version": ("version",),
    "model.no_output": (),
    "model.empty": (),
    "node.id_invalid": ("id", "reason"),
    "dist.unknown": ("dist", "known"),
    "dist.mode_unknown": ("dist", "mode", "modes"),
    "param.missing": ("dist", "mode"),
    "param.unknown": ("dist", "mode", "allowed"),
    "param.invalid": ("value", "rule"),
    "expr.syntax": ("expr", "problem"),
    "expr.forbidden": ("construct", "hint"),
    "expr.unknown_name": ("name", "suggestion"),
    "expr.unknown_function": ("name",),
    "expr.arity": ("name", "expected", "got"),
    "expr.type": ("expected", "got", "context"),
    "expr.too_long": ("length", "limit"),
    "expr.too_deep": ("depth", "limit"),
    "expr.too_large": ("size", "limit"),
    "expr.unknown_label": ("label", "choice", "labels"),
    "expr.choice_usage": ("choice",),
    "expr.interp_table": ("reason",),
    "graph.cycle": ("cycle",),
    "sim.n_range": ("n",),
    "sim.seed_range": ("seed",),
    "runtime.param_invalid": ("rule",),
    "runtime.non_finite": (),
    "runtime.clip_bounds": (),
    "range.violation": ("below", "above"),
    "uniform.degenerate": ("value",),
    "fit.deviation": ("dist", "deviation", "given", "fitted"),
    "fit.conflict": ("dist", "deviation", "given", "fitted"),
    "fit.bounds": ("p10", "p90"),
    "stats.single_sample": (),
    "stats.quantile_range": ("q",),
    "files.exists": ("name", "suggestion"),
    "scenario.id_invalid": ("id", "reason"),
    "scenario.parent_unknown": ("parent",),
    "scenario.parent_cycle": ("cycle",),
    "scenario.node_unknown": (),
    "scenario.field_invalid": (),
    "scenario.type_change": (),
    "scenario.corr_unknown": ("group",),
    "scenario.corr_field": ("group",),
    "corr.too_small": ("group",),
    "corr.node_unknown": ("group", "name"),
    "corr.node_type": ("group", "type"),
    "corr.node_twice": ("groups",),
    "corr.node_repeated": ("group",),
    "corr.shape": ("group", "k"),
    "corr.diagonal": ("group",),
    "corr.range": ("group",),
    "corr.asymmetric": ("group", "row", "col"),
    "corr.not_psd": ("group", "eig"),
    "corr.latent_not_psd": ("group", "eig"),
    "corr.discrete_ties": ("group", "nodes"),
    "scenario.inactive": (),
    "scenario.same_value": (),
    "files.changed": ("name",),
    "csv.encoding": (),
    "csv.column": ("column", "columns"),
    "csv.number": ("value", "column"),
    "csv.too_many": ("count", "limit"),
}


@dataclass(frozen=True)
class Issue:
    """A problem that stops validation or simulation."""

    code: str
    node_id: str | None = None
    field: str | None = None
    line: int | None = None
    params: Mapping[str, object] = dc_field(default_factory=dict[str, object])
    share: float | None = None
    scenario: str | None = None


@dataclass(frozen=True)
class Notice:
    """A hint that does not stop anything."""

    code: str
    node_id: str | None = None
    share: float | None = None
    params: Mapping[str, object] = dc_field(default_factory=dict[str, object])
    scenario: str | None = None


class RiskPilotError(Exception):
    """Base class of all Risk Pilot errors."""


class ModelError(RiskPilotError):
    """All problems found in a model at once."""

    def __init__(self, issues: list[Issue]) -> None:
        super().__init__(", ".join(i.code for i in issues))
        self.issues = issues


class SimulationError(RiskPilotError):
    """A problem that aborts a running simulation."""

    def __init__(self, issue: Issue) -> None:
        super().__init__(issue.code)
        self.issue = issue


class InputError(RiskPilotError):
    """An invalid argument from the caller, e.g. a quantile outside (0, 1)."""

    def __init__(self, issue: Issue) -> None:
        super().__init__(issue.code)
        self.issue = issue
