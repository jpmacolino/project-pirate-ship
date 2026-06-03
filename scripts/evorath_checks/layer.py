"""Layer-contract check (§4): narrative .rpy reaches mechanics only via the API.

Flags .rpy files that import systems internals directly instead of calling the
sanctioned API surface. Provisional and intentionally conservative.
"""
from __future__ import annotations
import re
from pathlib import Path

_IMPORT = re.compile(r"^\s*(?:from|import)\s+([a-zA-Z0-9_.]+)", re.M)


def check(root: str | Path = ".") -> list[str]:
    from . import config
    root = Path(root)
    errors = []
    for g in config.NARRATIVE_GLOBS:
        for f in root.glob(g):
            text = f.read_text(encoding="utf-8", errors="replace")
            for m in _IMPORT.finditer(text):
                mod = m.group(1)
                if mod.startswith(config.FORBIDDEN_RPY_IMPORT_PREFIXES):
                    errors.append(
                        f"{f}: narrative imports systems internal {mod!r}; "
                        f"call the mechanics API instead (§4)"
                    )
    return errors
