"""Sanctioned mechanics API — pure Python module (§4).

Re-exports the state-taking functions from systems.mechanics so that
game/evorath_api.rpy can import them as `import api` (not `from systems.*`),
satisfying the layer-contract check in evorath_checks/layer.py.

Narrative .rpy files NEVER import this module directly; they call the
wrapper functions defined in evorath_api.rpy which inject player_state.
Tests import from systems.mechanics directly (no Ren'Py needed).
"""
from __future__ import annotations

from systems.mechanics import (           # noqa: F401  (re-exported for evorath_api.rpy)
    GameState,
    CheckResult,
    ATTRIBUTES,
    ATTR_BASE,
    ATTR_CAP,
    FREE_POINT_POOL,
    FREE_POINT_MAX_PER_ATTR,
    DC_EASY,
    DC_MODERATE,
    DC_HARD,
    DC_VERY_HARD,
    resolve_check,
    adjust_stat,
    set_flag,
    has_flag,
    add_item,
    has_item,
)
from systems.creation import CharacterBuilder, CreationError  # noqa: F401
