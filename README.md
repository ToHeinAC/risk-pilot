# claude-dev-schema

A GitHub template for Python projects built with Claude Code. It follows the
[Claude Code best practices](https://code.claude.com/docs/en/best-practices): a short instruction
file with only what Claude can't see in the code, one executable quality gate as the definition of
done, and hooks only for the rules that can't have exceptions. Everything else is left to Claude
Code's defaults.

**How to use it, step by step: [docs/HOWTO.md](docs/HOWTO.md).**

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
src/app/             code (the slugify example is a placeholder)
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
| Doc size limits (AGENTS.md ≤ 100 lines), no broken local links | | yes | yes | yes |
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
