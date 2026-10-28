"""Analytic overlay for tutorials T1 and T2 (M2 AK 3)."""

from pathlib import Path

import numpy as np
import yaml

from app.adapters.files import load_model
from app.engine.simulate import simulate
from app.model.compile import compile_model, content_hash
from app.model.yaml_io import model_from_yaml, model_to_yaml
from app.present.references import tutorial_reference

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def run(name: str) -> tuple[str, str, dict[str, np.ndarray]]:
    compiled = compile_model(load_model(EXAMPLES / name))
    result = simulate(compiled)
    return compiled.model.model, content_hash(compiled.model), dict(result.samples)


def test_t1_reference_passes_dkw() -> None:
    model_id, model_hash, samples = run("t1_faltung.yaml")
    ref = tutorial_reference(model_id, model_hash, model_hash, samples)
    assert ref is not None
    assert ref.output == "s"
    assert ref.ks < ref.eps
    assert ref.passed
    assert {c.label for c in ref.cdf} >= {"Analytisch", "Numerische Faltung"}
    assert any("Faltung" in note for note in ref.notes)


def test_t2_reference_passes_dkw_and_shows_clark() -> None:
    model_id, model_hash, samples = run("t2_terminplan.yaml")
    ref = tutorial_reference(model_id, model_hash, model_hash, samples)
    assert ref is not None
    assert ref.output == "ende"
    assert ref.passed
    assert any("Clark" in note for note in ref.notes)
    pdf = ref.pdf[0]
    assert abs(float(np.trapezoid(pdf.y, pdf.x)) - 1) < 0.01


def test_changed_copy_has_no_reference() -> None:
    original = compile_model(load_model(EXAMPLES / "t1_faltung.yaml"))
    data = yaml.safe_load(model_to_yaml(original.model))
    data["nodes"]["x1"]["high"] = 2
    changed = model_from_yaml(yaml.safe_dump(data))
    compiled = compile_model(changed)
    samples = dict(simulate(compiled, n=1000).samples)
    assert (
        tutorial_reference("t1_faltung", compiled.model_hash, original.model_hash, samples) is None
    )


def test_unknown_model_has_no_reference() -> None:
    assert tutorial_reference("eigenes", "h", None, {"s": np.zeros(3)}) is None
