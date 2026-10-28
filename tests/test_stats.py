"""Summary statistics with numerical uncertainty (M1 AK 10)."""

import math

import numpy as np
import pytest
from scipy import stats

from app.analysis.stats import summarize, wilson
from app.errors import InputError
from app.model.schema import Target


def test_mean_and_standard_error() -> None:
    s = summarize(np.array([1.0, 2.0, 3.0, 4.0]))
    sd = math.sqrt(5 / 3)
    assert s.kind == "num"
    assert s.n == 4
    assert s.mean == pytest.approx(2.5)
    assert s.sd == pytest.approx(sd)
    assert s.var == pytest.approx(5 / 3)
    assert s.se == pytest.approx(sd / 2)
    assert (s.min, s.max, s.median) == (1.0, 4.0, 2.5)
    assert s.method == "quantile: Hyndman-Fan type 7; CI: order statistics; P: Wilson"


def test_quantile_ci_ranks_match_binomial() -> None:
    x = np.arange(1.0, 101.0)
    q = next(e for e in summarize(x, quantiles=(0.5,), conf=0.95).quantiles if e.q == 0.5)
    lower_rank = int(stats.binom.ppf(0.025, 100, 0.5))
    upper_rank = int(stats.binom.ppf(0.975, 100, 0.5)) + 1
    assert (q.lo, q.hi) == (float(lower_rank), float(upper_rank))
    assert q.value == pytest.approx(50.5)


def test_quantile_ci_ranks_clamped() -> None:
    q = summarize(np.arange(1.0, 11.0), quantiles=(0.99,)).quantiles[0]
    assert q.hi == 10.0


def test_median_ci_coverage() -> None:
    rng = np.random.default_rng(20261027)
    hits = 0
    for _ in range(200):
        q = summarize(rng.random(101), quantiles=(0.5,)).quantiles[0]
        hits += q.lo <= 0.5 <= q.hi
    assert hits / 200 >= 0.9


@pytest.mark.parametrize(
    ("k", "n", "lo", "hi"),
    [(81, 263, 0.2553, 0.3662), (0, 10, 0.0, 0.2775), (10, 10, 0.7225, 1.0)],
)
def test_wilson_matches_newcombe_1998(k: int, n: int, lo: float, hi: float) -> None:
    got = wilson(k, n, conf=0.95)
    assert got[0] == pytest.approx(lo, abs=5e-5)
    assert got[1] == pytest.approx(hi, abs=5e-5)


def test_zero_hits_upper_bound_positive() -> None:
    z = stats.norm.ppf(0.975)
    lo, hi = wilson(0, 1000)
    assert lo == 0.0
    assert hi == pytest.approx(z**2 / (1000 + z**2))
    assert hi > 0


@pytest.mark.parametrize(
    ("target", "expected"),
    [(Target(le=2), 2), (Target(lt=2), 1), (Target(ge=3), 2), (Target(gt=3), 1)],
)
def test_target_probability(target: Target, expected: int) -> None:
    s = summarize(np.array([1.0, 2.0, 3.0, 4.0]), target=target)
    assert s.target is not None
    assert s.target.k == expected
    assert s.target.p == expected / 4
    assert s.target.lo < s.target.p < s.target.hi


def test_bool_output_only_share() -> None:
    s = summarize(np.array([True, False, True, True]))
    assert s.kind == "bool"
    assert s.share is not None
    assert (s.share.k, s.share.n, s.share.p) == (3, 4, 0.75)
    assert s.mean is None
    assert s.quantiles == ()


def test_single_sample() -> None:
    s = summarize(np.array([3.0]))
    assert math.isnan(s.se)
    assert [n.code for n in s.notices] == ["stats.single_sample"]


@pytest.mark.parametrize("q", [0.0, 1.0, -0.1, 1.5])
def test_quantile_range(q: float) -> None:
    with pytest.raises(InputError) as exc:
        summarize(np.array([1.0, 2.0]), quantiles=(q,))
    assert exc.value.issue.code == "stats.quantile_range"


def test_default_quantiles() -> None:
    qs = [e.q for e in summarize(np.linspace(0, 1, 1000)).quantiles]
    assert qs == [0.05, 0.1, 0.5, 0.9, 0.95]
