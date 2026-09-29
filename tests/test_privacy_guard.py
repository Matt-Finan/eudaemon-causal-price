"""Regression tests for .claude/hooks/privacy_guard.sh (exit 0 = allow, 2 = block)."""
import sys
import json
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
GUARD = REPO / ".claude" / "hooks" / "privacy_guard.sh"
LAKE = r"D:\DT data lakes"
WINDOWS_ONLY = pytest.mark.skipif(sys.platform != "win32", reason="Windows path")


def run_guard(stdin: str) -> int:
    return subprocess.run(
        ["bash", GUARD.as_posix()], input=stdin, capture_output=True, text=True
    ).returncode


def call(tool: str, **tool_input) -> str:
    return json.dumps({"tool_name": tool, "tool_input": tool_input, "cwd": str(REPO)})


BLOCKED = [
    call("Read", file_path=LAKE + r"\_registry\secrets\x"),
    call("Read", file_path="D:/DT data lakes/bitwarden/vault.json"),
    call("Grep", pattern="password", path=LAKE + r"\profiles"),
    call("Bash", command='cat "/d/DT data lakes/_registry/secrets/x"'),
    call("Bash", command="cat /d/DT\\ data\\ lakes/_registry/secrets/x"),
    call("Bash", command="cat .env"),
    call("Read", file_path=str(REPO / "github.token")),
    pytest.param(call("Write", file_path=r"C:\Users\someone\elsewhere.txt", content="x"),
                 marks=WINDOWS_ONLY),
    call("Write", file_path="/tmp/elsewhere.txt", content="x"),
    call("Edit", file_path=LAKE + r"\sources.yaml", old_string="a", new_string="b"),
    call("Write", file_path=str(REPO / ".env"), content="X=1"),
]

ALLOWED = [
    call("Read", file_path=LAKE + r"\_registry\sources.yaml"),
    call("Bash", command="python -m pytest"),
    call("Grep", pattern="def main", path=str(REPO)),
    call("Read", file_path=str(REPO / ".env.example")),
    # Config files inside the repo may name denied paths in their content.
    call("Write", file_path=str(REPO / "AGENTS.md"), content=LAKE + r"\_registry\secrets"),
    call("Edit", file_path=str(REPO / ".gitignore"), old_string="a", new_string=".env"),
    # /done writes to the project folder (EXTRA_WRITE_ROOTS).
    pytest.param(call("Edit", file_path=r"C:\Users\mattf\OneDrive\Desktop\jarvis\files\personal"
                      r"\career\AI\Projects\eudaemon\00 plan\STATE.md", old_string="a", new_string="b"),
                 marks=WINDOWS_ONLY),
]


@pytest.mark.parametrize("stdin", BLOCKED)
def test_blocks(stdin):
    assert run_guard(stdin) == 2


@pytest.mark.parametrize("stdin", ALLOWED)
def test_allows(stdin):
    assert run_guard(stdin) == 0


@pytest.mark.parametrize("stdin", ["", "not json", "[]"])
def test_fails_closed_on_bad_input(stdin):
    assert run_guard(stdin) == 2
