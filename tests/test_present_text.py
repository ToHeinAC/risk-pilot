"""German result texts in model language (M2 AK 2, 8)."""

import numpy as np
import pytest

from app.analysis.stats import Proportion, QuantileEstimate, summarize
from app.model.schema import Target
from app.present import text


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (31.234, "31,2"),
        (0.0123456, "0,0123"),
        (100000, "100 000"),
        (26.6853, "26,7"),
        (-2.5, "-2,5"),
        (0.0, "0"),
        (float("nan"), "–"),
        (2026.4, "2 026"),
    ],
)
def test_number_format(value: float, expected: str) -> None:
    assert text.number(value) == expected


def test_integer_format() -> None:
    assert text.integer(100000) == "100 000"


def test_percent() -> None:
    assert text.percent(0.7413) == "74,1 %"
    assert text.percent(0.0) == "0 %"
    assert text.percent(1.0) == "100 %"


def test_quantile_sentence_in_model_language() -> None:
    q = QuantileEstimate(0.9, 31.234, 31.1, 31.3)
    assert text.quantile_sentence(q, "d", 0.95) == (
        "Im Modell liegen 90 % der Werte höchstens bei 31,2 d (95-%-Intervall 31,1 … 31,3 d)."
    )


def test_quantile_sentence_without_unit() -> None:
    q = QuantileEstimate(0.05, 0.5, 0.4, 0.6)
    assert text.quantile_sentence(q, None, 0.95).startswith(
        "Im Modell liegen 5 % der Werte höchstens bei 0,5 ("
    )


def test_target_sentence() -> None:
    prop = Proportion(741, 1000, 0.741, 0.712, 0.768)
    assert text.target_sentence(Target(le=30), prop, "d") == (
        "Im Modell wird das Ziel ≤ 30 d in 74,1 % der Iterationen erreicht (71,2 … 76,8 %)."
    )


def test_share_sentence_for_bool_output() -> None:
    prop = Proportion(826, 1000, 0.826, 0.8, 0.85)
    assert text.share_sentence(prop) == (
        "Im Modell trifft die Aussage in 82,6 % der Iterationen zu (80 … 85 %)."
    )


def test_validity_line() -> None:
    meta = {
        "model_id": "t2_terminplan",
        "model_hash": "3f9a1c2b" + "0" * 56,
        "n": 100000,
        "seed": 20261027,
        "timestamp": "2026-10-28T14:03:00+00:00",
    }
    assert text.validity_line(meta, "Hauptszenario") == (
        "Dieses Ergebnis gilt für Modell t2_terminplan (Hash 3f9a1c2b), Szenario Hauptszenario, "
        "N = 100 000, Seed 20261027, berechnet am 28.10.2026 14:03 UTC."
    )


def test_metric_rows_numeric() -> None:
    s = summarize(np.linspace(0.0, 10.0, 1001), target=Target(le=5))
    labels = [label for label, _ in text.metric_rows(s, "d")]
    assert labels[:3] == ["Mittelwert", "Median", "Standardabweichung"]
    assert "P(Ziel erreicht)" in labels
    assert "Relative Genauigkeit (SE / |Mittelwert|)" in labels
    assert any(label.startswith("P90") for label in labels)


def test_precision_hint_when_target_interval_wide() -> None:
    wide = summarize(np.arange(100.0), target=Target(le=50))
    narrow = summarize(np.arange(200000.0), target=Target(le=100000))
    assert text.precision_hints(wide)
    assert not text.precision_hints(narrow)
