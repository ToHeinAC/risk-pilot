"""Numbers and result sentences in German model language."""

import math
from collections.abc import Mapping
from datetime import datetime

from app.analysis.stats import Proportion, QuantileEstimate, Summary
from app.messages import t
from app.model.schema import Target

_OPS = {"le": "≤", "lt": "<", "ge": "≥", "gt": ">"}
_THIN = " "


def number(x: float, digits: int = 3) -> str:
    """Three significant digits, decimal comma, narrow space between thousands."""
    if not math.isfinite(x):
        return "–"
    if x == 0:
        return "0"
    decimals = max(0, digits - 1 - math.floor(math.log10(abs(x))))
    formatted = f"{x:,.{decimals}f}"
    if decimals:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted.replace(",", _THIN).replace(".", ",")


def decimal(x: float, places: int) -> str:
    """Fixed number of decimal places with a decimal comma."""
    return f"{x:.{places}f}".replace(".", ",")


def integer(n: int) -> str:
    return f"{n:,}".replace(",", _THIN)


def percent(p: float) -> str:
    return f"{number(p * 100)} %"


def _unit(unit: str | None) -> str:
    return f" {unit}" if unit else ""


def quantile_sentence(q: QuantileEstimate, unit: str | None, conf: float) -> str:
    return t(
        "result.quantile",
        pct=number(q.q * 100),
        value=number(q.value),
        lo=number(q.lo),
        hi=number(q.hi),
        unit=_unit(unit),
        conf=number(conf * 100),
    )


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


def metric_rows(s: Summary, unit: str | None) -> list[tuple[str, str]]:
    """(label, value) rows for the metrics table of one output."""
    if s.share is not None:
        return [_proportion_row(t("result.share_label"), s.share)]
    u = _unit(unit)
    rows = [
        (t("result.mean"), f"{number(s.mean or math.nan)}{u} ± {number(s.se)} ({t('result.se')})"),
        (t("result.median"), f"{number(s.median or math.nan)}{u}"),
        (t("result.sd"), f"{number(s.sd or math.nan)}{u}"),
        (t("result.relative"), _relative(s)),
    ]
    rows += [
        (
            t("result.quantile_label", pct=number(q.q * 100)),
            f"{number(q.value)}{u} [{number(q.lo)} … {number(q.hi)}]",
        )
        for q in s.quantiles
    ]
    rows += [
        (t("result.min"), f"{number(s.min or math.nan)}{u}"),
        (t("result.max"), f"{number(s.max or math.nan)}{u}"),
    ]
    if s.target is not None:
        rows.append(_proportion_row(t("result.target_label"), s.target))
    return rows


def precision_hints(s: Summary) -> list[str]:
    """Hints when a share is known to worse than ±1 percentage point."""
    hints: list[str] = []
    for label, prop in ((t("result.target_label"), s.target), (t("result.share_label"), s.share)):
        if prop is not None and (prop.hi - prop.lo) / 2 > 0.01:
            hints.append(t("result.precision_wide", what=label))
    return hints
