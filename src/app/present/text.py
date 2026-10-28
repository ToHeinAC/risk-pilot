"""Numbers and result sentences in German model language."""

import math
from collections.abc import Mapping
from datetime import datetime
from typing import Any

import numpy as np
from numpy.typing import NDArray

from app.analysis.stats import Proportion, QuantileEstimate, Summary, multimodal
from app.messages import t
from app.model.schema import Target

_OPS = {"le": "≤", "lt": "<", "ge": "≥", "gt": ">"}
_THIN = " "
GROUP_FROM = 10_000  # four-digit numbers stay unseparated


def number(x: float, digits: int = 3) -> str:
    """Three significant digits, decimal comma, narrow space between thousands."""
    if not math.isfinite(x):
        return "–"
    if x == 0:
        return "0"
    decimals = max(0, digits - 1 - math.floor(math.log10(abs(x))))
    formatted = f"{x:{_group(x)}.{decimals}f}"
    if decimals:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted.replace(",", _THIN).replace(".", ",")


def _group(x: float) -> str:
    """Thousands separator only from five digits on (DIN 5008), so years read 2040, not 2 040."""
    return "," if abs(x) >= GROUP_FROM else ""


def decimal(x: float, places: int) -> str:
    """Fixed number of decimal places with a decimal comma."""
    return f"{x:.{places}f}".replace(".", ",")


def integer(n: int) -> str:
    return f"{n:{_group(n)}}".replace(",", _THIN)


def percent(p: float) -> str:
    return f"{number(p * 100)} %"


def _unit(unit: str | None) -> str:
    return f" {unit}" if unit else ""


def _bound(value: float, horizon: float | None) -> str:
    """An interval bound, or "> Horizont" beyond the horizon."""
    if horizon is not None and value > horizon:
        return t("result.beyond_value", horizon=number(horizon))
    return number(value)


def quantile_sentence(
    q: QuantileEstimate, unit: str | None, conf: float, horizon: float | None = None
) -> str:
    if horizon is not None and q.value > horizon:
        return t("result.quantile_beyond", pct=number(q.q * 100), horizon=number(horizon))
    return t(
        "result.quantile",
        pct=number(q.q * 100),
        value=number(q.value),
        lo=number(q.lo),
        hi=_bound(q.hi, horizon),
        unit=_unit(unit),
        conf=number(conf * 100),
    )


def beyond_sentence(horizon: float, prop: Proportion, unit: str | None) -> str:
    return t(
        "result.beyond",
        horizon=f"{number(horizon)}{_unit(unit)}",
        p=percent(prop.p),
        lo=number(prop.lo * 100),
        hi=number(prop.hi * 100),
    )


def multimodal_sentence(median: float, mode: float, unit: str | None) -> str:
    u = _unit(unit)
    return t("result.multimodal", median=f"{number(median)}{u}", mode=f"{number(mode)}{u}")


def target_sentence(target: Target, prop: Proportion, unit: str | None) -> str:
    return t(
        "result.target",
        op=_OPS[target.op],
        value=number(target.value),
        unit=_unit(unit),
        p=percent(prop.p),
        lo=number(prop.lo * 100),
        hi=number(prop.hi * 100),
    )


def share_sentence(prop: Proportion) -> str:
    return t("result.share", p=percent(prop.p), lo=number(prop.lo * 100), hi=number(prop.hi * 100))


def validity_line(meta: Mapping[str, object], scenario: str) -> str:
    stamp = datetime.fromisoformat(str(meta["timestamp"]))
    n = meta["n"]
    return t(
        "result.validity",
        model=meta["model_id"],
        hash=str(meta["model_hash"])[:8],
        scenario=scenario,
        n=integer(n) if isinstance(n, int) else n,
        seed=meta["seed"],
        time=stamp.strftime("%d.%m.%Y %H:%M"),
    )


def _proportion_row(label: str, prop: Proportion) -> tuple[str, str]:
    return label, f"{percent(prop.p)} [{number(prop.lo * 100)} … {number(prop.hi * 100)} %]"


def _relative(s: Summary) -> str:
    """Standard error relative to the mean: how precisely N iterations pin the mean down."""
    if not s.mean or not math.isfinite(s.se):
        return "–"
    return percent(s.se / abs(s.mean))


def _moment_rows(s: Summary, u: str) -> list[tuple[str, str]]:
    """Mean, sd and relative precision; with censored values not as numbers (they'd be biased)."""
    if s.beyond is not None and s.beyond.k > 0:
        hidden = t("result.censored", p=percent(s.beyond.p))
        return [(t("result.mean"), hidden), (t("result.sd"), hidden), (t("result.relative"), "–")]
    return [
        (t("result.mean"), f"{number(_num(s.mean))}{u} ± {number(s.se)} ({t('result.se')})"),
        (t("result.sd"), f"{number(_num(s.sd))}{u}"),
        (t("result.relative"), _relative(s)),
    ]


def _quantile_value(q: QuantileEstimate, u: str, horizon: float | None) -> str:
    if horizon is not None and q.value > horizon:
        return t("result.beyond_value", horizon=number(horizon))
    return f"{number(q.value)}{u} [{number(q.lo)} … {_bound(q.hi, horizon)}]"


def _loss_rows(s: Summary, u: str) -> list[tuple[str, str]]:
    if s.loss is None:
        return []
    var, pct = s.loss.var, number(s.loss.var.q * 100)
    return [
        _proportion_row(t("result.p_loss"), s.loss.p_loss),
        (t("result.var", pct=pct), f"{number(var.value)}{u} [{number(var.lo)} … {number(var.hi)}]"),
        (
            t("result.es", pct=pct),
            f"{number(s.loss.es)}{u} ± {number(s.loss.es_se)} ({t('result.se')})",
        ),
    ]


def metric_rows(s: Summary, unit: str | None) -> list[tuple[str, str]]:
    """(label, value) rows for the metrics table of one output."""
    if s.share is not None:
        return [_proportion_row(t("result.share_label"), s.share)]
    u = _unit(unit)
    moments = _moment_rows(s, u)
    rows = [
        moments[0],
        (t("result.median"), _capped(_num(s.median), u, s.horizon)),
        *moments[1:],
    ]
    rows += [
        (t("result.quantile_label", pct=number(q.q * 100)), _quantile_value(q, u, s.horizon))
        for q in s.quantiles
    ]
    rows += [
        (t("result.min"), _capped(_num(s.min), u, s.horizon)),
        (t("result.max"), _capped(_num(s.max), u, s.horizon)),
    ]
    if s.target is not None:
        rows.append(_proportion_row(t("result.target_label"), s.target))
    if s.beyond is not None:
        rows.append(_proportion_row(t("result.beyond_label"), s.beyond))
    return rows + _loss_rows(s, u)


def _num(x: float | None) -> float:
    """A missing value as NaN (shown as "–"); a true 0 stays 0."""
    return math.nan if x is None else x


def multimodal_hint(x: NDArray[Any], s: Summary, unit: str | None) -> str | None:
    """The several-peaks hint, judged on the values within the horizon only."""
    values = np.asarray(x, dtype=np.float64)
    if s.horizon is not None:
        values = values[values <= s.horizon]
    peaks = multimodal(values)
    if peaks is None:
        return None
    median = _num(s.median)
    if s.horizon is not None and median > s.horizon:
        return None  # the typical case lies beyond the horizon; the horizon line says so
    return multimodal_sentence(median, peaks[1], unit)


def _capped(value: float, u: str, horizon: float | None) -> str:
    """A value with unit, or "> Horizont" beyond the horizon."""
    if horizon is not None and value > horizon:
        return t("result.beyond_value", horizon=number(horizon))
    return f"{number(value)}{u}"


def precision_hints(s: Summary) -> list[str]:
    """Hints when a share is known to worse than ±1 percentage point."""
    hints: list[str] = []
    for label, prop in ((t("result.target_label"), s.target), (t("result.share_label"), s.share)):
        if prop is not None and (prop.hi - prop.lo) / 2 > 0.01:
            hints.append(t("result.precision_wide", what=label))
    return hints
