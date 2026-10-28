"""Summaries per output and before/after comparison (M2 AK 2, 11)."""

import numpy as np

from app.analysis.stats import summarize
from app.engine.simulate import simulate
from app.model.compile import compile_model
from app.model.schema import Target
from app.model.yaml_io import model_from_yaml
from app.present.results import change_sentence, compare_rows, summaries_for


def test_summaries_use_output_targets() -> None:
    compiled = compile_model(
        model_from_yaml(
            "schema_version: 1\nmodel: m\nnodes:\n"
            "  a: {type: uncertain, dist: normal, mean: 10, sd: 2, track: true}\n"
            "  y: {type: output, expr: a, target: {le: 10}}\n  z: {type: output, expr: a > 12}\n"
        )
    )
    summaries = summaries_for(compiled, simulate(compiled, n=5000))
    assert set(summaries) == {"y", "z"}
    assert summaries["y"].target is not None
    assert summaries["z"].kind == "bool"


def test_compare_rows_numeric() -> None:
    before = summarize(np.arange(100.0))
    after = summarize(np.arange(100.0) + 2)
    rows = compare_rows(before, after, "d")
    labels = [r[0] for r in rows]
    assert labels[:2] == ["Mittelwert", "Median"]
    mean_row = rows[0]
    assert mean_row[1] == "49,5 d"
    assert mean_row[2] == "51,5 d"
    assert mean_row[3] == "+2 d"


def test_compare_rows_share() -> None:
    before = summarize(np.array([True, False, False, False]))
    after = summarize(np.array([True, True, False, False]))
    rows = compare_rows(before, after, None)
    assert rows == [("Anteil „trifft zu“", "25 %", "50 %", "+25 Prozentpunkte")]


def test_change_sentence_numeric_directions() -> None:
    before = summarize(np.arange(100.0))
    up = summarize(np.arange(100.0) + 2)
    assert change_sentence("mean", before, up, "d") == (
        "Mittelwert steigt um 2 d (von 49,5 d auf 51,5 d)."
    )
    assert change_sentence("mean", up, before, "d").startswith("Mittelwert sinkt um 2 d")
    assert change_sentence("mean", before, before, "d") == "Mittelwert bleibt gleich (49,5 d)."
    assert change_sentence("sd", before, summarize(np.arange(100.0) * 2), None).startswith(
        "Standardabweichung steigt um"
    )


def test_change_sentence_shares_and_target() -> None:
    a = summarize(np.array([True, False, False, False]))
    b = summarize(np.array([True, True, False, False]))
    assert change_sentence("share", b, a, None) == (
        "Anteil „trifft zu“ sinkt um 25 Prozentpunkte (von 50 % auf 25 %)."
    )
    x = summarize(np.arange(10.0), target=Target(le=4))
    y = summarize(np.arange(10.0), target=Target(le=6))
    assert change_sentence("target", x, y, None).startswith("P(Ziel erreicht) steigt um 20")
