# HOWTO: develop software with this template and Claude Code

Step by step, from a new repository to a merged milestone. The rules Claude follows are in
[AGENTS.md](../AGENTS.md); why the harness looks the way it does is in
[architecture.md](architecture.md#harness-design).

The short version: say what Claude can't see, give it a check to run, and let the hooks enforce the
few rules that can't have exceptions. Claude Code's defaults (Opus 5.5, medium effort, auto mode,
automatic compaction) need no tuning for most work.

## 0. Prerequisites

- [uv](https://docs.astral.sh/uv/) (it installs Python), git, and
  [Claude Code](https://code.claude.com/docs/en/overview).
- Optional: the [GitHub CLI](https://cli.github.com/) `gh`, signed in. Claude then opens PRs and
  reads review comments without further setup.

## 1. Create the project (once)

1. On GitHub, click **Use this template** (or `gh repo create <name> --template <this repo> --clone`)
   and clone the new repository.
2. Install and check the baseline:
   ```bash
   uv sync && uv run pre-commit install
   uv run pre-commit run --all-files   # must pass before you change anything
   ```
3. Set `name` and `description` in `pyproject.toml`.
4. Start `claude` in the repo and accept the trust dialog. Only then do the project's hooks and
   `allow` rules take effect. Run `/context` once to confirm that `AGENTS.md` is loaded.
5. Ask Claude to replace the example (`src/app/core.py`, `tests/test_core.py`) once your first
   milestone defines real code; until then it keeps the gate green.

## 2. Shape the work (larger features only)

For a new product or a feature that spans several sessions, write the spec first. Let Claude
interview you instead of writing it alone:

```text
I want <goal in two sentences>. Interview me until you could write the spec, then write it to
PRD.md. Keep its headings; every acceptance criterion must be testable.
```

- `/effort low` makes the back-and-forth faster; the interview doesn't need deep reasoning.
- Read `PRD.md` yourself. Cut gold-plating into **Non-goals**. Then commit it (`/commit-git`).
- Alternative: write `PRD.md` by hand, or generate it with your own skills. The headings are the
  contract.

Skip this step for a bug fix or a small change. Go to [Small changes](#small-changes).

## 3. Build one milestone

1. Start clean: `/clear` (or a new `claude` session). The build begins with a fresh context and the
   written definition of done.
2. Prompt with the milestone and how to prove it:
   ```text
   Implement M1 from PRD.md. Tests first: show each new test failing, then make it pass.
   Update M1's status line when done.
   ```
   Add what Claude can't know: a preferred library, an approach you rejected, a file to copy the
   pattern from. If you want more than the minimum, say `be ambitious` and name what you mean.
3. Watch the first minute. Press `Esc` the moment Claude drifts and redirect it.
4. For a change across many files, press `Shift+Tab` for plan mode first and approve the plan.
5. When Claude stops, the Stop hook runs the full gate if `.py` files changed. If it fails, Claude
   gets the failures back and keeps working.

Effort: the default `medium` fits scoped feature work. Use `/effort high` (or `xhigh`) for a bug in
unfamiliar code, a flaky test, or a schema change with many readers. For one hard question in
otherwise routine work, put `ultrathink` in that prompt instead.

## 4. Verify and review

1. Ask for evidence, not a claim: the commands Claude ran and their output (red, then green, then
   the gate).
2. Spec review by a reader who didn't write the code:
   ```text
   have the reviewer compare the diff against M1 in PRD.md
   ```
   The `reviewer` agent can only read. It reports correctness gaps and skips style; fix only what
   affects correctness.
3. Bug hunt: `/code-review` reviews the diff in a fresh subagent. For risky changes add
   `/security-review`, or let a second tool such as Codex review against `AGENTS.md`.
4. For anything with a UI or CLI, `/verify` has Claude run the app and look at the result.

## 5. Commit, push, merge

1. `/commit-git` creates small Conventional Commits through the gate. Only you can start it.
2. Say `push and open a PR` when you're ready. `git push` always asks for your approval.
3. CI runs the same gate on Python 3.11 and 3.14. A person approves the merge.
4. Next milestone: `/clear`, then step 3 again.

## Small changes

No PRD. Name the file, the symptom, and what "fixed" looks like:

```text
slugify drops digits after an umlaut ("Ä1" -> "ä"). Look at src/app/core.py, write a failing test
that reproduces it, then fix it.
```

Then step 4 (evidence; `/code-review` if the change is risky) and step 5.

## Steer the session and keep cost down

| Situation | Do this |
|---|---|
| Claude heads the wrong way | `Esc`, then redirect. `/rewind` (or `Esc Esc`) rolls code and conversation back. |
| Two corrections didn't help | `/clear` and write one better prompt that includes what you learned. |
| Switching to an unrelated task | `/clear`, so the old history isn't paid for on every turn. |
| Work spans several days | `/rename <name>` now, `claude --resume <name>` later. |
| Quick side question | `/btw <question>` adds nothing to the history. |
| Usage seems high | `/usage` shows what each skill, subagent, plugin and MCP server costs. |
| Long session, cache cold | Prefer a fresh session over `/compact` if you don't need the history. |

Checkpoints only cover edits made with Claude's file tools. Commit often; git is the real safety net.

## Parallel and unattended runs

- Parallel work: `claude -w <name>` starts a session in its own worktree. A worktree has no `.venv`
  and no `.env`; Claude runs the setup command from `AGENTS.md`, and a `.worktreeinclude` file at
  the repo root (gitignore syntax, e.g. `.env`) copies small gitignored files into each worktree.
- Long run in a session: `/goal all tests pass and the gate is green` keeps Claude going until a
  separate check confirms the condition.
- From a script: `claude -p "<task>" --max-turns 30` (add `--max-budget-usd`), see the
  [headless docs](https://code.claude.com/docs/en/headless). Before leaving a run alone, check: does
  it know what done is (PRD milestone or failing test), can it check itself (gate), what may it touch,
  what stops it, who approves the result.

## Extend the harness only when a gap shows up

Every addition costs tokens or maintenance. Add one only after you have seen the problem twice.

| You observe | Add |
|---|---|
| Claude rediscovers or gets a project fact wrong | One line in `AGENTS.md` (limit: 100 lines) |
| A convention applies only to part of the code | `.claude/rules/<topic>.md` with a `paths:` filter |
| A repeated procedure (release, migration, deploy) | `.claude/skills/<name>/SKILL.md`; `disable-model-invocation: true` if it has side effects |
| Something must happen or never happen, no exceptions | A hook or a deny rule in `.claude/settings.json` |
| Your personal preference only | `CLAUDE.local.md` (gitignored) or `~/.claude/` |
| Repeated permission prompts in manual mode | `/fewer-permission-prompts` |

`/doctor prompt-audit` flags instructions that are outdated, contradictory or point at missing files.
Remove what no longer earns its place.

## Keep the harness current

Anthropic updates its guidance as models improve, and advice that was right last quarter can become
dead weight. When a session starts and the last review is more than 30 days old, a reminder appears.
Before you begin work in that session:

1. Run `/harness-review` (optionally with extra sources, e.g. `/harness-review <announcement URL>`).
2. Claude checks the [best practices](https://code.claude.com/docs/en/best-practices) (only if the
   page changed) and the Claude Code changelog since the last reviewed version, and evaluates the
   impact on each harness component.
3. It presents a table of proposals and asks you about each one: adopt, reject, or defer.
4. It applies only what you adopted (tests first, gate green, docs updated) and records every
   decision in [harness-review.md](harness-review.md). Then `/commit-git`.

You can run the review at any time, for example after an announcement of a new model.

## Optional add-ons

Not enabled in the repository: each loads skill descriptions into every session and overlaps with
built-ins (plan mode, `/code-review`, subagents). Install them for yourself (user scope) if a task
needs them, and check `/usage` to see whether they pay off.

| Add-on | Install |
|---|---|
| [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design): UI design | `/plugin marketplace add anthropics/claude-code`, then `/plugin install frontend-design` |
| [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT): UI/UX data and styles | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill`, then `/plugin install ui-ux-pro-max` |
| [superpowers](https://github.com/obra/superpowers) (MIT): TDD, debugging, planning skills | `/plugin marketplace add obra/superpowers-marketplace`, then `/plugin install superpowers` |
| [gsd-core](https://github.com/open-gsd/gsd-core) (MIT): spec-driven phase loop | `/plugin marketplace add open-gsd/gsd-core`, then `/plugin install gsd-core` |
| [gstack](https://github.com/garrytan/gstack) (MIT, Bun) | see its README (`~/.claude/skills/gstack`, `./setup`) |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) (MIT, Node ≥ 20.19) | `npm install -g @fission-ai/openspec@latest`, then `openspec init` |

[pi](https://github.com/earendil-works/pi) is a separate coding-agent CLI, not a Claude Code add-on.
