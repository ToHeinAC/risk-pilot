"""Correlation groups: Gaussian copula with Spearman input, never repaired (M5 AK 1)."""

from pathlib import Path

import numpy as np
import pytest

from app.analysis.tornado import fixed
from app.engine.simulate import simulate
from app.errors import ModelError
from app.model.compile import CompiledModel, compile_model
from app.model.graph import Edge, edges
from app.model.scenarios import detach, diff, effective_model, validate
from app.model.schema import Model
from app.model.yaml_io import model_from_yaml

NODES = (
    "nodes:\n"
    "  a: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
    "  b: {type: uncertain, dist: lognormal, mu: 0, sigma: 0.5}\n"
    "  c: {type: uncertain, dist: uniform, low: 0, high: 1}\n"
    "  free: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
    "  e: {type: event, p: 0.3}\n"
    "  k: {type: uncertain, dist: poisson, rate: 2}\n"
    "  d: {type: derived, expr: 'a + b'}\n"
    "  y: {type: output, expr: 'a + b + c + free + e + k'}\n"
)
MATRIX = "[[1, 0.5, -0.3], [0.5, 1, 0.2], [-0.3, 0.2, 1]]"


def text(correlations: str = "", scenarios: str = "") -> str:
    return f"schema_version: 1\nmodel: m\n{NODES}{correlations}{scenarios}"


def group(nodes: str, matrix: str) -> str:
    return f"correlations:\n  g: {{nodes: {nodes}, spearman: {matrix}}}\n"


def compiled(correlations: str = "") -> CompiledModel:
    return compile_model(model_from_yaml(text(correlations)))


def codes(correlations: str) -> list[str]:
    with pytest.raises(ModelError) as exc:
        compiled(correlations)
    return [i.code for i in exc.value.issues]


def test_achieved_spearman_within_002_at_100000() -> None:
    c = compiled(group("[a, b, c]", MATRIX))
    result = simulate(c, n=100_000, seed=5)
    achieved = result.correlations["g"]
    target = np.array([[1, 0.5, -0.3], [0.5, 1, 0.2], [-0.3, 0.2, 1]])
    assert np.abs(achieved - target).max() <= 0.02


def test_nodes_outside_groups_keep_their_draws() -> None:
    plain = simulate(compiled(), n=1000, seed=1, keep="all").samples
    grouped = simulate(compiled(group("[a, b, c]", MATRIX)), n=1000, seed=1, keep="all").samples
    assert np.array_equal(plain["free"], grouped["free"])
    assert np.array_equal(plain["e"], grouped["e"])
    assert not np.array_equal(plain["b"], grouped["b"])


@pytest.mark.parametrize(
    ("block", "code"),
    [
        (group("[a]", "[[1]]"), "corr.too_small"),
        (group("[a, zz]", "[[1, 0], [0, 1]]"), "corr.node_unknown"),
        (group("[a, d]", "[[1, 0], [0, 1]]"), "corr.node_type"),
        (
            "correlations:\n  g: {nodes: [a, b], spearman: [[1, 0], [0, 1]]}\n"
            "  h: {nodes: [a, c], spearman: [[1, 0], [0, 1]]}\n",
            "corr.node_twice",
        ),
        (group("[a, b]", "[[1, 0, 0], [0, 1, 0]]"), "corr.shape"),
        (group("[a, b]", "[[1, 0.2], [0.2, 0.9]]"), "corr.diagonal"),
        (group("[a, b]", "[[1, 1.2], [1.2, 1]]"), "corr.range"),
        (group("[a, b]", "[[1, 0.2], [0.3, 1]]"), "corr.asymmetric"),
        (group("[a, b, c]", "[[1, 0.9, -0.9], [0.9, 1, 0.9], [-0.9, 0.9, 1]]"), "corr.not_psd"),
        (
            group("[a, b, c]", "[[1, 0.52, 0.03], [0.52, 1, 0.86], [0.03, 0.86, 1]]"),
            "corr.latent_not_psd",
        ),
    ],
)
def test_invalid_groups_rejected_not_repaired(block: str, code: str) -> None:
    assert code in codes(block)


def test_singular_matrix_allowed() -> None:
    c = compiled(group("[a, free]", "[[1, 1], [1, 1]]"))
    result = simulate(c, n=2000, seed=0, keep="all").samples
    assert np.corrcoef(result["a"], result["free"])[0, 1] == pytest.approx(1.0)


def test_discrete_members_get_ties_notice_and_events_correlate() -> None:
    c = compiled(group("[e, k, a]", "[[1, 0.6, 0.6], [0.6, 1, 0.6], [0.6, 0.6, 1]]"))
    assert "corr.discrete_ties" in [n.code for n in c.notices]
    samples = simulate(c, n=20_000, seed=0, keep="all").samples
    assert np.corrcoef(samples["e"], samples["a"])[0, 1] > 0.3


def test_scenario_replaces_matrix_and_unknown_group_rejected() -> None:
    crisis = (
        "scenarios:\n  krise:\n    name: Krise\n    why: W\n"
        "    correlations: {g: {spearman: [[1, 0.8], [0.8, 1]], why: Krise}}\n"
    )
    model = model_from_yaml(text(group("[a, b]", "[[1, 0.1], [0.1, 1]]"), crisis))
    effective = effective_model(model, "krise")
    assert effective.correlations["g"].spearman == [[1, 0.8], [0.8, 1]]
    assert validate(model)[0] == []
    wrong = crisis.replace("{g: {spearman", "{zz: {spearman")
    found = validate(model_from_yaml(text(group("[a, b]", "[[1, 0.1], [0.1, 1]]"), wrong)))[0]
    assert "scenario.corr_unknown" in [i.code for i in found]


def test_graph_has_correlation_edges() -> None:
    model = model_from_yaml(text(group("[a, b, c]", MATRIX)))
    found = [e for e in edges(model) if e.kind == "korrelation"]
    assert found == [
        Edge("a", "b", "korrelation"),
        Edge("a", "c", "korrelation"),
        Edge("b", "c", "korrelation"),
    ]


def test_detached_scenario_keeps_its_matrix() -> None:
    crisis = (
        "scenarios:\n  krise:\n    name: Krise\n    why: W\n"
        "    correlations: {g: {spearman: [[1, 0.8], [0.8, 1]]}}\n"
    )
    model = model_from_yaml(text(group("[a, b]", "[[1, 0.1], [0.1, 1]]"), crisis))
    frozen = detach(model, "krise")
    assert effective_model(frozen, "krise").correlations["g"].spearman == [[1, 0.8], [0.8, 1]]


T4 = Path(__file__).resolve().parent.parent / "examples" / "t4_portfolio.yaml"


def test_diff_shows_correlation_overrides() -> None:
    model = model_from_yaml(T4.read_text("utf-8"))
    rows = diff(model, "krise")
    assert [(r.node, r.field) for r in rows] == [("markt", "spearman")]
    assert rows[0].after == [[1, 0.8, 0.8], [0.8, 1, 0.8], [0.8, 0.8, 1]]


def test_scenario_matrix_reached_and_common_random_numbers_kept() -> None:
    model = model_from_yaml(T4.read_text("utf-8"))
    runs = {
        sid: simulate(compile_model(effective_model(model, sid)), n=20_000, seed=3)
        for sid in ("basis", "defensiv", "krise")
    }
    assert np.abs(runs["krise"].correlations["markt"][0, 1] - 0.8) <= 0.03
    basis = simulate(compile_model(effective_model(model, "basis")), n=2000, seed=3, keep="all")
    defensiv = simulate(
        compile_model(effective_model(model, "defensiv")), n=2000, seed=3, keep="all"
    )
    assert np.array_equal(basis.samples["l_aktien"], defensiv.samples["l_aktien"])


def test_detached_matrix_stays_when_main_matrix_changes() -> None:
    crisis = (
        "scenarios:\n  krise:\n    name: Krise\n    why: W\n"
        "    correlations: {g: {why: nur Begründung}}\n"
    )
    model = model_from_yaml(text(group("[a, b]", "[[1, 0.1], [0.1, 1]]"), crisis))
    frozen = detach(model, "krise")
    data = frozen.model_dump(mode="json", exclude_unset=True)
    data["correlations"]["g"]["spearman"] = [[1, 0.6], [0.6, 1]]
    changed = Model.model_validate(data)
    assert effective_model(changed, "krise").correlations["g"].spearman == [[1, 0.1], [0.1, 1]]


def test_tornado_fixed_member_leaves_partner_draws_unchanged() -> None:
    c = compiled(group("[a, b]", "[[1, 0.7], [0.7, 1]]"))
    base = simulate(c, n=1000, seed=2, keep="all").samples
    pinned = simulate(fixed(c, "a", 0.5), n=1000, seed=2, keep="all").samples
    assert np.array_equal(base["b"], pinned["b"])
