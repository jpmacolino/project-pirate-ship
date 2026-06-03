"""IP deny-list + content-guardrail scan (§5.11, §5.12).

Used by:
  - the PostToolUse hook (immediate feedback when the agent writes a .rpy)
  - the DoD battery / pre-commit gate (hard floor before any commit lands)
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from . import config


@dataclass
class Finding:
    kind: str          # "ip" | "content"
    term: str
    line: int
    path: str | None = None

    def __str__(self) -> str:
        loc = f"{self.path}:{self.line}" if self.path else f"line {self.line}"
        return f"[{self.kind}] {loc}  ->  {self.term!r}"


_IP_RES = [re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE) for t in config.IP_DENYLIST]
_THEME_RES = [re.compile(p, re.IGNORECASE) for p in config.THEME_REVIEW_PATTERNS]


def scan_text(text: str, path: str | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for rx, term in zip(_IP_RES, config.IP_DENYLIST):
            if rx.search(line):
                findings.append(Finding("ip", term, i, path))
        for rx in _THEME_RES:
            m = rx.search(line)
            if m:
                findings.append(Finding("content", m.group(0).lower(), i, path))
    return findings


def scan_file(path: str | Path) -> list[Finding]:
    p = Path(path)
    if not p.exists() or p.suffix.lower() != ".rpy":
        return []
    return scan_text(p.read_text(encoding="utf-8", errors="replace"), str(p))
