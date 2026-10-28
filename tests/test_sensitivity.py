"""Spearman rank correlation per input, descriptive only (M4 AK 5)."""

from app.analysis.sensitivity import spearman
from app.engine.simulate import simulate
from app.messages import t
from app.model.compile import compile_model
from app.model.yaml_io import model_from_yaml

NODES = (
    "  a: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
    "  noise: {type: uncertain, dist: normal, mean: 0, sd: 0.1}\n"
    "  free: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
    "  e: {type: event, p: 0.5}\n"
    "  never: {type: event, p: 0}\n"
    "  y: {type: output, expr: '3 * a + noise + 0.01 * e'}\n"
)


def test_linear_input_high_independent_near_zero_sorted() -> None:
    c = compile_model(model_from_yaml(f"schema_version: 1\nmodel: m\nnodes:\n{NODES}"))
    rows = spearman(c, simulate(c, n=20_000, seed=2, keep="all").samples, "y")
    by_node = {row.node: row for row in rows}
    assert by_node["a"].rho is not None
    assert by_node["a"].rho > 0.9
    free = by_node["free"]
    assert free.rho is not None
    assert free.lo < 0 < free.hi
    assert abs(free.rho) < 0.03
    assert rows[0].node == "a"
    assert by_node["never"].rho is None  # constant input: no rank correlation
    assert rows[-1].node == "never"


def test_label_says_descriptive() -> None:
    assert "Deskriptiv" in t("analysis.rho_caption")
