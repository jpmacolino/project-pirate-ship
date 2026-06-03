#!/usr/bin/env python3
"""SessionStart hook: re-orient a resumed unsupervised run."""
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True).stdout.strip()
    except Exception:
        return ""

OPEN_QUESTIONS = (
    "Open spec questions still live: 7.1 what physically sank the ship; "
    "7.4 camp name; 7.5 creation math; 7.7 skill/trait reconciliation; "
    "7.9 nat-20/nat-1 rule."
)

def main():
    branch = git("rev-parse", "--abbrev-ref", "HEAD") or "unknown"
    dirty = git("status", "--porcelain")
    blocked = (ROOT / "BLOCKED.md")
    ctx = [f"Current branch: {branch}",
           f"Working tree: {'dirty' if dirty else 'clean'}",
           OPEN_QUESTIONS]
    if blocked.exists():
        ctx.append("A BLOCKED.md report exists from a prior run — read it first.")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "\n".join(ctx),
    }}))

if __name__ == "__main__":
    main()
