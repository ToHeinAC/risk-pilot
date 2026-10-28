"""Stored runs: save, list, reload with the same numbers (M2 AK 5)."""

import json
from pathlib import Path

import numpy as np

from app.adapters import runs
from app.adapters.files import load_model, read_text
from app.analysis.stats import summarize, summary_to_dict
from app.engine.simulate import simulate
from app.model.compile import compile_model

ROOT = Path(__file__).resolve().parent.parent
T2 = ROOT / "examples" / "t2_terminplan.yaml"


def save_t2(directory: Path) -> Path:
    compiled = compile_model(load_model(T2))
    result = simulate(compiled, n=2000)
    summaries = {"ende": summary_to_dict(summarize(result.samples["ende"]))}
    return runs.save_run(
        directory,
        result.meta,
        read_text(T2),
        result.samples,
        summaries,
        {"scenario": "Hauptszenario"},
    )


def test_roundtrip_same_numbers(tmp_path: Path) -> None:
    path = save_t2(tmp_path)
    stored = runs.load_run(path)
    assert stored.model_text == read_text(T2)
    fresh = summary_to_dict(summarize(stored.samples["ende"]))
    assert json.dumps(fresh) == json.dumps(stored.summary["ende"])
    assert np.array_equal(stored.samples["pfad1"].shape, (2000,))


def test_meta_complete(tmp_path: Path) -> None:
    meta = runs.load_run(save_t2(tmp_path)).meta
    for key in ("model_hash", "seed", "n", "numpy", "scipy", "python", "risk_pilot", "timestamp"):
        assert key in meta
    assert meta["scenario"] == "Hauptszenario"
    assert meta["format_version"] == 1


def test_list_runs_newest_first_and_by_model(tmp_path: Path) -> None:
    first = save_t2(tmp_path)
    second = save_t2(tmp_path)
    assert first != second
    assert runs.list_runs(tmp_path, "t2_terminplan") == [second, first]
    assert runs.list_runs(tmp_path, "other") == []
    assert runs.list_runs(tmp_path / "missing") == []
    assert not list(tmp_path.glob("*.tmp"))
