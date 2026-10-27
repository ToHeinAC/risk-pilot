# AGENTS.md

Project facts an AI coding agent can't read from the code. Claude Code loads this file via
`CLAUDE.md`; Codex reads it directly. Keep it short: every line costs tokens in every session.
Step-by-step usage of this template: [docs/HOWTO.md](docs/HOWTO.md).

## Commands

- Setup (once per clone or worktree): `uv sync && uv run pre-commit install`
- One test file: `uv run pytest tests/test_core.py -q`
- Lint and format: `uv run ruff check --fix . && uv run ruff format .`
- Types: `uv run pyright`
- Full gate, the same one the Stop hook, `git commit` and CI run: `uv run pre-commit run --all-files`

## Conventions

- Dependencies only through uv: `uv add <pkg>`, dev tools `uv add --dev <pkg>`, never `pip install`.
  Commit `uv.lock`.
- Network, file and database I/O lives in adapter modules. Core logic stays pure and is tested
  without I/O ([docs/architecture.md](docs/architecture.md)).
- Tests are offline: `tests/conftest.py` blocks sockets. Use synthetic fixtures.
- Configuration comes from environment variables. Secrets only in `.env`; list the keys without
  values in `.env.example`. Runtime data goes in `data/`. Both are gitignored.
- Dependencies and copied code need a license compatible with Apache-2.0 (MIT, BSD, ISC, PSF,
  Apache-2.0). Record copied code in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Definition of done

1. For a behavior change, write the test first and show it failing for the expected reason, then
   make it pass. Report both outputs as evidence.
2. The full gate passes.
3. The same change updates what it made false: the milestone status in [PRD.md](PRD.md), README,
   `docs/`. Change PRD.md scope (goals, criteria, milestones) only with the user's approval.
4. Commit only when asked (`/commit-git`). Never push without asking.

## Gotchas

- `pre-commit run --all-files` only lints files git tracks. `git add` new files before relying on
  the gate.
- Coverage (≥ 85 % branch) is only measured by the gate's `pytest --cov`, so a single test file
  never fails on it.
- The Stop hook runs the full gate when `.py` files changed and sends Claude back once if it fails.
