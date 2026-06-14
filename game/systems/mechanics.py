"""Core d20 mechanics for Evorath (§5.9, §5.10).

Pure Python — never imports renpy. Usable in pytest without the engine.
All mutable operations take a GameState; the API layer (game/api.py) injects
the live store variable so narrative .rpy never touches internals directly.

Resolution: d20 + attribute_value + skill_rank vs DC.
  Nat-20  → auto-success (§7.9 resolved: nat-20 auto-succeeds).
  Nat-1   → auto-fail   (§7.9 resolved: nat-1 auto-fails).
  Adv/disadv: net sign, gather all sources simultaneously (§5.10).
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Sequence

# Primary attributes (§5.9)
ATTRIBUTES = ("STR", "DEX", "INT", "CHA", "SPR", "END")

# Attribute base at creation (§5.12 / §7.5 resolved: lean-open, small fixed base)
ATTR_BASE = 3

# Free-point pool at confirm screen (§5.12)
FREE_POINT_POOL = 6
FREE_POINT_MAX_PER_ATTR = 2
ATTR_CAP = 10

# Skill rank values
SKILL_UNTRAINED = 0
SKILL_TRAINED = 1

# Exhaustive MVP skill list (§5.12 creation data; §7.7 names+counts still open but these
# are the skills that exist in the current data — update here if data ever changes)
ALL_SKILLS = (
    "Appraisal",
    "Arcana",
    "Athletics",
    "Diplomacy",
    "Endurance",
    "Seamanship",
    "Survival",
)

# DC bands (§5.9)
DC_EASY = 8
DC_MODERATE = 12
DC_HARD = 16
DC_VERY_HARD = 20


@dataclass
class CheckResult:
    """Outcome of one skill-check resolution."""

    die_rolls: list[int]                    # raw d20 rolls (1 straight, 2 if adv/disadv)
    die_used: int                           # the die value that counted
    attribute: str
    attr_value: int
    skill: str | None
    skill_rank: int
    total: int                              # die_used + attr_value + skill_rank
    dc: int
    passed: bool                            # True iff total >= dc OR nat-20
    nat20: bool
    nat1: bool
    adv_sources: list[tuple[str, int]]      # (label, direction +1/-1)
    net_adv: int                            # -1 | 0 | +1 (sign of net advantage)


@dataclass
class GameState:
    """All serializable game state.

    Pure Python (picklable) so Ren'Py's save/load works automatically when
    this object lives in the store (store.player_state).
    """

    # Identity — locked after chargen
    species: str = ""
    class_: str = ""
    origin: str = ""
    background_id: str = ""
    sex: str = ""
    upbringing: str = ""
    name: str = "the survivor"

    # Primary attributes: name -> value (capped 1–ATTR_CAP)
    attributes: dict[str, int] = field(
        default_factory=lambda: {k: ATTR_BASE for k in ATTRIBUTES}
    )

    # Skills: name -> rank (0 untrained, 1 trained)
    skills: dict[str, int] = field(default_factory=dict)

    # Traits: set of trait IDs
    traits: set[str] = field(default_factory=set)

    # Inventory: list of item IDs (ordered, duplicates matter for stackables)
    inventory: list[str] = field(default_factory=list)

    # Story flags: set of flag names
    flags: set[str] = field(default_factory=set)


# ---------------------------------------------------------------------------
# Core resolution
# ---------------------------------------------------------------------------

def resolve_check(
    state: GameState,
    attribute: str,
    skill: str | None,
    dc: int,
    adv_sources: Sequence[tuple[str, int]] | None = None,
    _rng: random.Random | None = None,
) -> CheckResult:
    """Roll d20 + attribute + skill vs DC.

    adv_sources: sequence of (label, direction) where direction is +1 (advantage)
    or -1 (disadvantage).  Net sign determines the roll mode (§5.10).
    """
    sources = list(adv_sources or [])
    net = sum(d for _, d in sources)
    net_sign = 1 if net > 0 else (-1 if net < 0 else 0)

    attr_val = state.attributes.get(attribute, ATTR_BASE)
    sk_rank = state.skills.get(skill, SKILL_UNTRAINED) if skill else SKILL_UNTRAINED

    roll = _rng.randint if _rng else random.randint
    if net_sign != 0:
        r1, r2 = roll(1, 20), roll(1, 20)
        die_rolls = [r1, r2]
        die_used = max(r1, r2) if net_sign > 0 else min(r1, r2)
    else:
        r = roll(1, 20)
        die_rolls = [r]
        die_used = r

    nat20 = die_used == 20
    nat1 = die_used == 1
    total = die_used + attr_val + sk_rank

    if nat20:
        passed = True
    elif nat1:
        passed = False
    else:
        passed = total >= dc

    return CheckResult(
        die_rolls=die_rolls,
        die_used=die_used,
        attribute=attribute,
        attr_value=attr_val,
        skill=skill,
        skill_rank=sk_rank,
        total=total,
        dc=dc,
        passed=passed,
        nat20=nat20,
        nat1=nat1,
        adv_sources=sources,
        net_adv=net_sign,
    )


# ---------------------------------------------------------------------------
# Stat / flag / inventory mutations
# ---------------------------------------------------------------------------

def adjust_stat(state: GameState, stat: str, delta: int) -> None:
    """Adjust an attribute (clamped 1–ATTR_CAP) or skill rank (clamped 0+)."""
    if stat in state.attributes:
        state.attributes[stat] = max(1, min(ATTR_CAP, state.attributes[stat] + delta))
    else:
        state.skills[stat] = max(0, state.skills.get(stat, 0) + delta)


def set_flag(state: GameState, name: str) -> None:
    state.flags.add(name)


def has_flag(state: GameState, name: str) -> bool:
    return name in state.flags


def add_item(state: GameState, item_id: str) -> None:
    state.inventory.append(item_id)


def has_item(state: GameState, item_id: str) -> bool:
    return item_id in state.inventory
