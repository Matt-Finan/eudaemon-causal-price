"""PostToolUse audit hook: append one JSON line per tool call to .claude/audit.jsonl.

Records who/what/where, not content: tool name, the target (path, pattern or the first
200 characters of a command), session id and time. Tool output is never logged.
"""
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

LOG = Path(__file__).resolve().parents[1] / "audit.jsonl"
TARGET_KEYS = ("file_path", "notebook_path", "path", "pattern", "url", "command")


def main() -> None:
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input") or {}
    target = {k: str(tool_input[k])[:200] for k in TARGET_KEYS if k in tool_input}
    line = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session": payload.get("session_id"),
        "tool": payload.get("tool_name"),
        "target": target,
        "cwd": payload.get("cwd"),
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # the call already ran; report, never block
        print(f"audit: could not write log line: {exc}", file=sys.stderr)
