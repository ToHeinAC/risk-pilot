"""Reading examples on the open model, one per evaluation (M8 AK 2).

Each function takes the result the chart or table shows (no second computation) and returns a
sentence with the model's node names and numbers, or the reason why the evaluation stays empty.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from app.analysis.compare import Comparison
from app.analysis.criticality import Criticality
from app.analysis.riskmatrix import RiskRow
from app.analysis.sensitivity import RankCorrelation
from app.analysis.stats import Summary
from app.analysis.tornado import Tornado, run_count
from app.messages import t
from app.model.compile import CompiledModel
from app.model.schema import Model
from app.present.structure import missing_why
from app.present.text import number, percent


@dataclass(frozen=True)
class Sentence:
    text: str


@dataclass(frozen=True)
class Empty:
    reason: str


Reading = Sentence | Empty
NO_SCENARIOS = Empty(t("compare.need_two"))


def _u(unit: str | None) -> str:
    return f" {unit}" if unit else ""


def _amount(value: float, unit: str | None, share: bool) -> str:
    return percent(value) if share else f"{number(value)}{_u(unit)}"


def result(summary: Summary, name: str, unit: str | None) -> Reading:
    if summary.share is not None:
        return Sentence(t("read.share", name=name, p=percent(summary.share.p)))
    if summary.median is None:
        return Empty(t("read.no_values"))
    text = t("read.median", name=name, median=f"{number(summary.median)}{_u(unit)}")
    if summary.target is not None:
        text += " " + t("read.target", p=percent(summary.target.p))
    return Sentence(text)


def compare(c: Comparison, name_a: str, name_b: str, output: str, unit: str | None) -> Reading:
    metric = "share" if c.kind == "bool" else "mean"
    e = c.estimate(metric)
    if e.diff == 0:
        return Sentence(t("read.compare_same", b=name_b, a=name_a, name=output))
    word = t("read.higher") if e.diff > 0 else t("read.lower")
    amount = _amount(abs(e.diff), unit, share=False)
    if metric == "share":
        amount = t("read.points", diff=number(abs(e.diff) * 100))
    return Sentence(
        t("read.compare", b=name_b, a=name_a, name=output, amount=amount, direction=word)
    )


def graph(model: Model) -> Reading:
    missing = [node for node, flag in missing_why(model).items() if flag]
    if not missing:
        return Sentence(t("read.graph_complete", n=len(model.nodes)))
    return Sentence(t("read.graph_missing", n=len(model.nodes), k=len(missing)))


def criticality(
    crit: Criticality, names: Mapping[str, str], output: str, compiled: CompiledModel
) -> Reading:
    if not crit.selects_path:
        return Empty(t("analysis.crit_no_extremum"))
    inputs = [(n, p) for n, p in crit.indices if compiled.nodes[n].type != "derived"]
    if not inputs:
        return Empty(t("analysis.no_uncertain"))
    node, p = inputs[0]
    return Sentence(t("read.crit", node=names[node], p=percent(p.p), name=output))


def needs_uncertain(compiled: CompiledModel) -> Empty | None:
    """Tornado, sweep and Spearman need something uncertain that can shift the result."""
    return Empty(t("analysis.no_uncertain")) if run_count(compiled) == 0 else None


def tornado(result: Tornado, names: Mapping[str, str], output: str, unit: str | None) -> Reading:
    if not result.bars:
        return Empty(t("analysis.no_uncertain"))
    top = result.bars[0]
    share = result.metric == "target"
    return Sentence(
        t(
            "read.tornado",
            node=names[top.node],
            metric=t(f"analysis.metric_{result.metric}"),
            name=output,
            low=_amount(top.low, unit, share),
            high=_amount(top.high, unit, share),
        )
    )


def sweep(
    series: Sequence[tuple[float, float, float, float]],
    param: str,
    output: str,
    unit: str | None,
    share: bool,
) -> Reading:
    if len(series) < 2:
        return Empty(t("read.sweep_short"))
    (x0, y0, _, _), (x1, y1, _, _) = series[0], series[-1]
    word = t("read.rises") if y1 > y0 else t("read.falls") if y1 < y0 else t("read.stays")
    return Sentence(
        t(
            "read.sweep",
            name=output,
            direction=word,
            y0=_amount(y0, unit, share),
            y1=_amount(y1, unit, share),
            param=param,
            x0=number(x0),
            x1=number(x1),
        )
    )


def rho(rows: Sequence[RankCorrelation], names: Mapping[str, str], output: str) -> Reading:
    known = [r for r in rows if r.rho is not None]
    if not known:
        return Empty(t("analysis.no_uncertain"))
    top = max(known, key=lambda r: abs(r.rho or 0.0))
    assert top.rho is not None
    return Sentence(t("read.rho", node=names[top.node], name=output, rho=number(top.rho)))


def risk(
    rows: Sequence[RiskRow], names: Mapping[str, str], output: str, unit: str | None
) -> Reading:
    if not rows:
        return Empty(t("analysis.no_events"))
    defined = [r for r in rows if r.diff is not None]
    if not defined:
        return Empty(t("read.risk_undefined"))
    top = max(defined, key=lambda r: abs(r.diff.value) if r.diff else 0.0)
    assert top.diff is not None
    word = t("read.higher") if top.diff.value >= 0 else t("read.lower")
    return Sentence(
        t(
            "read.risk",
            node=names[top.node],
            p=percent(top.p.p),
            name=output,
            amount=f"{number(abs(top.diff.value))}{_u(unit)}",
            direction=word,
        )
    )
