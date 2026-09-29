"""PreToolUse privacy guard for eudaemon-causal-price.

Reads the hook payload (JSON) on stdin. Exit 0 = allow; exit 2 = block, reason on stderr.
Fails closed: any unexpected error blocks the call.

Rules:
1. Write/Edit-family tools may only touch files inside this repo (plus EXTRA_WRITE_ROOTS).
   Their *content* is not scanned, so the repo's own config files may name denied paths.
2. Every other tool (Read, Grep, Glob, Bash, MCP tools, ...) is blocked if any string in its
   input mentions a denied path.

This is a tripwire, not a sandbox: a shell command that builds a path indirectly
(variables, globs like D:/DT*/_reg*) can evade string matching. The deny rules in
settings.json and OS-level permissions are the other layers.
"""
import os
import re
import sys
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
# Outside roots Write/Edit may touch. The project folder is needed by /done
# (SESSION-LOG.md, STATE.md, INDEX.md lines). Decision 24.09.2026.
EXTRA_WRITE_ROOTS: list[Path] = [
    Path(r"C:\Users\mattf\OneDrive\Desktop\jarvis\files\personal\career\AI\Projects\eudaemon"),
]

DENIED = {
    "lake secrets/bitwarden/profiles": re.compile(
        r"dt data lakes.*\b(secrets|bitwarden|profiles)\b", re.DOTALL
    ),
    "registry secrets": re.compile(r"_registry/secrets\b"),
    ".env file": re.compile(r"(^|[^\w.])\.env(?![\w.-])"),
    "*.token file": re.compile(r"\.token\b"),
}


def normalise(text: str) -> str:
    text = text.lower().replace("\\ ", " ").replace("\\", "/")
    text = text.replace('"', "").replace("'", "")
    return re.sub(r"/+", "/", text)


def denied(text: str) -> str | None:
    norm = normalise(text)
    for name, pattern in DENIED.items():
        if pattern.search(norm):
            return name
    return None


def strings(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in strings(v)]
    return []


def resolve(target: str, cwd: str) -> str:
    target = re.sub(r"^/([a-zA-Z])/", r"\1:/", target)  # Git Bash /c/... -> C:/...
    path = Path(target)
    if not path.is_absolute():
        path = Path(cwd) / path
    return os.path.normcase(os.path.realpath(path))


def inside_allowed_root(resolved: str) -> bool:
    for root in [REPO, *EXTRA_WRITE_ROOTS]:
        root_norm = os.path.normcase(os.path.realpath(root))
        if resolved == root_norm or resolved.startswith(root_norm + os.sep):
            return True
    return False


def block(reason: str) -> int:
    print(f"privacy_guard: blocked. {reason}", file=sys.stderr)
    return 2


def main() -> int:
    payload = json.load(sys.stdin)
    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}
    cwd = payload.get("cwd") or os.getcwd()

    if tool in WRITE_TOOLS:
        target = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not target:
            return block(f"{tool} call has no file path.")
        if hit := denied(target):
            return block(f"{tool} targets a denied path ({hit}).")
        if not inside_allowed_root(resolve(target, cwd)):
            return block(f"{tool} outside the repo is not allowed: {target}")
        return 0

    if hit := denied("\n".join(strings(tool_input))):
        return block(f"{tool} input mentions a denied path ({hit}).")
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except Exception as exc:  # fail closed
        code = block(f"guard error, failing closed: {type(exc).__name__}: {exc}")
    sys.exit(code)
