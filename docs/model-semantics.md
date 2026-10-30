# Model semantics

Reference for the YAML model format (schema version 1): what each field means, how a model is
evaluated, and how scenarios and correlation groups act on it. The derivations are in the specs
[M1](specs/m1-rechenkern.md), [M3](specs/m3-szenarien.md) and [M5](specs/m5-abhaengigkeiten.md);
where they differ, this document follows the code (`src/app/model/`, `src/app/expr/`,
`src/app/engine/`). Statistics are in [statistical-methods.md](statistical-methods.md).

## File format

```yaml
schema_version: 1
model: t2_terminplan
title: "Mini-Terminplan: Serie und Parallelität"
description: "Pfad 1 (A, dann B) läuft parallel zu Pfad 2 (C)."
illustrative: false
settings: {n: 100000, seed: 20261027}
nodes:
  a: {type: uncertain, dist: normal, mean: 10, sd: 2, unit: d, name: "Vorgang A"}
  ende: {type: output, expr: "max(a + 15, 24)", unit: d, target: {le: 30}}
correlations: {}
scenarios: {}
```

| Field | Type | Default | Meaning |
|---|---|---|---|
| `schema_version` | int | required | Must be `1`; any other value is rejected (`model.schema_version`). |
| `model` | ID | required | Model ID, same rules as node IDs. |
| `title`, `description` | text | none | Display only; they do not change any number. |
| `illustrative` | bool | `false` | Marks didactic numbers; model and results pages say „Illustrative Zahlen“. |
| `settings.n` | int | 10000 | Iterations. A run accepts 1 to 2 000 000 (`sim.n_range`). A text such as `"1e5"` is read as an integer if it is one. |
| `settings.seed` | int ≥ 0 | 0 | Run seed; see [random streams](#evaluation-order-and-random-streams). |
| `nodes` | map ID → node | `{}` | The model; at least one node and at least one `output` (`model.empty`, `model.no_output`). |
| `correlations` | map ID → group | `{}` | Rank correlation groups. |
| `scenarios` | map ID → scenario | `{}` | Sub-scenarios of the main scenario `basis`. |
| `layout` | map ID → `[x, y]` | `{}` | Canvas positions in pixels (M9). Change no number and no hash; nodes without one are laid out automatically; a position of an unknown node is a notice (`layout.unknown_node`). |

General rules:

- Unknown keys are rejected everywhere (typos such as `sdd` fail), except in `uncertain` nodes,
  where extra keys are the distribution parameters and are checked against the family.
- Duplicate YAML keys are rejected with their line (`yaml.duplicate_key`); YAML is read with
  safe-load semantics (no tags, no Python objects).
- **IDs** (model, nodes, scenarios): `^[a-z][a-z0-9_]{0,63}$`; not a Python keyword, not
  `true`/`false`, not an expression function name (`min`, `sum`, …); no scenario may be called
  `basis` (the main scenario). The ID is the node's identity: it names its random stream and is what
  expressions reference. The display name is `name`.
- Validation collects all problems of a model at once. Errors are `Issue`s with a stable code
  (`src/app/errors.py`); hints that do not stop a run are `Notice`s.

## Node types

### Common fields

| Field | Type | Meaning |
|---|---|---|
| `type` | `constant`, `uncertain`, `event`, `choice`, `derived`, `output` | Required. |
| `name` | text | Display name; default is the ID. |
| `unit` | text | Free text, shown with values; not checked or converted. |
| `description` | text | Display only. |
| `why` | text or `{text, links: [..], date}` | Reason or research note. |
| `tags` | list of text | Stored and editable; no effect on any computation. |
| `bounds` | `{min?, max?}` | Plausible range. Values outside produce the notice `range.violation` with the share below and above. **Values are not clipped.** |
| `track` | bool | Keep this node's draws in the result. Outputs are always kept. |

`name`, `description`, `why` and `tags` are excluded from the content hash: relabelling a node
never changes a number.

### Type-specific fields

| Type | Fields | Value per iteration |
|---|---|---|
| `constant` | `value: number` | the number |
| `uncertain` | `dist`, `input` (default `params`), parameters of that mode | float |
| `event` | `p`: number in [0, 1] or expression | bool: occurs iff u < p |
| `choice` | `options: [{label, weight ≥ 0}, …]`, at least 2, labels unique, weight sum > 0 | option code; weights are relative |
| `derived` | `expr` | type of the expression (number, bool, or a choice it passes on) |
| `output` | `expr`, optional `target`, `better`, `horizon`, `loss_reference` | number or bool; never a choice |

**`uncertain` parameters** are given in the input mode named by `input`. Each parameter is
a number, an expression string (`mean: "jahre * 0.06"`), or, for list parameters, a literal
number list (`values: [2028, 2031, 2036]`). A string in a parameter field is always an
expression. The families, their modes and parameters are listed in
[statistical-methods.md](statistical-methods.md#distribution-families). Literal parameters are
checked when the model is compiled (`param.invalid`, `param.missing`, `param.unknown`,
`dist.unknown`, `dist.mode_unknown`). Expression parameters are checked per iteration during the
run; if any iteration violates a rule, the run stops with `runtime.param_invalid` and the share
of affected iterations. Mode `quantiles` accepts literal numbers only.

**`output` fields:**

| Field | Meaning |
|---|---|
| `target` | Exactly one of `le`, `lt`, `ge`, `gt` with a number, e.g. `{le: 30}`. Results report P(target reached). |
| `better` | `lower` or `higher`: direction for scenario comparisons when there is no `target` (a target implies it: `le`/`lt` lower, `ge`/`gt` higher). |
| `horizon` | Values above it count as „nicht im Horizont erreicht“; see [Horizon](#horizon). |
| `loss_reference` | Reference value for losses (loss = reference − value): P(loss), VaR and ES at 95 %. |

## Expressions

Expressions are parsed with `ast.parse(text, mode="eval")`, checked against a whitelist of
syntax nodes, type-checked and compiled into a tree of NumPy operations
(`src/app/expr/parser.py`, `evaluate.py`). **Nothing is passed to `eval`.**

| Allowed | Notes |
|---|---|
| Numbers, `true`, `false` | All numbers are float64. |
| Node IDs | Any node of the model; the value of that node in the same iteration. |
| `+ - * / ** %`, unary `-`, `+` | Booleans count as 0/1 (`5 * nacharbeit`). |
| `< <= > >= == !=` | Chains allowed: `0 < x < 1` means `0 < x and x < 1`. |
| `and`, `or`, `not` | Elementwise; operands must be booleans (`expr.type`). |
| Calls of registered functions | Positional arguments only. |
| `choice == "Label"`, `!=` | The only use of a choice node and the only place for a string; the label must exist (`expr.unknown_label`). |

| Function | Arguments | Semantics |
|---|---|---|
| `min(a, b, …)`, `max(a, b, …)` | ≥ 2 | Elementwise minimum, maximum. |
| `sum(a, …)` | ≥ 1 | Sum. |
| `abs`, `exp`, `log`, `sqrt`, `floor`, `ceil` | 1 | NumPy equivalents; `log` is the natural logarithm. |
| `clip(x, lo, hi)` | 3 | Clamp; `lo > hi` in any iteration stops the run (`runtime.clip_bounds`). |
| `where(c, a, b)` | 3 | `a` where `c` is true, else `b`; `c` must be boolean. Boolean if both branches are. |
| `interp(x, xs, ys)` | 3 | Linear interpolation; `xs`, `ys` literal number lists of equal length ≥ 2, `xs` strictly increasing; constant beyond the ends. |

Forbidden (`expr.forbidden` unless noted): attributes, indexing, `lambda`, comprehensions,
`a if c else b` (use `where`), keyword arguments, `*args`, walrus, f-strings and other strings,
lists outside `interp`, `//`, bit operators, `is`, `in`, calls of anything but a function name,
unknown functions (`expr.unknown_function`), wrong argument counts (`expr.arity`), unknown names
(`expr.unknown_name`, with the closest match as suggestion). Limits: 1000 characters (checked
before parsing, `expr.too_long`), nesting depth 32 (`expr.too_deep`), 500 syntax nodes
(`expr.too_large`).

**Numerics.** Evaluation runs with floating-point warnings switched off; afterwards every node's
result is checked. Any non-finite value stops the run with `runtime.non_finite` and the share of
iterations. So `log(0)` in the branch `where` does not choose is harmless, but a non-finite node
value never passes silently.

## Evaluation order and random streams

- References between nodes form a directed graph. A cycle is rejected (`graph.cycle`, listing
  the nodes in order). Unconnected nodes are allowed.
- Nodes are evaluated in a deterministic topological order, each **exactly once per run**,
  vectorised over all N iterations; every reference reuses that array (`x - x` is 0 everywhere).
- Every random node (`uncertain`, `event`, `choice`) has its own stream:
  `SeedSequence(entropy=seed, spawn_key=(key,))` with `key` = first 8 bytes of SHA-256 of the
  UTF-8 node ID (big-endian), generator PCG64. It draws exactly N uniforms; a draw of exactly 0
  is replaced by 2⁻⁵³, so u lies in (0, 1).
- Values come from **inversion**: `value = ppf(u)` of the node's distribution with its parameters
  in that iteration. Events occur iff u < p; a choice picks option j iff
  cum[j−1] ≤ u < cum[j] of its normalised weights.

Consequences:

- Same model, N, seed and package versions give bit-identical samples.
- Adding a node does not change the draws of any other node. Renaming `name` changes nothing;
  changing an ID changes that node's stream.
- The first n draws of a run with N > n equal a run of length n.
- Between runs with the same seed, a changed parameter moves values monotonically
  (common random numbers): a larger `p` gives a superset of occurrences, a larger mean shifts
  every iteration up. Scenario comparisons and the tornado rely on this.
- Exception: members of a correlation group draw through the copula; changing the group's
  members or matrix changes their draws (not those of other nodes).

## Scenarios

The main scenario `basis` is the model's own `nodes`. Sub-scenarios store only their changes.

```yaml
scenarios:
  b_schneller:
    name: "B −3 Tage"
    why: "Ein zweites Team verkürzt Vorgang B."
    overrides:
      b: {mean: 12, why: "Planwert mit zweitem Team"}
  beides:
    name: "hohe Förderung und Materialproblem"
    why: "Beide Annahmen zusammen."
    parent: foerderung
    overrides:
      f_material: {p: 0.4}
```

| Field | Meaning |
|---|---|
| `name` | Display name (required). |
| `why` | Reason (required, non-empty). |
| `parent` | Parent scenario ID, default `basis`. Chains of any depth. |
| `overrides` | Node ID → fields to replace, plus optional `why` (reason of that override) and `inactive: true`. |
| `correlations` | Group ID → `{spearman, why?}`: replaces the matrix of an existing group. |
| `nodes`, `detached_from` | Set by „Loslösen“ (see below). |

- **Inheritance:** the effective model applies the overrides from the root down to the scenario;
  fields not overridden come from the parent, so later changes to a parent reach its children.
- **Allowed fields** per node type: `constant` `value`, `bounds`; `event` `p`, `bounds`;
  `choice` `options`; `derived` `expr`, `bounds`; `output` `expr`, `target`, `better`, `bounds`,
  `horizon`, `loss_reference`; `uncertain` `dist`, `input`, its parameters, `bounds`. Labels
  (`name`, `unit`, `description`, `tags`, `track`) cannot be overridden
  (`scenario.field_invalid`); `type` neither (`scenario.type_change`).
- **Change of family:** if an override sets `dist` or `input`, all old parameters are dropped and
  the override must give the complete parameter set (`input` falls back to `params`).
- Scenarios cannot add or remove nodes. To switch a branch off, put a `constant` in the main
  model and use it in a `where`.
- **Checks:** unknown parent (`scenario.parent_unknown`), parent cycle (`scenario.parent_cycle`),
  override of a missing node (`scenario.node_unknown`), unknown correlation group or field
  (`scenario.corr_unknown`, `scenario.corr_field`). Every scenario is also compiled as a full
  model, so errors such as a cycle through a changed `expr` name the scenario.
- **Hints:** an override equal to the parent's value gives `scenario.same_value`; an override
  marked `inactive: true` on a deleted node is kept visible but not applied
  (`scenario.inactive`). Nothing is removed silently.
- **Detach („Loslösen“):** the scenario's effective nodes (and correlation matrices) are frozen
  into `nodes:`, `detached_from:` records the former parent. Later parent changes no longer
  apply; the scenario stays in the model and in comparisons.
- **Common random numbers:** streams depend only on seed and node ID, so with the same seed nodes
  not overridden are bit-identical across scenarios and overridden ones are coupled by inversion.

## Correlation groups

```yaml
correlations:
  markt:
    nodes: [l_aktien, l_anleihen, l_gold]
    spearman:
      - [1.0, 0.2, 0.1]
      - [0.2, 1.0, 0.3]
      - [0.1, 0.3, 1.0]
    why: "Grobe Erfahrungswerte (illustrativ)"
```

- Input is the target **Spearman rank correlation** matrix, in the order of `nodes`. Sampling uses
  a Gaussian copula ([statistical-methods.md](statistical-methods.md#gaussian-copula)); each
  run reports the achieved matrix.
- Members: `uncertain` and `event` nodes only; at least two; each node at most once in a group
  and in at most one group. In a group an event occurs when its correlated uniform exceeds
  1 − p, so ρ > 0 couples occurrence with high values of the other members.
- Matrix checks, in this order: k × k (`corr.shape`), diagonal exactly 1 (`corr.diagonal`),
  entries in [−1, 1] (`corr.range`), exactly symmetric (`corr.asymmetric`, names the first
  cell), positive semidefinite (`corr.not_psd`), and positive semidefinite after the conversion
  to the latent normal correlation (`corr.latent_not_psd`); eigenvalue tolerance −1e−10, so
  singular matrices (ρ = 1) are allowed.
- **A matrix that fails is rejected, never repaired** (no nearest-correlation projection): the
  message names the smallest eigenvalue and the user adjusts the numbers.
- Discrete members (events, discrete families) produce ties; the hint `corr.discrete_ties` says
  the achieved rank correlation will fall short of the target.
- A scenario can replace a group's `spearman` (and `why`); its members stay fixed.

## Horizon

`horizon` on an output marks values above it as „nicht im Horizont erreicht“ (for example
„Fusionskraftwerk nicht bis 2100“ in T5, where failure is encoded as 2200). The results show the
share beyond the horizon with its Wilson interval; quantiles, median, min and max beyond it are
shown as „> Horizont“; mean and standard deviation are not shown as numbers while any value lies
beyond („nicht bestimmbar: x % jenseits des Horizonts“). P(target) is unaffected. Comparison and
analysis pages use the raw values.

## Canvas and layout

The canvas on the model page (M9) is a view with editing, not a second model. Its edges are
derived exactly like the dependency graph: a reference in `expr` (expression), in a distribution
parameter or `p` (parameter), and every pair of a correlation group (correlation). Connecting two
nodes writes a preset expression (`a + b`, `max(a, b)`, `min(a, b)`, `a * b`,
`… + where(e, x, 0)`, a parameter `a` or `a * f`, `p: a`) or a correlation entry; deleting an
edge removes one argument of such an expression. A free expression is never rewritten: the
canvas opens it instead. Positions live in `layout` (see the file format above) and are shared
by all scenarios; a scenario changes values only, never the structure.

## Validation behaviour

- **No silent repair.** Invalid input is rejected with a code, node, field and parameters; it is
  never clipped, renormalised or projected. Choice and discrete weights are relative by
  definition, not repaired.
- `bounds` are a check, not a constraint: the run continues, values are unchanged, and the
  notice reports the share below `min` and above `max`.
- Other notices: quantile fit quality (`fit.deviation`, `fit.conflict`), `uniform` with
  `low = high` evaluated as a constant (`uniform.degenerate`), discrete ties in a group.
- Where texts live: codes and their parameters in `src/app/errors.py`, German message templates
  in `src/app/messages.py` (`CATALOG`, rendered by `render()`; UI texts in `UI` via `t()`).
