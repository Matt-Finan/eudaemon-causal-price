# 01 — Setting up eudaemon-causal-price (DRAFT)

Status: draft, 24.09.2026. Covers Part A steps 1–3 and the hook decisions. Steps 4–10 not started.
Paragraphs marked *[Claude's draft — rewrite in my words]* are not yet from my own answers.

## CLAUDE.md and AGENTS.md
AGENTS.md is the tool-neutral brief: what the repo is, the privacy rules, the three homes, where the
plan lives. A rule like "tests never use real lake data" goes there, because it has to hold whichever
tool is running — Claude Code, Codex or Cowork — and switching tools shouldn't change the rules of
engagement; a rule that only lived in CLAUDE.md would vanish the moment I used Codex, which for lake
data could mean a leak or a deletion. CLAUDE.md starts with `@AGENTS.md` and holds only
Claude-specific facts (test runner, CLI, commit conventions). If a rule were in both, Claude would read
two copies, and once they drift it can't tell which rule is in force. Both files load into every
session, so they are kept short (CLAUDE.md under 120 lines): long context files cost tokens and get
ignored. Both are advisory — the model can ignore them.
Correction I took: the deny rules and hooks govern *Claude's* tool calls, not code that pytest runs.
Stopping a test from opening lake files needs a guard inside the test suite (e.g. a conftest fixture);
CI only catches it by accident because its runner has no D: drive. Name which actor each control covers.
The enterprise analogue is one policy document shared across every vendor's tool, with tool-specific
runbooks that point to it rather than copy it.

## Settings: permission rules (`.claude/settings.json`)
Deny rules on the lake's secrets, bitwarden and profiles folders, `.env` and `*.token`; an allow on the
rest of the lake for now (the `lake` MCP server replaces direct reads later). Rules are evaluated deny →
ask → allow, and deny is prioritised: a secrets file still cannot be read even if someone adds a more
specific allow for it. It is category order that decides, not position in the file or specificity — to
open that file you would have to narrow the deny itself. A deny rule is enforced by the harness before
the tool runs; an instruction in CLAUDE.md is only something the model reads. Gap: Read/Edit rules
don't cover `cat` in Bash — which is why the hook exists. The file is checked in, so everyone who clones
gets the same guardrails; personal overrides go in the gitignored `settings.local.json`.
The enterprise analogue is IAM policy where an explicit deny beats any allow, locked org-wide with
managed settings.

## Hooks (`.claude/hooks/`)
The guard has to run before the tool call: if it ran after, the tool might already have accessed
things it didn't need, and it would be impossible to put the milk back into the udder — even with the
best intention, you can't row back from access after the fact. Prevent beats detect.
The audit hook may fail open because it runs after the tool and can't block anything anyway; failing
closed would only stop all work when the log breaks. Controls that prevent fail closed; controls that
record fail loud but open (a strictly regulated shop might still choose "no log, no action").
*[Claude's draft below — rewrite in my words]*
`privacy_guard.sh` is a PreToolUse hook: it runs before every tool call and exit code 2 blocks it.
It blocks Write/Edit outside the repo (and outside the project folder, which `/done` needs), and blocks
any read, search or shell command whose input names a denied path. The repo's own config files may
name those paths, because the content of writes inside the repo isn't scanned. It fails closed: a
try/except in Python and a bash wrapper that turns any non-zero exit into 2, because Claude Code only
blocks on exit 2 — a crashing guard would otherwise let the call through. It has a regression suite
(`tests/test_privacy_guard.py`, 21 cases, including bad input). Proven live on 24.09.2026: a Read of
the secrets folder was stopped by the deny rule; `cat` of the same path in Bash was stopped by the hook.
`audit.sh` is a PostToolUse hook appending one JSON line per successful tool call to
`.claude/audit.jsonl` (gitignored): tool, target, session, time — never the output. PostToolUse only
fires on success, so blocked attempts are not logged yet (a PostToolUseFailure hook would add them).
Advisory vs deterministic: CLAUDE.md is advisory — a probabilistic model usually follows it. Hooks and
deny rules are deterministic — ordinary code the harness runs, where the model has no vote.
Honest limits: string matching can be evaded (globs, variables), and the Write/Edit block doesn't cover
Bash redirects; the real boundary is OS permissions or the sandbox. The hook is a tripwire on top.
Decisions (24.09.2026): project folder added to the write allowlist for `/done`; the `/done` skill file
will be written as a one-off; Part B runs in its own session opened in `_registry`.
The enterprise analogue is a policy-enforcement point plus an audit trail — like a DLP gateway and
SIEM logging in front of an employee's actions.

## Still to write (steps 4–10)
Skills, MCP placeholder, CI, detect-secrets, commit trailers.
