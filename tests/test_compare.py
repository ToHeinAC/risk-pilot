"""Paired comparison of two scenarios (M3 AK 7)."""

import numpy as np
import pytest

from app.analysis.compare import compare, direction
from app.model.schema import Target
from app.present.compare import better_sentence, compare_rows, d_rows, direction_sentence


def test_direction_from_target_or_better() -> None:
    assert direction(Target(le=30), None) == "lower"
    assert direction(Target(gt=0), None) == "higher"
    assert direction(None, "higher") == "higher"
    assert direction(None, None) is None


def test_known_shift_paired() -> None:
    rng = np.random.default_rng(1)
    a = rng.normal(10, 2, 10_000)
    c = compare(a, a - 1.0, target=Target(le=10))
    mean = c.estimate("mean")
    assert mean.diff == pytest.approx(-1.0)
    assert mean.hi - mean.lo < 1e-9  # paired: no noise in a pure shift
    assert c.better is not None
    assert c.better.p == 1.0
    assert c.ties.p == 0.0
    assert c.estimate("median").diff == pytest.approx(-1.0)
    target = c.estimate("target")
    assert target.b > target.a


def test_ties_and_worse_counted() -> None:
    a = np.array([1.0, 2.0, 3.0, 4.0])
    b = np.array([1.0, 1.0, 4.0, 4.0])
    c = compare(a, b, better="lower", batches=2)
    assert c.better is not None
    assert c.worse is not None
    assert (c.better.k, c.ties.k, c.worse.k) == (1, 2, 1)


def test_no_direction_no_better() -> None:
    c = compare(np.arange(10.0), np.arange(10.0) + 1, batches=2)
    assert c.better is None
    assert c.worse is None


def test_batch_means_interval_covers_true_difference() -> None:
    rng = np.random.default_rng(7)
    hits = 0
    for _ in range(100):
        a = rng.normal(0, 1, 2000)
        b = rng.normal(0.5, 1, 2000)
        median = compare(a, b).estimate("median")
        hits += median.lo <= 0.5 <= median.hi
    assert hits >= 90


def test_bool_outputs_compare_shares() -> None:
    a = np.array([True, False] * 50)
    b = np.array([True, True] * 50)
    c = compare(a, b, batches=10)
    share = c.estimate("share")
    assert (share.a, share.b, share.diff) == (0.5, 1.0, 0.5)
    assert c.better is None


def test_rows_and_sentence() -> None:
    rng = np.random.default_rng(2)
    a = rng.normal(20, 2, 20_000)
    c = compare(a, a - 1.0, target=Target(le=20))
    rows = compare_rows(c, "d")
    assert rows[0][0] == "Mittelwert"
    assert rows[0][3].startswith("-1 d [")
    assert better_sentence(c, "Hauptszenario", "B −3 Tage") == (
        "Im Modell ist „B −3 Tage“ in 100 % der Iterationen besser als „Hauptszenario“ "
        "(100 … 100 %), in 0 % gleich und in 0 % schlechter."
    )


def test_noisy_shift_mean_criterion_and_paired_se() -> None:
    rng = np.random.default_rng(3)
    a = rng.normal(10, 2, 50_000)
    b = a - 1.0 + rng.normal(0, 0.5, a.size)
    mean = compare(a, b, better="lower").estimate("mean")
    se = (mean.hi - mean.lo) / (2 * 1.959964)
    assert se == pytest.approx(0.5 / np.sqrt(a.size), rel=0.05)
    assert abs(mean.diff + 1.0) < 4 * se


def test_better_has_wilson_bounds() -> None:
    from app.analysis.stats import wilson

    rng = np.random.default_rng(4)
    a = rng.normal(0, 1, 1000)
    c = compare(a, a + rng.normal(0, 1, 1000), better="lower")
    assert c.better is not None
    assert (c.better.lo, c.better.hi) == pytest.approx(wilson(c.better.k, 1000))


def test_shares_without_direction() -> None:
    c = compare(np.array([1.0, 2.0, 3.0, 4.0]), np.array([0.0, 2.0, 5.0, 6.0]), batches=2)
    assert (c.lower.k, c.ties.k, c.higher.k) == (1, 1, 2)
    assert direction_sentence(c, "A", "B") == (
        "Im Modell ist „B“ in 25 % der Iterationen kleiner als „A“, "
        "in 25 % gleich und in 50 % größer."
    )


def test_d_rows() -> None:
    c = compare(np.zeros(100), np.arange(100.0), batches=2)
    labels = [r[0] for r in d_rows(c, "d")]
    assert labels == [
        "Mittelwert",
        "Median",
        "P10 (10-%-Quantil)",
        "P90 (90-%-Quantil)",
        "Anteil B = A",
    ]
    assert d_rows(c, "d")[-1][1] == "1 %"
