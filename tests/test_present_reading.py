"""Reading examples on the open model and reasons for empty evaluations (M8 AK 2, edge cases)."""

from pathlib import Path

import pytest

from app.analysis.compare import compare
from app.analysis.criticality import criticality
from app.analysis.riskmatrix import risk_matrix
from app.analysis.sensitivity import spearman
from app.analysis.sweep import plan_sweep, run_sweep
from app.analysis.tornado import tornado
from app.engine.simulate import simulate
from app.model.compile import CompiledModel, compile_model
from app.model.scenarios import effective_model
from app.model.yaml_io import model_from_yaml
from app.present import reading, structure
from app.present.reading import Empty, Sentence
from app.present.results import summaries_for
from app.present.text import number, percent

ROOT = Path(__file__).resolve().parent.parent
T1 = ROOT / "examples" / "t1_faltung.yaml"
T2 = ROOT / "examples" / "t2_terminplan.yaml"
NAMES = {"a": "Vorgang A", "b": "Vorgang B", "c": "Vorgang C", "nacharbeit": "Nacharbeit an B"}
NAMES |= {"pfad1": "Pfad 1", "ende": "Projektende"}
CONSTANT = (
    "schema_version: 1\nmodel: fest\nnodes:\n  k: {type: constant, value: 2}\n"
    "  y: {type: output, expr: k * 3}\n"
)
FLAG = (
    "schema_version: 1\nmodel: flag\nnodes:\n  e: {type: event, p: 0.3}\n"
    "  y: {type: output, expr: e}\n"
)


def t2(scenario: str = "basis") -> CompiledModel:
    return compile_model(effective_model(model_from_yaml(T2.read_text("utf-8")), scenario))


def sentence(r: reading.Reading) -> str:
    assert isinstance(r, Sentence), r
    return r.text


def reason(r: reading.Reading) -> str:
    assert isinstance(r, Empty), r
    return r.reason


def test_result_names_the_output_and_its_numbers() -> None:
    c = t2()
    result = simulate(c, n=5_000)
    summary = summaries_for(c, result)["ende"]
    text = sentence(reading.result(summary, "Projektende", "d"))
    assert "Projektende" in text
    assert number(summary.median or 0.0) in text
    assert percent(summary.target.p) in text  # pyright: ignore[reportOptionalMemberAccess]


def test_yes_no_output_reads_the_share_only() -> None:
    c = compile_model(model_from_yaml(FLAG))
    summary = summaries_for(c, simulate(c, n=5_000))["y"]
    text = sentence(reading.result(summary, "y", None))
    assert percent(summary.share.p) in text  # pyright: ignore[reportOptionalMemberAccess]
    assert "Median" not in text


def test_compare_reads_the_mean_difference() -> None:
    a = simulate(t2(), n=5_000).samples["ende"]
    b = simulate(t2("b_schneller"), n=5_000).samples["ende"]
    c = compare(a, b, target=t2().nodes["ende"].target)
    text = sentence(reading.compare(c, "Hauptszenario", "B −3 Tage", "Projektende", "d"))
    mean = c.estimate("mean")
    assert "„B −3 Tage“" in text
    assert number(abs(mean.diff)) in text
    assert "niedriger" in text


def test_criticality_names_the_most_critical_input_or_explains_why_empty() -> None:
    c = t2()
    samples = simulate(c, n=5_000, keep="all").samples
    crit = criticality(c, samples, "ende")
    text = sentence(reading.criticality(crit, NAMES, "Projektende", c))
    top_node, top = next((n, p) for n, p in crit.indices if c.nodes[n].type != "derived")
    assert NAMES[top_node] in text
    assert percent(top.p) in text
    c1 = compile_model(model_from_yaml(T1.read_text("utf-8")))
    crit1 = criticality(c1, simulate(c1, n=1_000, keep="all").samples, "s")
    assert "max" in reason(reading.criticality(crit1, {}, "Summe", c1))


def test_tornado_reads_the_largest_bar_with_its_numbers() -> None:
    c = t2()
    result = tornado(c, "ende", n=2_000, seed=1)
    text = sentence(reading.tornado(result, NAMES, "Projektende", "d"))
    top = result.bars[0]
    assert NAMES[top.node] in text
    assert number(top.low) in text
    assert number(top.high) in text


def test_rank_correlation_names_the_strongest_input() -> None:
    c = t2()
    rows = spearman(c, simulate(c, n=5_000, keep="all").samples, "ende")
    text = sentence(reading.rho(rows, NAMES, "Projektende"))
    top = max((r for r in rows if r.rho is not None), key=lambda r: abs(r.rho or 0))
    assert NAMES[top.node] in text
    assert number(top.rho or 0.0) in text


def test_risk_reads_the_event_or_explains_why_empty() -> None:
    c = t2("nacharbeit")
    rows = risk_matrix(c, simulate(c, n=5_000, keep="all").samples, "ende")
    text = sentence(reading.risk(rows, NAMES, "Projektende", "d"))
    assert "Nacharbeit an B" in text
    assert number(rows[0].diff.value) in text  # pyright: ignore[reportOptionalMemberAccess]
    c0 = t2()  # the rework never occurs in the main scenario
    rows0 = risk_matrix(c0, simulate(c0, n=2_000, keep="all").samples, "ende")
    assert "nicht bestimmbar" in reason(reading.risk(rows0, NAMES, "Projektende", "d"))
    assert "keine Ereignisse" in reason(reading.risk([], NAMES, "Projektende", "d"))


def test_sweep_reads_from_first_to_last_value() -> None:
    c = t2()
    plan = plan_sweep(c.model, "b", "mean", (10.0, 15.0, 20.0))
    series = structure.sweep_series(run_sweep(plan, "ende", n=2_000, seed=1), "mean")
    text = sentence(reading.sweep(series, "Vorgang B · mean", "Projektende", "d", share=False))
    assert number(series[0][1]) in text
    assert number(series[-1][1]) in text
    assert "steigt" in text


def test_graph_counts_missing_reasons() -> None:
    text = sentence(reading.graph(model_from_yaml(T2.read_text("utf-8"))))
    assert "Begründung" in text


@pytest.mark.parametrize("which", ["tornado", "rho", "sweep"])
def test_without_uncertain_inputs_nothing_shifts_the_result(which: str) -> None:
    c = compile_model(model_from_yaml(CONSTANT))
    found = reading.needs_uncertain(c)
    assert found is not None
    assert "unsicheren Eingaben" in found.reason
    assert reading.needs_uncertain(t2()) is None
    assert which  # the same reason serves all three tabs


def test_compare_without_sub_scenario_says_what_to_do() -> None:
    assert "Szenarien" in reading.NO_SCENARIOS.reason
