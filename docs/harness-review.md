# Harness review log

Written by `/harness-review` ([skill](../.claude/skills/harness-review/SKILL.md)). The state lines
below are machine-read: the SessionStart hook reminds you once `last-review` is over 30 days old,
and the skill uses the hash and version to read only what changed since the last review.

## State

- last-review: 2026-10-27
- best-practices-sha256: 3a737bc6ffa82ea2aae5c6c19047d1c8e74a517fea82ce809ea92f2f9175c7ba
- claude-code-version: 2.1.311

## Decisions

Newest first. Rejected and deferred proposals stay listed so they aren't proposed again unchanged.

| Date | Source | Proposal | Decision | Why |
|---|---|---|---|---|
| 2026-10-27 | [Best practices](https://code.claude.com/docs/en/best-practices) (Opus 5.5) | Align the harness: short AGENTS.md, gate as definition of done, hooks only for rules without exceptions, plugins opt-in | adopted | [architecture.md](architecture.md#harness-design) |
| 2026-10-27 | User request | Regular, dialog-based review of new best practices (`/harness-review`, reminder hook) | adopted | Keep the harness current without loading anything into normal sessions |
