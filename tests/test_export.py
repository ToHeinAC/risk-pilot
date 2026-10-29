"""Export of a run: metrics CSV, samples Parquet, standalone HTML report (M6 AK 4)."""

import csv
import io
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
import pytest

from app.adapters import export as export_adapter
from app.engine.simulate import SimulationResult, simulate
from app.model.compile import CompiledModel, compile_model
from app.model.scenarios import effective_model
from app.model.yaml_io import model_from_yaml
from app.present import export
from app.present.results import summaries_for

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def run(name: str, scenario: str = "basis") -> export.Report:
    text = (EXAMPLES / name).read_text("utf-8")
    compiled: CompiledModel = compile_model(effective_model(model_from_yaml(text), scenario))
    result: SimulationResult = simulate(compiled, n=3000, seed=1)
    summaries = summaries_for(compiled, result)
    return export.Report(compiled, result, summaries, f"Name {scenario}", text, scenario)


def rows(report: export.Report) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(export.metrics_csv(report))))


def test_metrics_csv_columns_and_values() -> None:
    report = run("t2_terminplan.yaml", "nacharbeit")
    found = rows(report)
    assert list(found[0]) == list(export.CSV_COLUMNS)
    ende = {r["metric"]: r for r in found if r["output"] == "ende"}
    assert {"mean", "sd", "median", "p5", "p50", "p95", "min", "max", "p_target"} <= set(ende)
    summary = report.summaries["ende"]
    assert float(ende["mean"]["value"]) == pytest.approx(summary.mean)
    assert float(ende["mean"]["se"]) == pytest.approx(summary.se)
    assert summary.target is not None
    assert float(ende["p_target"]["lo"]) == pytest.approx(summary.target.lo)
    assert ende["p50"]["label"].startswith("P50")
    assert {r["scenario"] for r in found} == {"nacharbeit"}  # the ID, as in the Parquet file
    quantile = report.summaries["ende"].quantiles[0]
    assert export.quantile_key(quantile.q) == "p5"
    assert export.quantile_key(0.025) == "p2.5"
    assert {r["n"] for r in found} == {"3000"}
    assert ende["mean"]["unit"] == "d"


def test_loss_horizon_and_share_rows() -> None:
    t4 = {r["metric"] for r in rows(run("t4_portfolio.yaml"))}
    assert {"p_loss", "var95", "es95"} <= t4
    t5 = {r["metric"] for r in rows(run("t5_fusion.yaml"))}
    assert "p_beyond" in t5


def test_samples_parquet_reads_back() -> None:
    report = run("t2_terminplan.yaml")
    table = pq.read_table(io.BytesIO(export_adapter.samples_parquet(report.result, "basis")))
    assert table.column_names == list(report.result.samples)
    assert np.array_equal(table.column("ende").to_numpy(), report.result.samples["ende"])
    meta = table.schema.metadata
    assert meta[b"model_hash"].decode() == report.result.meta["model_hash"]
    assert meta[b"scenario"] == b"basis"
    assert meta[b"seed"] == b"1"


def test_html_embeds_plotly_when_the_first_output_is_yes_no() -> None:
    report = run("t3_bahn.yaml")
    assert next(iter(report.summaries.values())).share is not None
    html = export.report_html(report)
    assert len(html) > 1_000_000  # plotly.js itself is inline
    assert "Im Modell liegen" in html  # the sentences of the result page


def test_html_report_is_standalone() -> None:
    report = run("t4_portfolio.yaml")
    html = export.report_html(report)
    assert html.startswith("<!DOCTYPE html>")
    assert 'src="http' not in html  # plotly is embedded, nothing loads from the net
    assert "Plotly" in html
    assert "Median" in html
    assert "Erreichte Rangkorrelation" in html
    assert "Illustrative Zahlen" in html
    assert "model: t4_portfolio" in html  # the model YAML at the end


def test_file_names() -> None:
    assert export.file_name("t2_terminplan", "basis", "kennzahlen.csv") == (
        "t2_terminplan_basis_kennzahlen.csv"
    )
