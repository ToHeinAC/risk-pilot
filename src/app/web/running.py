"""Simulate, cache and save runs; no UI import."""

import dataclasses
import json
import time
from pathlib import Path

from app.adapters import files, runs, settings
from app.analysis.stats import summary_to_dict
from app.engine.simulate import simulate
from app.errors import ModelError
from app.messages import t
from app.model.compile import CompiledModel, compile_model, content_hash, model_hash
from app.model.scenarios import effective_model
from app.model.schema import BASIS
from app.model.yaml_io import model_from_yaml
from app.present.results import summaries_for
from app.web.session import RunKey, RunView


def template_and_hash(compiled: CompiledModel, text: str) -> tuple[str, str | None]:
    """The tutorial this model is (a copy of) and that tutorial's content hash, if any."""
    template = files.template_of(text) or compiled.model.model
    path = settings.examples_dir() / f"{template}.yaml"
    if not path.is_file():
        return template, None
    try:
        return template, content_hash(effective_model(files.load_model(path), BASIS))
    except ModelError:
        return template, None


def _full_hash(text: str, compiled: CompiledModel) -> str:
    """Hash of the whole model text (with scenarios); the effective model's if unparsable."""
    try:
        return model_hash(model_from_yaml(text))
    except ModelError:
        return compiled.model_hash


def compute_run(
    cache: dict[RunKey, RunView],
    compiled: CompiledModel,
    text: str,
    n: int,
    seed: int,
    scenario: str,
    scenario_id: str = BASIS,
    notices: list[str] | None = None,
) -> RunView:
    """Simulate, or reuse the cached run; raises ``SimulationError``."""
    key = (compiled.model_hash, n, seed)
    cached = cache.get(key)
    if cached is not None and cached.scenario == scenario:
        return cached
    started = time.perf_counter()
    result = simulate(compiled, n=n, seed=seed)
    seconds = time.perf_counter() - started
    meta = {
        **result.meta,
        "model_hash": _full_hash(text, compiled),
        "effective_hash": content_hash(compiled.model),
    }
    result = dataclasses.replace(result, meta=meta)
    template, original = template_and_hash(compiled, text)
    summaries = summaries_for(compiled, result)
    run = RunView(
        text,
        compiled,
        result,
        summaries,
        scenario,
        template,
        original,
        seconds,
        list(notices or []),
        scenario_id,
    )
    cache[key] = run
    return run


def load(path: Path) -> RunView:
    """A stored run, recomputed summaries included; a mismatch with the stored ones is noted."""
    stored = runs.load_run(path)
    scenario_id = str(stored.meta.get("scenario_id", BASIS))
    compiled = compile_model(effective_model(model_from_yaml(stored.model_text), scenario_id))
    result = runs.as_result(stored)
    summaries = summaries_for(compiled, result)
    fresh = {k: summary_to_dict(v) for k, v in summaries.items()}
    notices = [] if json.dumps(fresh) == json.dumps(stored.summary) else [t("ui.run_mismatch")]
    scenario = str(stored.meta.get("scenario", t("ui.main_scenario")))
    template, original = template_and_hash(compiled, stored.model_text)
    return RunView(
        stored.model_text,
        compiled,
        result,
        summaries,
        scenario,
        template,
        original,
        0.0,
        notices,
        scenario_id,
    )


def save(run: RunView) -> Path:
    """Store the run under ``data/runs/`` (samples, summaries, model text, scenario)."""
    summaries = {k: summary_to_dict(v) for k, v in run.summaries.items()}
    extra = {
        "scenario": run.scenario,
        "scenario_id": run.scenario_id,
        "scenario_name": run.scenario,
        "effective_hash": content_hash(run.compiled.model),
        "correlations": {g: m.tolist() for g, m in run.result.correlations.items()},
    }
    return runs.save_run(
        settings.runs_dir(), run.result.meta, run.model_text, run.result.samples, summaries, extra
    )
