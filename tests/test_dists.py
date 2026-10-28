"""Distribution families: inversion against SciPy, input modes, parameter checks (M1 AK 1-3)."""

import math

import numpy as np
import pytest
from numpy.typing import NDArray
from scipy import stats

from app.analysis.analytic import dkw_epsilon, ks_distance
from app.dists.base import Family, Params, fill_defaults
from app.dists.registry import families, get_family
from app.engine.simulate import simulate
from app.errors import ModelError
from app.model.compile import compile_model
from app.model.yaml_io import model_from_yaml

N = 100_000
RNG_SEED = 20261027


def uniforms(n: int = N, seed: int = RNG_SEED) -> NDArray[np.float64]:
    return np.random.default_rng(seed).random(n)


def canon(family: Family, mode: str, given: dict[str, float]) -> Params:
    params = fill_defaults(family, mode, {k: np.asarray(float(v)) for k, v in given.items()})
    return family.to_canonical(mode, params)


def scalars(params: Params) -> dict[str, float]:
    return {k: float(v) for k, v in params.items()}


def test_sixteen_families_registered() -> None:
    assert sorted(families()) == sorted(
        [
            "uniform",
            "triangular",
            "pert",
            "normal",
            "truncnormal",
            "lognormal",
            "beta",
            "student_t",
            "exponential",
            "gamma",
            "weibull",
            "bernoulli",
            "discrete",
            "poisson",
            "piecewise",
            "empirical",
        ]
    )


CONTINUOUS = [
    ("uniform", "params", {"low": 2, "high": 5}),
    ("triangular", "params", {"low": 1, "mode": 2, "high": 6}),
    ("triangular", "three_point", {"low": 1, "mode": 1, "high": 6}),
    ("pert", "params", {"low": 8, "mode": 10, "high": 15}),
    ("pert", "three_point", {"low": 0, "mode": 3, "high": 3, "lambda": 2}),
    ("normal", "params", {"mean": 10, "sd": 2}),
    ("normal", "mean_sd", {"mean": -1, "sd": 0.5}),
    ("truncnormal", "params", {"mean": 0, "sd": 1, "lower": -0.5, "upper": 2}),
    ("truncnormal", "params", {"mean": 5, "sd": 2, "lower": 4}),
    ("lognormal", "params", {"mu": 1, "sigma": 0.4}),
    ("lognormal", "mean_sd", {"mean": 3, "sd": 1.5}),
    ("beta", "params", {"alpha": 2, "beta": 5}),
    ("beta", "mean_sd", {"mean": 30, "sd": 5, "low": 10, "high": 60}),
    ("student_t", "params", {"df": 4, "loc": 1, "scale": 2}),
    ("exponential", "params", {"rate": 0.5}),
    ("exponential", "mean", {"mean": 6}),
    ("gamma", "params", {"shape": 2.5, "scale": 3}),
    ("gamma", "mean_sd", {"mean": 10, "sd": 4}),
    ("weibull", "params", {"shape": 1.7, "scale": 3, "loc": 1}),
]


@pytest.mark.parametrize(("dist", "mode", "given"), CONTINUOUS)
def test_continuous_family_matches_scipy_cdf(dist: str, mode: str, given: dict[str, float]) -> None:
    family = get_family(dist)
    assert family is not None
    assert family.kind == "continuous"
    c = canon(family, mode, given)
    x = family.ppf(uniforms(), c)
    reference = family.reference(scalars(c))
    assert ks_distance(x, reference.cdf) < dkw_epsilon(N)


def wilson(k: int, n: int, z: float = 3.2905) -> tuple[float, float]:
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z / (1 + z * z / n) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return center - half, center + half


DISCRETE = [
    ("bernoulli", {"p": 0.3}, {0.0: 0.7, 1.0: 0.3}),
    ("poisson", {"rate": 2.0}, {float(k): float(stats.poisson.pmf(k, 2.0)) for k in range(6)}),
]


@pytest.mark.parametrize(("dist", "given", "expected"), DISCRETE)
def test_discrete_frequencies(
    dist: str, given: dict[str, float], expected: dict[float, float]
) -> None:
    family = get_family(dist)
    assert family is not None
    assert family.kind == "discrete"
    x = family.ppf(uniforms(), canon(family, "params", given))
    for value, prob in expected.items():
        lo, hi = wilson(int(np.sum(x == value)), N)
        assert lo <= prob <= hi, value


def test_discrete_values_and_weights() -> None:
    family = get_family("discrete")
    assert family is not None
    given = {"values": np.array([3.0, -1.0, 7.5]), "weights": np.array([1.0, 0.0, 3.0])}
    c = family.to_canonical("params", given)
    x = family.ppf(uniforms(), c)
    assert set(np.unique(x)) == {3.0, 7.5}
    for value, prob in ((3.0, 0.25), (7.5, 0.75)):
        lo, hi = wilson(int(np.sum(x == value)), N)
        assert lo <= prob <= hi, value
    assert c["cum"][-1] == 1.0


def test_bernoulli_extremes() -> None:
    family = get_family("bernoulli")
    assert family is not None
    u = uniforms(1000)
    assert np.all(family.ppf(u, {"p": np.asarray(0.0)}) == 0.0)
    assert np.all(family.ppf(u, {"p": np.asarray(1.0)}) == 1.0)


def test_lognormal_mean_sd_formula_exact() -> None:
    family = get_family("lognormal")
    assert family is not None
    c = canon(family, "mean_sd", {"mean": 3, "sd": 1.5})
    sigma2 = math.log(1 + 1.5**2 / 3**2)
    assert float(c["sigma"]) == pytest.approx(math.sqrt(sigma2), rel=1e-12)
    assert float(c["mu"]) == pytest.approx(math.log(3) - sigma2 / 2, rel=1e-12)


@pytest.mark.parametrize(
    ("dist", "given"),
    [
        ("beta", {"mean": 30, "sd": 5, "low": 10, "high": 60}),
        ("beta", {"mean": 0.2, "sd": 0.1}),
        ("gamma", {"mean": 10, "sd": 4}),
        ("lognormal", {"mean": 3, "sd": 1.5}),
        ("normal", {"mean": 3, "sd": 1.5}),
    ],
)
def test_mean_sd_modes_hit_moments(dist: str, given: dict[str, float]) -> None:
    family = get_family(dist)
    assert family is not None
    reference = family.reference(scalars(canon(family, "mean_sd", given)))
    assert reference.mean() == pytest.approx(given["mean"], rel=1e-9)
    assert reference.std() == pytest.approx(given["sd"], rel=1e-9)


def test_pert_mapping_and_default_lambda() -> None:
    family = get_family("pert")
    assert family is not None
    c = scalars(canon(family, "params", {"low": 8, "mode": 10, "high": 15}))
    assert c["alpha"] == pytest.approx(1 + 4 * 2 / 7)
    assert c["beta"] == pytest.approx(1 + 4 * 5 / 7)
    assert c["lambda"] == 4.0
    assert family.reference(c).mean() == pytest.approx((8 + 4 * 10 + 15) / 6)


def test_ppf_vectorised_over_parameters_and_monotone_in_u() -> None:
    family = get_family("normal")
    assert family is not None
    u = np.array([0.1, 0.5, 0.9])
    x = family.ppf(u, {"mean": np.array([0.0, 10.0, 20.0]), "sd": np.asarray(1.0)})
    np.testing.assert_allclose(x, [stats.norm.ppf(0.1), 10.0, 20 + stats.norm.ppf(0.9)])
    grid = np.linspace(0.001, 0.999, 999)
    for dist, mode, given in CONTINUOUS:
        fam = get_family(dist)
        assert fam is not None
        assert np.all(np.diff(fam.ppf(grid, canon(fam, mode, given))) >= 0), dist


def test_ppf_finite_at_extreme_uniforms() -> None:
    u = np.array([2.0**-53, 0.5, 1 - 2.0**-53])
    for dist, mode, given in CONTINUOUS:
        fam = get_family(dist)
        assert fam is not None
        assert np.all(np.isfinite(fam.ppf(u, canon(fam, mode, given)))), dist


INVALID = [
    ("uniform", "params", {"low": 2, "high": 1}, "high"),
    ("triangular", "params", {"low": 1, "mode": 0, "high": 3}, "mode"),
    ("triangular", "params", {"low": 1, "mode": 4, "high": 3}, "mode"),
    ("triangular", "params", {"low": 1, "mode": 1, "high": 1}, "high"),
    ("pert", "params", {"low": 1, "mode": 2, "high": 3, "lambda": 0}, "lambda"),
    ("pert", "params", {"low": 1, "mode": 5, "high": 3}, "mode"),
    ("normal", "params", {"mean": 0, "sd": 0}, "sd"),
    ("normal", "params", {"mean": 0, "sd": -1}, "sd"),
    ("truncnormal", "params", {"mean": 0, "sd": 1}, "lower"),
    ("truncnormal", "params", {"mean": 0, "sd": 1, "lower": 2, "upper": 1}, "upper"),
    ("truncnormal", "params", {"mean": 0, "sd": 1, "lower": 40, "upper": 41}, "lower"),
    ("truncnormal", "params", {"mean": 0, "sd": 0, "lower": 0}, "sd"),
    ("lognormal", "params", {"mu": 0, "sigma": 0}, "sigma"),
    ("lognormal", "mean_sd", {"mean": -1, "sd": 1}, "mean"),
    ("lognormal", "mean_sd", {"mean": 1, "sd": 0}, "sd"),
    ("beta", "params", {"alpha": 0, "beta": 1}, "alpha"),
    ("beta", "params", {"alpha": 1, "beta": -1}, "beta"),
    ("beta", "params", {"alpha": 1, "beta": 1, "low": 1, "high": 1}, "high"),
    ("beta", "mean_sd", {"mean": 1.5, "sd": 0.1}, "mean"),
    ("beta", "mean_sd", {"mean": 0.5, "sd": 0.6}, "sd"),
    ("student_t", "params", {"df": 2, "loc": 0, "scale": 1}, "df"),
    ("student_t", "params", {"df": 5, "loc": 0, "scale": 0}, "scale"),
    ("exponential", "params", {"rate": 0}, "rate"),
    ("exponential", "mean", {"mean": -2}, "mean"),
    ("gamma", "params", {"shape": 0, "scale": 1}, "shape"),
    ("gamma", "params", {"shape": 1, "scale": 0}, "scale"),
    ("gamma", "mean_sd", {"mean": 0, "sd": 1}, "mean"),
    ("gamma", "mean_sd", {"mean": 1, "sd": 0}, "sd"),
    ("weibull", "params", {"shape": 0, "scale": 1}, "shape"),
    ("weibull", "params", {"shape": 1, "scale": -1}, "scale"),
    ("bernoulli", "params", {"p": 1.2}, "p"),
    ("bernoulli", "params", {"p": -0.1}, "p"),
    ("poisson", "params", {"rate": -1}, "rate"),
]


@pytest.mark.parametrize(("dist", "mode", "given", "field"), INVALID)
def test_invalid_parameters_flagged(
    dist: str, mode: str, given: dict[str, float], field: str
) -> None:
    family = get_family(dist)
    assert family is not None
    params = fill_defaults(family, mode, {k: np.asarray(float(v)) for k, v in given.items()})
    violations = [v for v in family.check(mode, params) if np.any(v.mask)]
    assert field in {v.field for v in violations}


@pytest.mark.parametrize(("dist", "mode", "given"), CONTINUOUS)
def test_valid_parameters_pass(dist: str, mode: str, given: dict[str, float]) -> None:
    family = get_family(dist)
    assert family is not None
    params = fill_defaults(family, mode, {k: np.asarray(float(v)) for k, v in given.items()})
    assert not [v for v in family.check(mode, params) if np.any(v.mask)]


def test_nan_marks_unknown_parameters_as_not_violated() -> None:
    family = get_family("uniform")
    assert family is not None
    params = {"low": np.asarray(np.nan), "high": np.asarray(1.0)}
    assert not [v for v in family.check("params", params) if np.any(v.mask)]


@pytest.mark.parametrize(
    ("values", "weights", "field"),
    [
        ([], [], "values"),
        ([1, 2], [1], "weights"),
        ([1, 2], [1, -1], "weights"),
        ([1, 2], [0, 0], "weights"),
        ([1, 1], [1, 1], "values"),
    ],
)
def test_invalid_discrete(values: list[float], weights: list[float], field: str) -> None:
    family = get_family("discrete")
    assert family is not None
    params = {"values": np.asarray(values, float), "weights": np.asarray(weights, float)}
    violations = [v for v in family.check("params", params) if np.any(v.mask)]
    assert field in {v.field for v in violations}


def test_poisson_rate_zero_is_always_zero() -> None:
    family = get_family("poisson")
    assert family is not None
    assert np.all(family.ppf(uniforms(1000), {"rate": np.asarray(0.0)}) == 0.0)


def lists(**given: list[float]) -> Params:
    return {k: np.asarray(v, dtype=np.float64) for k, v in given.items()}


def test_piecewise_meets_ks_criterion() -> None:
    family = get_family("piecewise")
    assert family is not None
    assert family.kind == "continuous"
    c = family.to_canonical(
        "params", lists(probs=[0, 0.1, 0.5, 0.9, 1], values=[2030, 2034, 2040, 2052, 2080])
    )
    x = family.ppf(uniforms(), c)
    assert ks_distance(x, lambda t: np.interp(t, c["values"], c["probs"])) < dkw_epsilon(N)
    assert x.min() >= 2030
    assert x.max() <= 2080


@pytest.mark.parametrize(
    ("probs", "values", "field"),
    [
        ([0, 0.5, 1], [1, 1, 2], "values"),
        ([0, 0.5, 1], [3, 2, 4], "values"),
        ([0, 0.5, 0.5, 1], [1, 2, 3, 4], "probs"),
        ([0.1, 0.5, 1], [1, 2, 3], "probs"),
        ([0, 0.5, 0.9], [1, 2, 3], "probs"),
        ([0, 1], [1, 2, 3], "values"),
        ([0], [1], "probs"),
    ],
)
def test_invalid_piecewise(probs: list[float], values: list[float], field: str) -> None:
    family = get_family("piecewise")
    assert family is not None
    violations = [
        v for v in family.check("params", lists(probs=probs, values=values)) if v.mask.any()
    ]
    assert field in {v.field for v in violations}


def test_empirical_resamples_with_replacement() -> None:
    family = get_family("empirical")
    assert family is not None
    assert family.kind == "discrete"
    c = family.to_canonical("params", lists(values=[5, 1, 1, 9]))
    x = family.ppf(uniforms(), c)
    for value, prob in ((1.0, 0.5), (5.0, 0.25), (9.0, 0.25)):
        lo, hi = wilson(int(np.sum(x == value)), N)
        assert lo <= prob <= hi, value
    edge = family.ppf(np.array([2.0**-53, 1 - 2.0**-53]), c)
    assert edge.tolist() == [5.0, 9.0]
    assert [v.field for v in family.check("params", lists(values=[])) if v.mask.any()] == ["values"]


def test_piecewise_and_empirical_in_a_model() -> None:
    head = "schema_version: 1\nmodel: m\nnodes:\n"
    ok = (
        "  r: {type: uncertain, dist: piecewise, probs: [0, 0.5, 1], values: [1, 2, 4]}\n"
        "  e: {type: uncertain, dist: empirical, values: [3, 4]}\n"
        "  y: {type: output, expr: 'r + e'}\n"
    )
    x = simulate(compile_model(model_from_yaml(head + ok)), n=1000, seed=0).samples["y"]
    assert 4 <= x.min() <= x.max() <= 8
    bad = ok.replace("values: [1, 2, 4]", "values: [1, 2, 2]")
    with pytest.raises(ModelError) as exc:
        compile_model(model_from_yaml(head + bad))
    assert [(i.code, i.field) for i in exc.value.issues] == [("param.invalid", "values")]
