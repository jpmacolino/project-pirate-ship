"""Referenced-asset existence check (§5.7, §6).

The entire enforcement story for art in MVP: every image/audio a .rpy references
must exist in the approved asset folder. No generator in the autonomous path.
Provisional patterns — extend as the script grows.
"""
from __future__ import annotations
import re
from pathlib import Path

_REFS = [
    re.compile(r"""\bimage\b[^\n=]*=\s*[\"']([^\"']+\.(?:png|jpg|jpeg|webp|gif))[\"']""", re.I),
    re.compile(r"""\b(?:scene|show)\b[^\n]*?[\"']([^\"']+\.(?:png|jpg|jpeg|webp))[\"']""", re.I),
    re.compile(r"""\bplay\s+(?:music|sound|audio)\s+[\"']([^\"']+\.(?:ogg|mp3|wav|opus))[\"']""", re.I),
    re.compile(r"""\bImage\(\s*[\"']([^\"']+)[\"']""", re.I),
]


def check(root: str | Path = ".") -> list[str]:
    from . import config
    root = Path(root)
    game = root / "game"
    errors = []
    for g in config.NARRATIVE_GLOBS:
        for f in root.glob(g):
            text = f.read_text(encoding="utf-8", errors="replace")
            for rx in _REFS:
                for m in rx.finditer(text):
                    rel = m.group(1).lstrip("/")
                    # Ren'Py resolves asset paths relative to game/.
                    if not (game / rel).exists():
                        errors.append(f"missing asset {rel!r} referenced in {f}")
    return errors
