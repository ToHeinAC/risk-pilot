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


def test_horizon_rows_hide_mean_and_mark_quantiles() -> None:
    rng = np.random.default_rng(3)
    x = np.concatenate([rng.normal(2050, 5, 8000), np.full(2000, 2200.0)])
    s = summarize(x, horizon=2100)
    rows = dict(text.metric_rows(s, "Jahr"))
    assert rows["Mittelwert"].startswith("nicht bestimmbar: 20 % jenseits des Horizonts")
    assert rows["P95 (95-%-Quantil)"] == "> Horizont 2 100"
    assert rows["P10 (10-%-Quantil)"].startswith("2 04")
    assert rows["Anteil nicht im Horizont"].startswith("20 % [")
    q95 = next(q for q in s.quantiles if q.q == 0.95)
    assert "Horizont" in text.quantile_sentence(q95, "Jahr", 0.95, horizon=2100)
    assert s.beyond is not None
    assert "nicht erreicht" in text.beyond_sentence(2100, s.beyond, "Jahr")


def test_loss_rows_and_multimodal_sentence() -> None:
    x = np.random.default_rng(4).normal(100, 10, 50_000)
    rows = dict(text.metric_rows(summarize(x, loss_reference=100), "EUR"))
    assert {"P(Verlust)", "VaR 95 %", "ES 95 %"} <= set(rows)
    sentence = text.multimodal_sentence(3.0, 12.0, "min")
    assert "mehrere Gipfel" in sentence
    assert "3 min" in sentence


def test_all_beyond_horizon_rows_and_zero_values() -> None:
    rows = dict(text.metric_rows(summarize(np.full(100, 2200.0), horizon=2100), "Jahr"))
    for label in ("Median", "P5 (5-%-Quantil)", "P95 (95-%-Quantil)", "Kleinster Wert"):
        assert rows[label].startswith("> Horizont"), label
    zero = dict(text.metric_rows(summarize(np.array([-1.0, 0.0, 1.0])), None))
    assert zero["Median"] == "0"


def test_multimodal_hint_ignores_values_beyond_horizon() -> None:
    rng = np.random.default_rng(6)
    x = np.concatenate([rng.normal(2060, 5, 4000), np.full(6000, 2200.0)])
    assert text.multimodal_hint(x, summarize(x, horizon=2100), "Jahr") is None
    two = np.concatenate([rng.normal(0, 1, 6000), rng.normal(10, 1, 4000)])
    hint = text.multimodal_hint(two, summarize(two), "min")
    assert hint is not None
    assert "mehrere Gipfel" in hint
