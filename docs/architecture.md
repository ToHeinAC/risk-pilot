# Architecture

## Code layers

| Layer | Where | Rule |
|---|---|---|
| Core logic | `src/app/` except `adapters/` and `ui/` | Pure functions, fully typed, no I/O. Unit-tested directly. |
| Adapters | `src/app/adapters/` | The only place for file and process I/O: model files, CSV columns, runs, settings, shutdown. |
| Entry point | `src/app/ui/` (Streamlit) | Thin: read widgets, call core and adapters, render. Tested with AppTest. |

Core packages (M1, [spec](specs/m1-rechenkern.md)):

| Package | Role |
|---|---|
| `errors.py`, `messages.py` | Issue/Notice with stable codes and parameters; German message catalogue, `render()` |
| `model/` | Pydantic schema, YAML text <-> model, reference graph and typed edges (`graph.edges`, M4), `compile_model`; `scenarios.py` (M3): chain, effective model, validation, diff, editing; M5: `correlations.py` (group checks, Spearman -> latent, matrix factor), `edits.py` (quantiles -> piecewise, CSV values -> empirical) |
| `expr/` | Expression language: AST whitelist, static types, vectorised evaluation, function registry; `activity.py` (M4): which references decide a result per iteration |
| `dists/` | Distribution families (inversion sampling), registry; M5: `piecewise`, `empirical`, input mode `quantiles` with `fit.py` (least squares, deviation relative to P90 − P10) |
| `engine/` | One random stream per node, `simulate` (`keep="all"` holds every node's array for the M4 analyses); `copula.py` (M5): correlated uniforms from the members' own streams, achieved ρ |
| `analysis/` | Summary statistics with intervals (M5: horizon, VaR/ES, multimodality), analytic references for T1–T4; `compare.py` (M3): paired differences, batch means, P(B better); M4 ([spec](specs/m4-struktur.md)): `criticality.py` (decisive path, index, constellations), `tornado.py`, `sweep.py`, `sensitivity.py` (Spearman), `riskmatrix.py` (Wilson, Welch) |
| `present/` (M2) | German texts in model language, plotly figures, T1/T2 overlays, editor validation (incl. scenarios), before/after rows, comparison texts, structure figures and tables (M4, graph layout via NetworkX); no Streamlit import |
| `lessons/` (M2) | Learning path: manifest schema, knob (`with_value`), analytic checks per lesson, reading list |

Dependency direction: `ui` -> `present`, `lessons`, `adapters` -> `analysis`, `engine` -> `model`
-> `expr`, `dists` -> `errors`.

UI notes: every page calls `views.sidebar_exit()` itself, because AppTest re-renders only the page
after a widget interaction under `st.navigation`. All visible texts come from `messages.UI` via
`t()`; `tests/test_messages_ui.py` checks that every key used in the code exists. Numeric
modules switch off pyright's `reportUnknownMemberType` per file, because the NumPy stubs mark
`ArrayLike` as partially unknown under `pythonVersion = 3.11`.

## Quality gate flow

```
Claude edits a .py file  -> PostToolUse hook: ruff format (that file only)
Claude stops             -> Stop hook: if .py files changed, run the gate; exit 2 = keep working
git commit               -> pre-commit: the gate on staged files
push / pull request      -> CI: uv sync --locked, then the gate on all files (Python 3.11 and 3.14)
```

The gate itself is defined once, in `.pre-commit-config.yaml`; its numbers live in `pyproject.toml`.
The Stop hook and CI only call it.

## Harness design

The harness follows the [Claude Code best practices](https://code.claude.com/docs/en/best-practices):
tell Claude what it can't see, give it a check to run, enforce only the rules that can't have
exceptions. Every component encodes an assumption about what the model can't do on its own, so
each one has to keep earning its place.

| Component | Kind | Why it exists |
|---|---|---|
| `AGENTS.md` (via `CLAUDE.md`) | guidance, loaded every session | Commands, conventions and gotchas not visible in the code. Capped at 100 lines by `tests/test_docs.py`. |
| `PRD.md` | spec, read on demand | Definition of done for larger work; the reviewer checks against it. |
| Edit hook, Stop hook | enforced | Formatting and a passing gate must hold every time. |
| Deny rules | enforced | `.env` stays unread; `--no-verify` can't skip the gate. `git push` asks. |
| `/commit-git` skill | user-invoked procedure | Commit policy with side effects; Claude can't start it on its own. |
| `/harness-review` skill, reminder hook | user-invoked procedure; SessionStart hook shows a user message | Keeps the harness aligned with new guidance; decisions logged in [harness-review.md](harness-review.md). |
| `reviewer` agent | read-only subagent | Independent spec review that can't edit (`tools: Read, Grep, Glob`). |
| pre-commit, CI | enforced | The same checks, independent of Claude's own report. |

Removed when the harness was aligned with the best practices for Opus 5.5:

- **Generic coding guidelines in AGENTS.md** ("think before coding", "simplicity first"). Current
  models already behave this way; the lines cost attention in every session.
- **IMPLEMENTATION.md with a module map.** Claude reads the layout itself. Milestone status moved
  into `PRD.md`, run/verify commands into `AGENTS.md`.
- **`/documentation-update` command.** Updating affected docs is part of the definition of done in
  `AGENTS.md`; a separate procedure added no knowledge Claude lacks.
- **Custom AST test for function length.** Replaced by ruff `PLR0915` (≤ 50 statements per function).
- **Project-wide plugins** (superpowers, gsd-core, frontend-design, ui-ux-pro-max). Their workflows
  duplicate built-ins (plan mode, `/code-review`, subagents) and their skill descriptions load into
  every session of every user. They remain available as personal opt-ins
  ([HOWTO](HOWTO.md#optional-add-ons)).

## Design decisions

- **One gate definition.** The pre-commit config is the only list of checks, so the Stop hook,
  commits and CI can't drift apart.
- **Tool versions come from `uv.lock`.** The local pre-commit hooks use `language: unsupported`
  (the new name for `system`) and call `uv run <tool>`, so ruff, pyright and pytest aren't pinned
  a second time.
- **The edit hook formats but never lint-fixes.** `ruff check --fix` would delete an import that
  Claude adds one edit before its first use.
- **The Stop hook is cheap and sends Claude back at most once.** It only runs when `.py` files
  changed, and the `stop_hook_active` guard stops a gate failure Claude can't fix from burning
  tokens up to Claude Code's own block cap.
- **Coverage runs only in the gate** (`pytest --cov`), not in `addopts`, so running a single test
  file never fails on the threshold.

## Known limits

- `pre-commit run --all-files` checks only files git tracks. New untracked files are formatted by
  the edit hook, and pyright and pytest cover the whole project; ruff lint reaches them at commit.
- gitleaks scans staged changes, so it protects commits; CI doesn't rescan history. Contributors
  must run `uv run pre-commit install`.
- Permission rules match tool calls, not intent. `Read(.env)` also stops `cat .env`, but not a
  script that opens the file. For an OS-level limit, turn on the sandbox (`/sandbox`).
