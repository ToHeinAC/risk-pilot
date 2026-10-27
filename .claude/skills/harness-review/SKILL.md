---
name: harness-review
description: Check Anthropic's latest Claude Code best practices and changelog against this harness, discuss proposed changes with the user, apply only the approved ones, and log every decision.
argument-hint: "[extra source URLs, e.g. an Anthropic announcement]"
disable-model-invocation: true
---

Review this repository's Claude Code harness against Anthropic's current guidance. The user decides;
you research, evaluate and propose. Change nothing before the user has approved it.

## 1. Find what changed

Read the state lines and the decision table in `docs/harness-review.md`.

- Best practices: `curl -fsSL https://code.claude.com/docs/en/best-practices.md | sha256sum`.
  If the hash differs from `best-practices-sha256`, read the page in full; otherwise skip it.
- Changelog: read only the entries newer than `claude-code-version`:
  `curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md | awk '/^## <version>$/{exit} {print}'`
  Keep only entries that touch what the harness uses: CLAUDE.md/memory, skills, subagents, hooks,
  permissions, settings, plugins, models and effort, defaults.
- Every URL in `$ARGUMENTS` (for example an Anthropic engineering post or release note).
- Follow a linked docs page only when a change points to it and it matters for the harness.

If nothing relevant changed, update `last-review` (and the version), tell the user in one line, and stop.

## 2. Evaluate the impact

Harness components: `AGENTS.md`/`CLAUDE.md`, `.claude/settings.json` (permissions, hooks),
`.claude/hooks/`, `.claude/skills/`, `.claude/agents/`, the gate (`.pre-commit-config.yaml`,
`pyproject.toml`, CI), `PRD.md`, `docs/HOWTO.md`, `docs/architecture.md`.

For each relevant change, decide whether it makes a component obsolete, wrong, or missing. Apply the
best-practices test: every component encodes an assumption about what the model can't do on its own.
Propose only what improves clarity, token use or user experience in practice; "no change" is a valid
result. Skip proposals already rejected in the decision table unless the source changed the argument.

## 3. Decide with the user

Present a short table: change in the source (with link), affected component, proposal
(keep / change / remove / add), effect on tokens, enforcement and UX. Then ask about each proposal
with AskUserQuestion: adopt, reject, or defer. Recommend one option and say why.

## 4. Apply and record

1. Apply the adopted proposals. Follow AGENTS.md: test first for hook or gate changes, then the full
   gate, and update affected docs (HOWTO, architecture, README) in the same change.
2. Update `docs/harness-review.md`: the three state lines, and one row per proposal (adopted,
   rejected and deferred) at the top of the decision table.
3. Report what changed and offer `/commit-git`.
