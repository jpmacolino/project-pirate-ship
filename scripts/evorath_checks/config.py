"""Central configuration for the Evorath guardrail layer.

Everything project-shaped lives here so the checks stay generic. Paths assume
the standard Ren'Py layout (game/ at the project root).
"""
from __future__ import annotations
import os

# --- Layout -----------------------------------------------------------------
NARRATIVE_GLOBS      = ["game/**/*.rpy"]
SYSTEM_PYTHON_GLOBS  = ["game/systems/**/*.py"]   # the pure-Python layer you audit (§3)
ASSET_ROOTS          = ["game/images", "game/audio"]

# --- The sanctioned mechanics API surface (§4 / §5.9) -----------------------
# Narrative .rpy is allowed to reach mechanics ONLY through these names.
SANCTIONED_API = {
    "check", "check_skill",          # d20 + attr + skill vs DC (adv=None)
    "adjust_stat",
    "set_flag", "has_flag",
    "add_item", "has_item",
}

# .rpy should never import the internals of the systems package directly;
# it goes through the API module. (Provisional — tighten once the package exists.)
FORBIDDEN_RPY_IMPORT_PREFIXES = ("game.systems.", "systems.")

# --- IP deny-list (§5.11) ---------------------------------------------------
# Proprietary named IP that must never appear in shipped content. Mechanics are
# free; named expression is not. Matched case-insensitively as whole words.
IP_DENYLIST = [
    "beholder", "illithid", "mind flayer", "mindflayer",
    "githyanki", "githzerai", "forgotten realms", "faerun",
    "tharizdun", "displacer beast", "umber hulk",
    # NOTE: "drow" is borderline D&D IP. Evorath uses Hájje, so include it as a
    # guard but confirm in the IP pass. Remove if you decide it's generic.
    "drow",
]

# --- Content guardrail (§5.12 Hájje heritage) ------------------------------
# The agent may reference the Hájje's feared/tragic heritage IN THE ABSTRACT.
# These patterns flag any drift toward GRAPHIC sexual-violence content for a
# hard block + human review. Kept deliberately small and non-descriptive.
THEME_REVIEW_PATTERNS = [
    r"\brape\b", r"\brap(?:ed|ing|ist)\b",
    r"\bmolest", r"\bsexual(?:ly)?\s+assault",
]

# --- Toggles / decisions embedded here so they're one edit away -------------
DOD_GIVE_UP_N = 3           # Stop-hook: allow stop after N no-progress loops (the give-up policy)

# Ren'Py executable. Point RENPY_SDK at your SDK folder, or put `renpy` on PATH.
def renpy_cmd() -> list[str]:
    sdk = os.environ.get("RENPY_SDK")
    if sdk:
        # renpy.sh on *nix, renpy.exe on Windows; the launcher resolves either.
        exe = os.path.join(sdk, "renpy.exe" if os.name == "nt" else "renpy.sh")
        return [exe]
    return ["renpy"]
