"""M1 benchmark: 30 nodes x 100 000 iterations (PRD target < 5 s). Not part of the test suite.

Run: uv run python scripts/bench_m1.py
"""

import time

from app.engine.simulate import simulate
from app.model.compile import compile_model
from app.model.yaml_io import model_from_yaml

# Mix of fast and slow inversions (beta, student_t, gamma are the slowest), plus expressions.
NODES = [
    *(f"  n{i}: {{type: uncertain, dist: normal, mean: 10, sd: 2}}" for i in range(4)),
    *(f"  b{i}: {{type: uncertain, dist: beta, alpha: 2, beta: 5}}" for i in range(4)),
    *(f"  t{i}: {{type: uncertain, dist: student_t, df: 4, loc: 0, scale: 1}}" for i in range(4)),
    *(f"  g{i}: {{type: uncertain, dist: gamma, shape: 2.5, scale: 3}}" for i in range(4)),
    *(f"  p{i}: {{type: uncertain, dist: pert, low: 1, mode: 2, high: 5}}" for i in range(4)),
    "  e0: {type: event, p: 0.2}",
    "  s0: {type: derived, expr: 'n0 + n1 + b0 * 10'}",
    "  s1: {type: derived, expr: 'max(s0, n2 + n3)'}",
    "  s2: {type: derived, expr: 'where(e0, s1 + 5, s1)'}",
    "  s3: {type: derived, expr: 'g0 + g1 + g2 + g3'}",
    "  s4: {type: derived, expr: 'p0 + p1 + p2 + p3 + t0'}",
    "  s5: {type: derived, expr: 'b1 + b2 + b3 + t1 + t2 + t3'}",
    "  s6: {type: derived, expr: 'interp(s3, [0, 20, 40], [0, 1, 1.5])'}",
    "  s7: {type: derived, expr: 's2 + s4 + s5 + s6'}",
    "  y: {type: output, expr: 's7 * 1.1', target: {le: 80}}",
]
TEXT = "schema_version: 1\nmodel: bench\nnodes:\n" + "\n".join(NODES) + "\n"


def main() -> None:
    compiled = compile_model(model_from_yaml(TEXT))
    assert len(compiled.nodes) == 30
    simulate(compiled, n=1000)  # warm-up
    times = []
    for _ in range(3):
        start = time.perf_counter()
        simulate(compiled, n=100_000, seed=1)
        times.append(time.perf_counter() - start)
    print(f"30 nodes x 100 000 iterations: best {min(times):.2f} s, worst {max(times):.2f} s")


if __name__ == "__main__":
    main()
