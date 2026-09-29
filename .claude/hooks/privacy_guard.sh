#!/usr/bin/env bash
# PreToolUse hook. Thin wrapper around privacy_guard.py that fails closed:
# Claude Code only blocks on exit 2, so any other non-zero exit (python missing,
# crash, bad path) is converted to 2 rather than letting the call through.
here="$(cd "$(dirname "$(printf '%s' "$0" | tr '\\' '/')")" && pwd)"
py="$(command -v python || command -v python3)"
if [ -z "$py" ] || [ -z "$here" ]; then
  echo "privacy_guard: python or hook directory not found; failing closed" >&2
  exit 2
fi
"$py" "$here/privacy_guard.py"
rc=$?
[ "$rc" -eq 0 ] && exit 0
exit 2
