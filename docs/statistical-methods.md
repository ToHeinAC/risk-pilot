# Statistical methods

Reference for how Risk Pilot draws samples, which statistics it reports with which uncertainty,
how the structure analyses are defined, and how to extend the families and functions. Model
format and evaluation order: [model-semantics.md](model-semantics.md). Derivations: specs
[M1](specs/m1-rechenkern.md), [M3](specs/m3-szenarien.md), [M4](specs/m4-struktur.md),
[M5](specs/m5-abhaengigkeiten.md); where they differ, this document follows the code.

All numbers are estimates from N iterations. Every reported statistic carries its numerical
uncertainty (standard error or interval); the default confidence level is 95 %.

## Sampling

**Inversion.** Each random node turns its own uniforms u ∈ (0, 1) into values with the inverse
CDF of its distribution (`Family.ppf`). Inversion is mandatory for every family: with the same
u, a changed parameter moves each value monotonically, which gives scenario comparisons and the
tornado their common random numbers. Streams are described in
[model-semantics.md](model-semantics.md#evaluation-order-and-random-streams).

### Distribution families

Built-in families (`src/app/dists/families.py`); `input` selects the mode, `params` is the
default. Defaults in parentheses.

| `dist` | Kind | Modes and parameters |
|---|---|---|
| `uniform` | cont. | `params`: low, high (low ≤ high; low = high gives a constant and a notice) |
| `triangular` | cont. | `params` = `three_point`: low, mode, high |
| `pert` | cont. | `params` = `three_point`: low, mode, high, lambda (4); Beta with α = 1 + λ(mode − low)/(high − low), β = 1 + λ(high − mode)/(high − low) |
| `normal` | cont. | `params` = `mean_sd`: mean, sd; `quantiles`: p10, p50, p90 |
| `truncnormal` | cont. | `params`: mean, sd, lower (−∞), upper (+∞); mean and sd of the *untruncated* normal; one bound finite, mass ≥ 1e−9 |
| `lognormal` | cont. | `params`: mu, sigma (log scale); `mean_sd`: mean, sd (σ² = ln(1 + sd²/mean²), μ = ln mean − σ²/2); `quantiles` |
| `beta` | cont. | `params`: alpha, beta, low (0), high (1); `mean_sd`: mean, sd, low (0), high (1) |
| `student_t` | cont. | `params`: df (> 2), loc, scale |
| `exponential` | cont. | `params`: rate; `mean`: mean |
| `gamma` | cont. | `params`: shape, scale; `mean_sd` (shape = mean²/sd², scale = sd²/mean); `quantiles` |
| `weibull` | cont. | `params`: shape, scale, loc (0); `quantiles` (loc = 0) |
| `bernoulli` | discr. | `params`: p; values 0.0 / 1.0 |
| `discrete` | discr. | `params`: values [list], weights [list, relative], in list order |
| `poisson` | discr. | `params`: rate (≥ 0) |
| `piecewise` | cont. | `params`: probs [list, from 0 to 1, strictly increasing], values [list, strictly increasing]; CDF linear between the pairs |
| `empirical` | discr. | `params`: values [list]; each value with probability 1/n, drawn with replacement |

Literal parameters are checked when compiling; expression parameters per iteration during the
run. The canonical parameters of literal distributions are stored with each run.

### Gaussian copula

Correlation groups take a target Spearman matrix ρ_s. The members' uniforms are coupled as
follows (`src/app/engine/copula.py`, `src/app/model/correlations.py`):

1. Latent normal correlation **ρ_latent = 2 sin(π ρ_s / 6)** (exact relation between Spearman and
   Pearson correlation for bivariate normals).
2. Factor F with F Fᵀ = latent matrix: Cholesky; for singular, semidefinite matrices the
   symmetric root V Λ^½ from the eigendecomposition.
3. Per member z = Φ⁻¹(u) from its *own* stream; z' = F z; u' = Φ(z'), kept inside (0, 1). The
   member then draws `ppf(u')` (events: occurs iff u' > 1 − p).

Nodes outside groups keep their streams untouched, and members keep the same streams across
scenarios, so common random numbers still hold. Every run reports the **achieved** Spearman
matrix (rank correlation of the members' final values); the results page shows target and
achieved ρ per pair. Discrete members tie, so their achieved ρ falls short of the target
(notice `corr.discrete_ties`).

### Quantile fit

Mode `quantiles` (normal, lognormal, gamma, weibull) takes literal **P10, P50, P90**, strictly
increasing (and > 0 except for normal). `src/app/dists/fit.py` finds the family's parameters by
least squares: normal by linear regression of the quantiles on z = Φ⁻¹(p); lognormal the same on
log q; gamma and weibull by `scipy.optimize.least_squares` on log-parameters from a fixed start
(deterministic), residuals divided by P90 − P10.

- **Deviation** = max |fitted − given| / (P90 − P10), relative to the spread so that years
  (2040) and small numbers are judged alike.
- Always reported: notice `fit.deviation` with the three given and fitted quantiles. Above
  **2 %** the notice is `fit.conflict`: the three values do not fit that family.
- **Alternative:** „als Stützstellen übernehmen“ replaces the node by `piecewise` with
  probs [0, 0.1, 0.5, 0.9, 1] and values [P0, P10, P50, P90, P100]. P0 < P10 and P100 > P90
  must be entered by the user (`fit.bounds`); no bounds are invented.

## Summary statistics

`src/app/analysis/stats.py::summarize`, per output:

| Statistic | Method and uncertainty |
|---|---|
| Mean | sample mean ± standard error SE = s/√N (s with ddof = 1); N = 1 gives no SE (`stats.single_sample`) |
| SD, variance | ddof = 1 |
| Quantiles P5, P10, P50, P90, P95 | Hyndman–Fan type 7 (`np.quantile`, linear); distribution-free CI from order statistics: ranks l = Bin⁻¹((1−c)/2; N, q), u = Bin⁻¹(1−(1−c)/2; N, q) + 1, clipped to [1, N], interval (x₍l₎, x₍u₎) |
| P(target), shares, boolean outputs | k/N with the **Wilson** interval: centre (p̂ + z²/2N)/(1 + z²/N), half-width z/(1 + z²/N)·√(p̂(1−p̂)/N + z²/4N²); lower bound 0 at k = 0, upper 1 at k = N, so k = 0 still gives an upper bound > 0 |
| Min, max | sample extremes |

The results page also states the relative precision SE/|mean| and warns when the half-width of
P(target) exceeds 1 percentage point.

**Censoring at the horizon.** With `horizon`, the share P(X > horizon) gets a Wilson interval.
Quantiles and interval bounds above the horizon are shown as „> Horizont“; mean and SD are not
shown while any value is beyond (they would be biased); P(target) stays valid.

**VaR and ES at 95 %** (with `loss_reference` R; loss = R − X):

- P(loss) = P(X < R), Wilson.
- VaR₉₅ = R − Q₀.₀₅, interval from the order-statistic CI of Q₀.₀₅ (bounds swapped).
- ES₉₅ = R − mean of the values ≤ Q₀.₀₅, with SE = s_tail/√n_tail.

**Multimodality.** Histogram with 60 equal bins, smoothed by a 3-bin moving average. A peak is an
interior bin higher than its left and not lower than its right neighbour, at least 10 % of the
highest; two neighbouring peaks are separate if the density between them drops below half of
the smaller one. With two or more separate peaks the page says that median and the most frequent
range (centre of the highest bin) differ and the mean describes no typical case. With a horizon
only values within it count, and the hint is dropped if the median lies beyond.

## Comparison of scenarios

`src/app/analysis/compare.py`. Scenarios A (reference) and B run with the same N and seed, so
nodes share their streams (**common random numbers**) and the comparison is paired per
iteration: d = b − a.

| Quantity | Method |
|---|---|
| Mean difference | mean(d) ± z·s_d/√N (paired, hence narrow) |
| Median, P10, P90, P(target) differences; boolean shares | point value from A and B; uncertainty by **batch means**: 20 equal blocks, difference per block, SE = s/√20, interval with t(19) |
| P(B better), ties, P(B worse) | shares of d < 0, d = 0, d > 0 with Wilson; „better“ from `target` or `better`, otherwise both shares without a verdict |

Welch's interval is not used here (the samples are paired); it is used in the risk matrix.

## Structure analyses

All on one scenario and one output; runs use `keep="all"` to hold every node's array.

**Criticality** (`criticality.py`, `expr/activity.py`). Per iteration, a reference is *active*
in an expression if it decides the result: `max`/`min` only the winners (ties: all winners);
`where` only the chosen branch, not the condition; everything else all operands; parameters of
random nodes fully. Masks run backwards in reverse topological order from the output (all
iterations) and are OR-ed over successors. The **criticality index** of an `uncertain`, `event`
or `derived` node is the share of iterations on the decisive path, with Wilson; indices need not
sum to 1. A **path constellation** is the set of critical `uncertain`/`event` inputs of one
iteration; their shares sum to 1 (most frequent first, from rank 10 on collected in one row).
Without `max`, `min` or `where` every connected input is always critical and the page says the
index carries no information.

**Tornado** (`tornado.py`). For every `uncertain` node: P10 and P90 of its simulated marginal
(discrete families with `inverted_cdf`, so real support values); two runs with that node fixed
as a constant, same seed, default N = 20 000. Swing = metric(P90) − metric(P10) of the output
mean (default), median or P(target), sorted by |swing|. Common random numbers make the swing of
a node without a path to the output exactly 0. The page warns above 50 runs.

**Sweep** (`sweep.py`). One literal number (`value`, `p`, or a distribution parameter) over k
values (default 9, evenly spaced), same N and seed. Invalid values are reported before any run.
Per value: mean ± SE, median and a chosen quantile with order-statistic CI, P(target) with Wilson.

**Rank correlation** (`sensitivity.py`). Spearman ρ (average ranks) of each `uncertain` and
`event` node with the output from one run; interval by Fisher z with SE 1.03/√(N − 3);
undefined if one side is constant. **Descriptive only**: it shows co-movement in the model, not
a cause and not an effect size.

**Risk matrix** (`riskmatrix.py`). Per event: x = p̂ with Wilson; y = E[Y | event] −
E[Y | no event] with a **Welch** interval (Welch–Satterthwaite df). y is undefined if either
group has fewer than two iterations. The difference is no causal effect when events share causes
or interact.

## Acceptance tolerances used in tests

Defined in PRD §3, used throughout `tests/` (`analysis/analytic.py` provides the helpers):

| Criterion | Rule |
|---|---|
| KS (DKW) | sup-distance between empirical and reference CDF < ε = √(ln(2/α)/(2N)), α = 0.001 (`ks_distance`, `dkw_epsilon`; ε ≈ 0.0062 at N = 100 000) |
| Mean | \|estimate − reference\| < 4 SE |
| Proportion | reference value inside the Wilson interval at 99.9 % |

Specific checks add their own tolerances, e.g. achieved Spearman within ±0.02 of the target at
N = 100 000, T4 standard deviation within ±3 %, tornado swings of T1 equal within ±2 %.

## Extension points

### Adding a distribution family

A family is any object satisfying the `Family` protocol (`src/app/dists/base.py`); no base class
is needed. Register it with `register()` from `src/app/dists/registry.py`.

| Member | Contract |
|---|---|
| `name` | Key used in YAML `dist:` |
| `kind` | `"continuous"` or `"discrete"` (discrete: tornado uses real support values; ties hint in groups) |
| `modes` | Mode name → tuple of `ParamSpec(name, default=None, is_list=False)`; `default=None` means required, `is_list` a literal number list |
| `check(mode, p)` | Rules on the *input* parameters as `Violation(field, rule, mask)` (build with `violation()`); mask True = violated; write rules as positive comparisons so NaN never counts |
| `to_canonical(mode, p)` | Input parameters → canonical parameters, elementwise on arrays |
| `ppf(u, c)` | Inverse CDF, vectorised over u and parameter arrays |
| `reference(c)` | Frozen SciPy distribution for tests (`cdf`, `mean`, `std`) |

Worked example, abridged from `tests/test_family_extension.py` (the test registers it through a
fixture, so it is removed again afterwards):

```python
class Logistic:
    name = "test_logistik"
    kind: Literal["continuous"] = "continuous"
    modes: ClassVar[Mapping[str, tuple[ParamSpec, ...]]] = {
        "params": (ParamSpec("loc"), ParamSpec("scale"))
    }
    def to_canonical(self, mode, p): return {k: np.asarray(v, dtype=np.float64) for k, v in p.items()}
    def check(self, mode, p): return [violation("scale", "scale > 0", p["scale"] <= 0)]
    def ppf(self, u, c): return np.asarray(c["loc"] + c["scale"] * np.log(u / (1 - u)))
    def reference(self, c): return stats.logistic(loc=c["loc"], scale=c["scale"])

register(Logistic())
```

The test shows that, with no other code changed, a model with `dist: test_logistik` compiles,
simulates and passes the KS criterion, and that the form editor offers the family with exactly
its parameter fields (built from `ParamSpec`) and the distribution preview works. Validation
messages, expression parameters, correlation groups and scenarios work through the same
protocol. Add a KS (or frequency) test for every new family.

### Adding an expression function

Register an `ExprFunction(name, min_args, max_args, impl)` with `register_function()` in
`src/app/expr/functions.py` (`max_args=None` for unlimited). `impl` receives float64 arrays and
returns an array; raise `EvalError(code, share)` for runtime failures and add that code. The
function name becomes a reserved ID. Functions that need special typing or criticality rules
(like `where`, `interp`, `min`, `max`) need their own handler in `parser.py`, a node class in
`evaluate.py` and a rule in `activity.py`.

### Texts and issue codes

Issue and notice codes with their parameter names are listed in `CODES` in `src/app/errors.py`;
error objects carry codes and parameters only, never text. German templates are in
`src/app/messages.py`: `CATALOG` (rendered by `render()`) for issues and notices, `UI` (via
`t()`) for page texts. Tests check that every code has a template and every used UI key exists.

### Adding a node type

Not a plug-in point: node types are a closed union. A new type touches `model/schema.py` (class
and `Node` union), `model/compile.py` (compiled body and value type), `engine/simulate.py`
(evaluation), `model/graph.py` (expression fields), `model/scenarios.py` (overridable fields),
`model/correlations.py` if it may join groups, the analyses in `analysis/` that filter by type,
`model/form.py` and `ui/form.py` (form fields and type list), `present/structure.py` (graph
symbol) and other `present/` texts, and `errors.py`/`messages.py`.
