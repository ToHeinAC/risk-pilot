"""Streams and vectorised simulation (M1 AK 5, 7-9 and runtime edge cases)."""

import math

import numpy as np
import pytest

from app.engine.simulate import SimulationResult, simulate
from app.engine.streams import stream_key, uniforms
from app.errors import SimulationError
from app.model.compile import compile_model
from app.model.yaml_io import model_from_yaml

SEED = 20261027


def run(nodes: str, n: int = 20_000, seed: int = SEED) -> SimulationResult:
    model = model_from_yaml(f"schema_version: 1\nmodel: m\nnodes:\n{nodes}")
    return simulate(compile_model(model), n=n, seed=seed)


def sim_error(nodes: str, n: int = 20_000) -> SimulationError:
    with pytest.raises(SimulationError) as exc:
        run(nodes, n)
    return exc.value


def within_4se(x: np.ndarray, expected: float) -> bool:
    return abs(float(x.mean()) - expected) < 4 * float(x.std(ddof=1)) / math.sqrt(x.size)


def test_uniforms_open_interval_and_deterministic() -> None:
    u = uniforms(SEED, "a", 50_000)
    assert u.min() > 0.0
    assert u.max() < 1.0
    np.testing.assert_array_equal(u, uniforms(SEED, "a", 50_000))
    assert not np.array_equal(u, uniforms(SEED, "b", 50_000))
    assert not np.array_equal(u, uniforms(SEED + 1, "a", 50_000))


def test_stream_key_is_sha256_prefix() -> None:
    assert stream_key("a") == int("ca978112ca1bbdca", 16)


def test_prefix_property() -> None:
    np.testing.assert_array_equal(uniforms(SEED, "a", 100), uniforms(SEED, "a", 1000)[:100])
    nodes = "  x: {type: uncertain, dist: normal, mean: 0, sd: 1}\n  y: {type: output, expr: x}\n"
    np.testing.assert_array_equal(run(nodes, 100).samples["y"], run(nodes, 1000).samples["y"][:100])


def test_conditional_distribution() -> None:
    result = run(
        "  e: {type: event, p: 0.3, track: true}\n"
        "  b: {type: uncertain, dist: normal, mean: '10 * e', sd: 1}\n"
        "  y: {type: output, expr: b}\n",
        n=100_000,
    )
    e, b = result.samples["e"], result.samples["y"]
    assert within_4se(b[e], 10.0)
    assert within_4se(b[~e], 0.0)


def test_invalid_expression_parameter_aborts_with_share() -> None:
    err = sim_error(
        "  x: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  b: {type: uncertain, dist: normal, mean: 0, sd: x}\n  y: {type: output, expr: b}\n"
    )
    issue = err.issue
    assert (issue.code, issue.node_id, issue.field) == ("runtime.param_invalid", "b", "sd")
    assert issue.share == pytest.approx(0.5, abs=0.02)


def test_invalid_event_probability_expression() -> None:
    err = sim_error(
        "  x: {type: uncertain, dist: uniform, low: 0, high: 2}\n"
        "  e: {type: event, p: x}\n  y: {type: output, expr: 'where(e, 1, 0)'}\n"
    )
    assert (err.issue.code, err.issue.node_id, err.issue.field) == (
        "runtime.param_invalid",
        "e",
        "p",
    )
    assert err.issue.share == pytest.approx(0.5, abs=0.02)


def test_shared_driver_drawn_once() -> None:
    result = run(
        "  x: {type: uncertain, dist: lognormal, mu: 0, sigma: 1}\n"
        "  a: {type: derived, expr: x, track: true}\n  b: {type: derived, expr: x, track: true}\n"
        "  y: {type: output, expr: x - x}\n"
    )
    np.testing.assert_array_equal(result.samples["a"], result.samples["b"])
    assert np.all(result.samples["y"] == 0.0)


BASE = (
    "  a: {type: uncertain, dist: normal, mean: 10, sd: 2, name: A}\n"
    "  b: {type: uncertain, dist: pert, low: 1, mode: 2, high: 5}\n"
    "  y: {type: output, expr: a + b}\n"
)


def test_bitwise_reproducible() -> None:
    np.testing.assert_array_equal(run(BASE).samples["y"], run(BASE).samples["y"])


def test_new_independent_node_keeps_draws() -> None:
    extended = (
        BASE
        + "  z: {type: uncertain, dist: gamma, shape: 2, scale: 1}\n  w: {type: output, expr: z}\n"
    )
    np.testing.assert_array_equal(run(BASE).samples["y"], run(extended).samples["y"])


def test_display_name_changes_nothing() -> None:
    renamed = BASE.replace("name: A", "name: Ganz anderer Name")
    np.testing.assert_array_equal(run(BASE).samples["y"], run(renamed).samples["y"])


def test_constant_exact_and_event_extremes() -> None:
    result = run(
        "  c: {type: constant, value: 3.25}\n"
        "  never: {type: event, p: 0, track: true}\n  always: {type: event, p: 1, track: true}\n"
        "  y: {type: output, expr: c}\n"
    )
    assert np.all(result.samples["y"] == 3.25)
    assert not result.samples["never"].any()
    assert result.samples["always"].all()


def test_event_monotone_coupling() -> None:
    low = run("  e: {type: event, p: 0.2}\n  y: {type: output, expr: e}\n").samples["y"]
    high = run("  e: {type: event, p: 0.5}\n  y: {type: output, expr: e}\n").samples["y"]
    assert np.all(high[low])
    assert high.sum() > low.sum()


def test_choice_frequencies_and_comparison() -> None:
    result = run(
        "  r: {type: choice, options: [{label: ICE, weight: 3}, {label: Bus, weight: 1}]}\n"
        "  y: {type: output, expr: 'r == \"Bus\"'}\n",
        n=100_000,
    )
    assert result.samples["y"].mean() == pytest.approx(0.25, abs=0.01)


def test_bounds_violation_is_notice_without_clipping() -> None:
    result = run(
        "  a: {type: uncertain, dist: normal, mean: 0, sd: 1, bounds: {min: 0}, track: true}\n"
        "  y: {type: output, expr: a}\n"
    )
    notice = next(w for w in result.warnings if w.code == "range.violation")
    assert notice.node_id == "a"
    assert notice.params["below"] == pytest.approx(0.5, abs=0.02)
    assert notice.params["above"] == 0.0
    assert result.samples["a"].min() < 0


def test_non_finite_result_aborts_with_share() -> None:
    err = sim_error(
        "  x: {type: uncertain, dist: uniform, low: -1, high: 1}\n"
        "  y: {type: output, expr: 'log(max(x, 0))'}\n"
    )
    assert (err.issue.code, err.issue.node_id) == ("runtime.non_finite", "y")
    assert err.issue.share == pytest.approx(0.5, abs=0.02)


def test_non_finite_in_unchosen_branch_is_fine() -> None:
    result = run(
        "  x: {type: uncertain, dist: uniform, low: -1, high: 1}\n"
        "  y: {type: output, expr: 'where(x > 0, log(where(x > 0, x, 0)), 0)'}\n"
    )
    assert np.all(np.isfinite(result.samples["y"]))


def test_clip_bounds_runtime_error_names_node() -> None:
    err = sim_error(
        "  x: {type: uncertain, dist: uniform, low: 0, high: 2}\n"
        "  y: {type: output, expr: 'clip(1, x, 1)'}\n"
    )
    assert (err.issue.code, err.issue.node_id) == ("runtime.clip_bounds", "y")


def test_degenerate_uniform_is_constant() -> None:
    result = run(
        "  a: {type: uncertain, dist: uniform, low: 3, high: 3}\n  y: {type: output, expr: a}\n"
    )
    assert np.all(result.samples["y"] == 3.0)
    assert [w.code for w in result.warnings] == ["uniform.degenerate"]


@pytest.mark.parametrize("n", [0, 2_000_001])
def test_n_range(n: int) -> None:
    assert sim_error("  y: {type: output, expr: '1'}\n", n=n).issue.code == "sim.n_range"


def test_defaults_from_settings_and_meta() -> None:
    model = model_from_yaml(
        "schema_version: 1\nmodel: m\nsettings: {n: 123, seed: 7}\n"
        "nodes:\n  a: {type: uncertain, dist: normal, mean: 0, sd: 1}\n"
        "  y: {type: output, expr: a}\n"
    )
    compiled = compile_model(model)
    result = simulate(compiled)
    meta = result.meta
    assert result.samples["y"].shape == (123,)
    assert (meta["n"], meta["seed"], meta["model_id"]) == (123, 7, "m")
    assert meta["model_hash"] == compiled.model_hash
    assert meta["generator"] == "PCG64"
    assert meta["stream_derivation"] == "sha256-spawn-key-v1"
    for key in ("risk_pilot", "numpy", "scipy", "python", "timestamp", "schema_version"):
        assert key in meta
    assert set(result.samples) == {"y"}
    assert result.canonical["a"]["canonical"] == {"mean": 0.0, "sd": 1.0}


def test_bool_output_and_tracked_types() -> None:
    result = run("  e: {type: event, p: 0.5}\n  y: {type: output, expr: 'e or false'}\n")
    assert result.samples["y"].dtype == np.bool_
    assert result.samples["y"].shape == (20_000,)


def test_unused_node_changes_no_output() -> None:
    extended = BASE + "  unused: {type: derived, expr: 'a * 100'}\n"
    np.testing.assert_array_equal(run(BASE).samples["y"], run(extended).samples["y"])


@pytest.mark.parametrize("k", [0.5, 3.0])
def test_scaling_scales_mean_and_quantiles(k: float) -> None:
    base = run(BASE).samples["y"]
    scaled = run(BASE.replace("expr: a + b", f"expr: '{k} * (a + b)'")).samples["y"]
    assert scaled.mean() == pytest.approx(k * base.mean(), rel=1e-12)
    np.testing.assert_allclose(np.quantile(scaled, [0.1, 0.9]), k * np.quantile(base, [0.1, 0.9]))


def test_higher_mean_of_a_summand_lowers_no_iteration() -> None:
    base = run(BASE).samples["y"]
    higher = run(BASE.replace("mean: 10", "mean: 11")).samples["y"]
    assert np.all(higher >= base)


@pytest.mark.parametrize("n", [10.5, True])
def test_n_must_be_integer(n: object) -> None:
    compiled = compile_model(
        model_from_yaml("schema_version: 1\nmodel: m\nnodes:\n  y: {type: output, expr: '1'}\n")
    )
    with pytest.raises(SimulationError) as exc:
        simulate(compiled, n=n)  # pyright: ignore[reportArgumentType]
    assert exc.value.issue.code == "sim.n_range"


@pytest.mark.parametrize("seed", [-1, 1.5])
def test_seed_must_be_non_negative_integer(seed: object) -> None:
    compiled = compile_model(
        model_from_yaml("schema_version: 1\nmodel: m\nnodes:\n  y: {type: output, expr: '1'}\n")
    )
    with pytest.raises(SimulationError) as exc:
        simulate(compiled, n=10, seed=seed)  # pyright: ignore[reportArgumentType]
    assert exc.value.issue.code == "sim.seed_range"
