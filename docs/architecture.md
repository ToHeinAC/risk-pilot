# Architecture

## Code layers

| Layer | Where | Rule |
|---|---|---|
| Core logic | `src/app/*.py` | Pure functions, fully typed, no I/O. Unit-tested directly. |
| Adapters | `src/app/<adapter>.py` (add when needed) | The only place for network, file, or database I/O. |
| Entry points | CLI / app module (add when needed) | Wire adapters to core logic; keep them thin. |

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
