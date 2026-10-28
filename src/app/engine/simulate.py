"""Vectorised Monte Carlo simulation of a compiled model."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false

import platform
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.metadata import version
from typing import Any, Literal

import numpy as np
import scipy
from numpy.typing import NDArray

from app.engine.streams import GENERATOR, STREAM_DERIVATION, uniforms
from app.errors import Issue, Notice, SimulationError
from app.expr.evaluate import EvalError
from app.model.compile import CChoice, CConstant, CEvent, CExpr, CNode, CompiledModel, CUncertain

N_MAX = 2_000_000
Array = NDArray[Any]


@dataclass(frozen=True)
class SimulationResult:
    samples: Mapping[str, Array]
    meta: Mapping[str, object]
    canonical: Mapping[str, Mapping[str, object]]
    warnings: tuple[Notice, ...]


@dataclass(frozen=True)
class _Run:
    values: dict[str, Array]
    n: int
    seed: int

    def full(self, x: Array) -> Array:
        """Broadcast a (possibly scalar) result to one value per iteration."""
        dtype = np.bool_ if x.dtype == np.bool_ else np.float64
        return np.array(np.broadcast_to(x, (self.n,)), dtype=dtype)

    def evaluate(self, node: CNode) -> Array:
        body = node.body
        if isinstance(body, CConstant):
            return np.full(self.n, body.value)
        if isinstance(body, CExpr):
            return self.full(body.expr.evaluate(self.values))
        u = uniforms(self.seed, node.id, self.n)
        if isinstance(body, CChoice):
            return np.searchsorted(body.cum, u, side="right").astype(np.float64)
        if isinstance(body, CEvent):
            return self.event(node.id, body, u)
        return self.uncertain(node.id, body, u)

    def event(self, node_id: str, body: CEvent, u: NDArray[np.float64]) -> Array:
        p = np.asarray(body.p.evaluate(self.values), dtype=np.float64)
        if not body.literal:
            self.check(node_id, "p", "0 ≤ p ≤ 1", (p < 0) | (p > 1))
        return self.full(u < p)

    def uncertain(self, node_id: str, body: CUncertain, u: NDArray[np.float64]) -> Array:
        params = {
            k: np.asarray(e.evaluate(self.values), dtype=np.float64) for k, e in body.params.items()
        }
        family = body.family
        if not body.literal:
            with np.errstate(all="ignore"):
                violations = family.check(body.mode, params)
            for v in violations:
                self.check(node_id, v.field, v.rule, v.mask)
        with np.errstate(all="ignore"):
            return self.full(family.ppf(u, family.to_canonical(body.mode, params)))

    def check(self, node_id: str, field: str, rule: str, mask: Array) -> None:
        bad = np.broadcast_to(mask, (self.n,))
        if bad.any():
            share = float(bad.mean())
            raise SimulationError(
                Issue("runtime.param_invalid", node_id, field, params={"rule": rule}, share=share)
            )


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _finite(node_id: str, x: Array) -> None:
    if x.dtype == np.bool_:
        return
    bad = ~np.isfinite(x)
    if bad.any():
        raise SimulationError(Issue("runtime.non_finite", node_id, share=float(bad.mean())))


def _bounds_notice(node: CNode, x: Array) -> Notice | None:
    if node.bounds is None or x.dtype == np.bool_:
        return None
    lo, hi = node.bounds.min, node.bounds.max
    below = float(np.mean(x < lo)) if lo is not None else 0.0
    above = float(np.mean(x > hi)) if hi is not None else 0.0
    if below == 0.0 and above == 0.0:
        return None
    return Notice("range.violation", node.id, below + above, {"below": below, "above": above})


def _meta(compiled: CompiledModel, n: int, seed: int) -> dict[str, object]:
    return {
        "model_id": compiled.model.model,
        "model_hash": compiled.model_hash,
        "schema_version": compiled.model.schema_version,
        "n": n,
        "seed": seed,
        "generator": GENERATOR,
        "stream_derivation": STREAM_DERIVATION,
        "risk_pilot": version("risk-pilot"),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "python": platform.python_version(),
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
    }


def simulate(
    compiled: CompiledModel,
    n: int | None = None,
    seed: int | None = None,
    keep: Literal["outputs", "all"] = "outputs",
) -> SimulationResult:
    """Evaluate every node once per iteration, in dependency order.

    ``keep="all"`` returns every node's array (for the structure analyses), not only the
    tracked ones; memory grows with N times the number of nodes.
    """
    n = compiled.model.settings.n if n is None else n
    seed = compiled.model.settings.seed if seed is None else seed
    if not _is_int(n) or not 1 <= n <= N_MAX:
        raise SimulationError(Issue("sim.n_range", params={"n": n}))
    if not _is_int(seed) or seed < 0:
        raise SimulationError(Issue("sim.seed_range", params={"seed": seed}))
    run = _Run({}, n, seed)
    pending = Counter(ref for refs in compiled.refs.values() for ref in refs)
    samples: dict[str, Array] = {}
    notices = list(compiled.notices)
    for node_id in compiled.order:
        node = compiled.nodes[node_id]
        try:
            x = run.evaluate(node)
        except EvalError as exc:
            raise SimulationError(Issue(exc.code, node_id, share=exc.share)) from exc
        _finite(node_id, x)
        notice = _bounds_notice(node, x)
        if notice is not None:
            notices.append(notice)
        run.values[node_id] = x
        if node.tracked or keep == "all":
            samples[node_id] = x
        _release(run.values, compiled.refs[node_id], pending, samples)
    return SimulationResult(samples, _meta(compiled, n, seed), compiled.canonical, tuple(notices))


def _release(
    values: dict[str, Array], refs: frozenset[str], pending: Counter[str], keep: Mapping[str, Array]
) -> None:
    """Drop arrays nobody needs any more, so large models stay within memory."""
    for ref in refs:
        pending[ref] -= 1
        if pending[ref] == 0 and ref not in keep:
            del values[ref]
