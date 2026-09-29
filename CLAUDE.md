@AGENTS.md

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
Everything tool-neutral is in `AGENTS.md` (imported above). Only Claude-specific facts go here. Keep it under 120 lines.

## Tests
- Runner: pytest. `python -m pytest` runs everything; `python -m pytest tests/test_smoke.py::test_name` runs one test.
- Tests read `fixtures/synthetic/` only. A test that needs the real lake is wrong — add a synthetic fixture instead.
- CI (`.github/workflows/ci.yml`) runs the same command on every push.

## CLI
- None yet. When the package gains an entry point, document the invocation here (`python -m causal_price ...`).

## Lake access
- Today: direct reads of `D:\DT data lakes\**` are allowed by `.claude/settings.json`, minus the denied folders.
- Later: the `lake` MCP server (`.mcp.json`) replaces direct reads; the allow rule is then removed.

## Guardrails you will hit (by design)
- `.claude/hooks/privacy_guard.sh` (PreToolUse) blocks Write/Edit outside this repo and any read, search or shell command naming a denied path. If it blocks you, stop and tell Matt; do not work around it.
- `.claude/hooks/audit.sh` (PostToolUse) appends one line per tool call to `.claude/audit.jsonl` (gitignored).
- `detect-secrets` runs as a pre-commit hook. If it flags something, fix the file; never `--no-verify`. Update the baseline only for a confirmed false positive: `detect-secrets scan > .secrets.baseline`.

## Commits
- Short imperative subject (≤ 72 chars), body says why. One logical change per commit.
- Keep the `Co-Authored-By: Claude ...` trailer that Claude Code adds: it records which commits were AI-assisted.
- Commit or push only when Matt asks.

## Session end
- Run `/done <what finished>` (user-level skill): it updates SESSION-LOG.md, STATE.md and INDEX lines in the project folder.
