# AGENTS.md — eudaemon-causal-price

Read this first, in any tool (Claude Code, Codex, Cowork). Tool-specific notes live in `CLAUDE.md`.

## What this repo is
The public research code for eudaemon (https://eudaemon.uk). The research prices T, the days it takes
to turn a correlation in one person's record into a cause:
T ≥ (7.85/d²) × ((1+ρ)/(1−ρ)) × (M/f), against a drift half-life it must beat.

Planned contents:
- `src/causal_price/` — adapters (read lake sources into tidy series), statistics (ρ, drift, f, d, M, T)
- an MCP server (`lake`, stdio, see `.mcp.json`) — the only door from agents into the data lake, returning summaries, never raw rows
- `tests/` — run against `fixtures/synthetic/` only, never against real lake data
- `docs/methods.md` — the statistical methods, in prose

Licence: Apache-2.0 (`LICENSE`, `NOTICE`).

## Privacy rules (non-negotiable)
1. This repo is public. Nothing from `D:\DT data lakes` is ever committed, pasted into an issue, or printed into a transcript: no raw rows, no file contents, no names, no account identifiers.
2. Never open `D:\DT data lakes\_registry\secrets\`, `D:\DT data lakes\bitwarden\`, or `D:\DT data lakes\profiles\`. Never read `.env` or `*.token` files.
3. Tests and examples use synthetic data from `fixtures/synthetic/` only.
4. Published outputs are summary statistics only; never a raw series. Intimate variables are abstracted.
5. These rules are also enforced mechanically — deny rules and hooks in `.claude/`, and a `detect-secrets` pre-commit hook. Prose is advisory; the enforcement is not. Do not bypass it (no `--no-verify`).

## The three homes
- Project folder (documents for humans, OneDrive):
  `C:\Users\mattf\OneDrive\Desktop\jarvis\files\personal\career\AI\Projects\eudaemon`
- This repo (public code): `C:\dev\eudaemon-causal-price` → github.com/Matt-Finan/eudaemon-causal-price. Outside OneDrive on purpose; GitHub is its backup.
- The private lake control plane: `D:\DT data lakes\_registry` → private repo `deep-twin-registry`. Secrets, logs and reports there are never tracked.

## Where the plan lives
In the project folder, not here: `AGENTS.md` (programme map), then `00 plan/STATE.md` (now / next / blocked).
Session end: one line in `00 plan/SESSION-LOG.md`, STATE.md updated (in Claude Code: `/done <what finished>`).
Definitions of T, ρ, f, d, M: `02 research/definitions.md` in the project folder.
