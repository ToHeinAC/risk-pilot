---
name: commit-git
description: Commit the uncommitted work as small Conventional Commits through the quality gate. Never pushes.
disable-model-invocation: true
---

1. Inspect `git status --porcelain` and `git diff HEAD`, including untracked files.
2. Group the changes by concern: one feature, fix, or doc change per commit.
3. Stage explicit paths only (`git add <path>...`), never `git add -A` or `git add .`. Never stage
   `.env*` (except `.env.example`), `data/`, or anything `.gitignore` excludes.
4. Commit as `<type>(<optional scope>): <subject>` in imperative mood. Types: feat, fix, docs, test,
   refactor, perf, build, ci, chore. Subject ≤ 72 chars; add a body only when the why isn't obvious.
5. The pre-commit gate runs on each commit. If it fails or rewrites files, fix the cause, re-stage
   and commit again. Never amend unless asked.
6. Report the commits (`git log --oneline -n <count>`). Ask before any `git push`.
