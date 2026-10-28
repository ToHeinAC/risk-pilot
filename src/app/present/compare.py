"""Texts and tables of the comparison view."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
import numpy as np

from app.analysis.compare import Comparison, DiffEstimate
from app.messages import t
from app.present.text import number, percent

_LABELS = {
    "mean": "result.mean",
    "median": "result.median",
    "p10": "compare.p10",
    "p90": "compare.p90",
    "target": "result.target_label",
    "share": "result.share_label",
}


def _signed(x: float) -> str:
    return f"+{number(x)}" if x > 0 else number(x)


def _row(e: DiffEstimate, unit: str | None) -> tuple[str, str, str, str]:
    label = t(_LABELS[e.metric])
    if e.metric in ("target", "share"):
        diff = t(
            "compare.points",
            diff=_signed(e.diff * 100),
            lo=number(e.lo * 100),
            hi=number(e.hi * 100),
        )
        return label, percent(e.a), percent(e.b), diff
    u = f" {unit}" if unit else ""
    return (
        label,
        f"{number(e.a)}{u}",
        f"{number(e.b)}{u}",
        f"{_signed(e.diff)}{u} [{number(e.lo)} … {number(e.hi)}]",
    )


def compare_rows(c: Comparison, unit: str | None) -> list[tuple[str, str, str, str]]:
    """(label, A, B, B − A [95-%-Intervall]) per metric."""
    return [_row(e, unit) for e in c.estimates]


def better_sentence(c: Comparison, name_a: str, name_b: str) -> str:
    """How often B beats A, in model language; empty without a direction."""
    if c.better is None or c.worse is None:
        return ""
    return t(
        "compare.better",
        a=name_a,
        b=name_b,
        p=percent(c.better.p),
        lo=number(c.better.lo * 100),
        hi=number(c.better.hi * 100),
        ties=percent(c.ties.p),
        worse=percent(c.worse.p),
    )


def direction_sentence(c: Comparison, name_a: str, name_b: str) -> str:
    """Shares of smaller, equal and larger results when no direction says what is better."""
    if c.kind == "bool":
        return t("compare.same_bool", b=name_b, a=name_a, ties=percent(c.ties.p))
    return t(
        "compare.direction",
        a=name_a,
        b=name_b,
        lower=percent(c.lower.p),
        ties=percent(c.ties.p),
        higher=percent(c.higher.p),
    )


def d_rows(c: Comparison, unit: str | None) -> list[tuple[str, str]]:
    """Statistics of the per-iteration difference d = B − A."""
    u = f" {unit}" if unit else ""
    q10, q50, q90 = (float(v) for v in np.quantile(c.d, [0.1, 0.5, 0.9]))
    return [
        (t("result.mean"), f"{number(float(np.mean(c.d)))}{u}"),
        (t("result.median"), f"{number(q50)}{u}"),
        (t("compare.p10"), f"{number(q10)}{u}"),
        (t("compare.p90"), f"{number(q90)}{u}"),
        (t("compare.ties_label"), percent(c.ties.p)),
    ]
