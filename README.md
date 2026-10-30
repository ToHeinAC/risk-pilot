# claude-dev-schema

A GitHub template for Python projects built with Claude Code. It follows the
[Claude Code best practices](https://code.claude.com/docs/en/best-practices): a short instruction
file with only what Claude can't see in the code, one executable quality gate as the definition of
done, and hooks only for the rules that can't have exceptions. Everything else is left to Claude
Code's defaults.

**How to use it, step by step: [docs/HOWTO.md](docs/HOWTO.md).**

## Risk Pilot

The project built on this template: a local world-model builder with a Monte Carlo core. Models
are YAML files made of six node types (constant, uncertain, event, choice, derived, output);
the engine simulates them with one random stream per node and reports statistics with their
numerical uncertainty. Spec and milestones: [PRD.md](PRD.md); computation core (M1):
[docs/specs/m1-rechenkern.md](docs/specs/m1-rechenkern.md); first app (M2):
[docs/specs/m2-erste-app.md](docs/specs/m2-erste-app.md).

**Start the app** (German UI, NiceGUI, port 8642; set `RISK_PILOT_PORT` to change it):

```
uv run python -m app.web.main
```

Open <http://localhost:8642>. **Stop it** with the power icon top right ("App beenden"): it asks
once, then sends SIGTERM to the app's own process only (no port kill). Ctrl+C in the terminal
works too.

- **Tutorials** (`examples/`): T1 sum of two uniforms, T2 mini schedule, each with its analytic
  solution shown next to the simulation; T3 train connection (two-peaked arrival), T4 portfolio
  of three assets (correlation group, VaR/ES), T5 fusion power plant (piecewise maturity years,
  failure events, horizon 2100). T3–T5 carry illustrative numbers. Read-only; "Als Vorlage
  kopieren" creates your own model in `data/models/`.
- **Dependencies and inputs** (M5, [spec](docs/specs/m5-abhaengigkeiten.md)): correlation groups
  under `correlations:` (Spearman input, Gaussian copula, invalid matrices are rejected, never
  repaired; achieved ρ shown after the run), distributions `piecewise` (quantile pairs) and
  `empirical` (value list, CSV import on the model page), input mode `quantiles` (P10/P50/P90
  for normal, lognormal, gamma, weibull, with the fit's deviation), `horizon` and
  `loss_reference` on outputs.
- **Lernpfad** (`examples/lernpfad/`): eleven short lessons on dependency patterns (series,
  parallel AND/OR, k-out-of-n, event branch, threshold, conditional distribution, multiplicative
  chain, Jensen, common cause, capstone). Each has a prediction, a knob that reruns with the same
  seed and shows before/after, and an analytic check. Numbers are illustrative.
- **Scenarios** (M3, [spec](docs/specs/m3-szenarien.md)): sub-scenarios store only their
  overrides (with a reason) under `scenarios:` in the model YAML and inherit everything else, to
  any depth. Pages "Szenarien" (tree, diff, create, override, duplicate, detach) and "Vergleich"
  (same seed, paired differences B − A with intervals, P(B better than A)). T2 ships with
  "B −3 Tage" and "mit Nacharbeit".
- **Analysis** (M4, [spec](docs/specs/m4-struktur.md)): page "Analyse" per scenario and output.
  Dependency graph (node type as symbol, edge kind as line style, coloured by |Spearman ρ|,
  criticality or missing reason), criticality index and path constellations (decisive path
  through `max`/`min` winners and the chosen `where` branch), tornado (each uncertain input fixed
  at its P10 and P90, same seed), sweep of one literal parameter over k values, Spearman rank
  correlation (descriptive) and a risk matrix per event (p̂ with Wilson, conditional difference
  with Welch interval).
- **Form editor and export** (M6, [spec](docs/specs/m6-formular-export.md)): the model page has
  the tabs "Formular" and "YAML" on one draft. The form edits the model header, every node by
  type (parameter fields come from the distribution family) and shows a preview of each
  uncertain node (density, CDF, mean, median, P5/P95, share outside `bounds`). Form edits patch
  the YAML text in place, so comments and layout stay. "Neues leeres Modell" on the start page.
  The results page exports metrics as CSV, raw samples as Parquet and a standalone HTML report.
- **Self-explaining UI** (M8, [spec](docs/specs/m8-ux-selbsterklaerung.md)): every page starts
  with its purpose and the next step for the current state; every evaluation (results,
  comparison, each analysis tab) explains its question, a reading example from the open model,
  how to read it and its limit, and why it stays empty. Page "Glossar" explains the UI terms
  (also as tooltips). "Rundgang an T2 starten" on the start page guides through open, simulate,
  scenario, comparison and analysis with a banner on every page; progress is read from the
  state. A new uncertain node starts with the range input P10/P50/P90.
- **Canvas** (M9, in progress, [spec](docs/specs/m9-grafischer-editor.md)): the model page
  draws the model on a canvas (Vue Flow) instead of the static graph, also while the draft is
  invalid. Moving a node writes its position to the optional `layout` block of the YAML, which
  changes no number and no hash; "Neu anordnen" lays out every node, a click opens the node card.
- **Reference:** model format and semantics in [docs/model-semantics.md](docs/model-semantics.md),
  statistics and extension points in [docs/statistical-methods.md](docs/statistical-methods.md).
- **Runs** are saved on request to `data/runs/` and reload with the same numbers.
- Data location: `RISK_PILOT_DATA_DIR` (default `data/`, gitignored).

Use the core without the app:

```python
from pathlib import Path
from app.adapters.files import load_model
from app.analysis.stats import summarize
from app.engine.simulate import simulate
from app.model.compile import compile_model

result = simulate(compile_model(load_model(Path("examples/t2_terminplan.yaml"))))
print(summarize(result.samples["ende"]).mean)  # about 26.69 days (Clark: 26.685)
```

Benchmark (30 nodes x 100 000 iterations, target < 5 s): `uv run python scripts/bench_m1.py`.

## Quickstart

1. On GitHub, click **Use this template**, then clone your new repository.
2. `uv sync && uv run pre-commit install`
3. `uv run pre-commit run --all-files` must pass.
4. Set `name` and `description` in `pyproject.toml`, then start `claude` in the repo.

Requirements: [uv](https://docs.astral.sh/uv/), git and Claude Code. uv installs Python itself.

## Layout

```
AGENTS.md            facts and rules for AI coding tools (Claude Code via CLAUDE.md, Codex natively)
CLAUDE.md            imports AGENTS.md
PRD.md               spec template: goals, non-goals, milestones with status and acceptance criteria
docs/HOWTO.md        step-by-step workflow
docs/architecture.md code layers, gate flow, harness design decisions
docs/harness-review.md review state and decision log of /harness-review
src/app/             code (computation core, see docs/specs/m1-rechenkern.md)
examples/            tutorial models T1, T2 and the learning path (YAML + explanations)
scripts/             benchmark, not part of the test suite
tests/               pytest suite (offline) and the docs checks
.claude/settings.json            shared permissions and hooks
.claude/hooks/                   format-on-edit, Stop-gate and review-reminder scripts (tested)
.claude/skills/commit-git/       /commit-git: small commits through the gate, never pushes
.claude/skills/harness-review/   /harness-review: check new best practices, decide changes with you
.claude/agents/reviewer.md       read-only reviewer that checks a diff against PRD.md
.pre-commit-config.yaml          the quality gate
.github/workflows/ci.yml         runs the gate on Python 3.11 and 3.14
```

## Where each rule is enforced

| Rule | Edit hook | Stop hook | Commit | CI |
|---|---|---|---|---|
| Formatting (ruff) | yes | yes | yes | yes |
| Lint, complexity ≤ 10, ≤ 50 statements per function (ruff); types (pyright, strict in `src/`) | | yes | yes | yes |
| Tests, branch coverage ≥ 85 %, suite ≤ 60 s | | yes | yes | yes |
| Doc size limits (AGENTS.md ≤ 100 lines; `ideas/` exempt), no broken local links | | yes | yes | yes |
| No `.env` files, no private keys | | yes | yes | yes |
| Secret scan of staged changes (gitleaks) | | | yes | |

The Stop hook runs only when `.py` files changed. Permission rules add: Claude can't read `.env`,
can't pass `--no-verify`, and asks before `git push`. The numbers live in `pyproject.toml`. Process
rules (tests first, docs in the same change) are in [AGENTS.md](AGENTS.md) and are checked in review.
Details: [docs/architecture.md](docs/architecture.md).

## Skills, agents and add-ons

- `/commit-git` (this repo): small Conventional Commits through the gate. Only you can start it.
- `/harness-review` (this repo): checks Anthropic's latest guidance against the harness and
  decides changes with you. A reminder appears when the last review is over 30 days old.
- `reviewer` agent (this repo): `have the reviewer compare the diff against M1 in PRD.md`.
- Claude Code built-ins: `/code-review`, `/security-review`, `/verify`, `/simplify`, `/init`,
  `/doctor`.
- Plugins and frameworks (superpowers, gsd-core, frontend-design, ui-ux-pro-max, gstack, OpenSpec)
  are not enabled by default. See [HOWTO: Optional add-ons](docs/HOWTO.md#optional-add-ons).

## Credits and license

Apache-2.0, see [LICENSE](LICENSE). Third-party material: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
