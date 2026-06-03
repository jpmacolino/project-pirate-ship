"""Orphan-flag analysis (§6 DoD: 'no orphan mechanical flags').

A flag set but never read  -> orphan producer.
A flag read but never set  -> dangling consumer.
Both are reported. Provisional: only catches string-literal flag names; dynamic
names need a runtime trace (see scripts/playthrough.py).
"""
from __future__ import annotations
import re
from pathlib import Path

_SET = re.compile(r"set_flag\(\s*[\"']([^\"']+)[\"']")
_HAS = re.compile(r"has_flag\(\s*[\"']([^\"']+)[\"']")


def _collect(globs: list[str], root: Path):
    produced, consumed = {}, {}
    for g in globs:
        for f in root.glob(g):
            text = f.read_text(encoding="utf-8", errors="replace")
            for m in _SET.finditer(text):
                produced.setdefault(m.group(1), []).append(str(f))
            for m in _HAS.finditer(text):
                consumed.setdefault(m.group(1), []).append(str(f))
    return produced, consumed


def check(root: str | Path = ".") -> list[str]:
    from . import config
    root = Path(root)
    globs = config.NARRATIVE_GLOBS + config.SYSTEM_PYTHON_GLOBS
    produced, consumed = _collect(globs, root)
    errors = []
    for name in sorted(set(produced) - set(consumed)):
        errors.append(f"orphan flag (set, never read): {name!r}  in {produced[name]}")
    for name in sorted(set(consumed) - set(produced)):
        errors.append(f"dangling flag (read, never set): {name!r}  in {consumed[name]}")
    return errors
