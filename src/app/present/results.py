"""Summaries per output and the before/after table of the learning path."""

import math

from app.analysis.stats import Summary, summarize
from app.engine.simulate import SimulationResult
from app.messages import t
from app.model.compile import CompiledModel
from app.present.text import number, percent

Row = tuple[str, str, str, str]


def summaries_for(compiled: CompiledModel, result: SimulationResult) -> dict[str, Summary]:
    """Statistics of every output, with its target if it has one."""
    return {
        node_id: summarize(result.samples[node_id], target=node.target)
        for node_id, node in compiled.nodes.items()
        if node.type == "output"
    }


def _signed(value: float, unit: str) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{number(value)}{unit}"


def _num_row(label: str, before: float | None, after: float | None, unit: str) -> Row:
    b, a = before if before is not None else math.nan, after if after is not None else math.nan
    return label, f"{number(b)}{unit}", f"{number(a)}{unit}", _signed(a - b, unit)


def _share_row(label: str, before: float, after: float) -> Row:
    diff = number((after - before) * 100)
    sign = "+" if after > before else ""
    return label, percent(before), percent(after), t("result.points", diff=f"{sign}{diff}")


def compare_rows(before: Summary, after: Summary, unit: str | None) -> list[Row]:
    """(label, before, after, difference) for mean, median, sd, P10, P90 and shares."""
    if before.share is not None and after.share is not None:
        return [_share_row(t("result.share_label"), before.share.p, after.share.p)]
    u = f" {unit}" if unit else ""
    rows = [
        _num_row(t("result.mean"), before.mean, after.mean, u),
        _num_row(t("result.median"), before.median, after.median, u),
        _num_row(t("result.sd"), before.sd, after.sd, u),
    ]
    quantiles_after = {q.q: q.value for q in after.quantiles}
    rows += [
        _num_row(
            t("result.quantile_label", pct=number(q.q * 100)), q.value, quantiles_after.get(q.q), u
        )
        for q in before.quantiles
        if q.q in (0.1, 0.9)
    ]
    if before.target is not None and after.target is not None:
        rows.append(_share_row(t("result.target_label"), before.target.p, after.target.p))
    return rows


def _metric_value(metric: str, s: Summary) -> float | None:
    if metric in ("share", "target"):
        prop = s.share if metric == "share" else s.target
        return prop.p if prop is not None else None
    return s.mean if metric == "mean" else s.sd


_METRIC_LABELS = {
    "mean": "result.mean",
    "sd": "result.sd",
    "share": "result.share_label",
    "target": "result.target_label",
}


def change_sentence(metric: str, before: Summary, after: Summary, unit: str | None) -> str:
    """How a metric changed between two runs with the same seed (common random numbers)."""
    label = t(_METRIC_LABELS[metric])
    b, a = _metric_value(metric, before), _metric_value(metric, after)
    if b is None or a is None:
        return ""
    u = f" {unit}" if unit else ""
    shares = metric in ("share", "target")

    def fmt(v: float) -> str:
        return percent(v) if shares else f"{number(v)}{u}"

    amount = f"{number(abs(a - b) * 100)} {t('result.points_unit')}" if shares else fmt(abs(a - b))
    if abs(a - b) <= 1e-12 * max(1.0, abs(b)):
        return t("result.change_same", label=label, before=fmt(b))
    key = "result.change_up" if a > b else "result.change_down"
    return t(key, label=label, amount=amount, before=fmt(b), after=fmt(a))
