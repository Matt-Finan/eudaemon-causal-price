#!/usr/bin/env bash
# PostToolUse hook. Wrapper around audit.py; appends one JSON line per tool call
# to .claude/audit.jsonl (gitignored). Never blocks: the tool has already run.
here="$(cd "$(dirname "$(printf '%s' "$0" | tr '\\' '/')")" && pwd)"
py="$(command -v python || command -v python3)"
[ -n "$py" ] && [ -n "$here" ] && "$py" "$here/audit.py"
exit 0
