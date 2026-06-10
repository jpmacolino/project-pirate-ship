"""Tests for game/systems/mechanics.py (§5.9, §5.10, §7.9)."""
import random
import pickle

import pytest

from systems.mechanics import (
    GameState, CheckResult,
    ATTR_BASE, ATTR_CAP,
    DC_EASY, DC_MODERATE, DC_HARD,
    resolve_check, adjust_stat, set_flag, has_flag, add_item, has_item,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def state():
    return GameState()


class FixedRng:
    """Deterministic RNG for test reproducibility."""
    def __init__(self, *values):
        self._queue = list(values)

    def randint(self, lo, hi):
        return self._queue.pop(0)


# ---------------------------------------------------------------------------
# Basic check resolution
# ---------------------------------------------------------------------------

def test_check_passes_when_total_beats_dc(state):
    state.attributes["INT"] = 5
    state.skills["Investigation"] = 1
    rng = FixedRng(10)                  # d20 = 10; 10+5+1=16 vs DC 12
    result = resolve_check(state, "INT", "Investigation", DC_MODERATE, _rng=rng)
    assert result.passed
    assert result.total == 16
    assert result.die_used == 10


def test_check_fails_when_total_misses_dc(state):
    state.attributes["INT"] = 2
    rng = FixedRng(3)                   # d20 = 3; 3+2+0=5 vs DC 12
    result = resolve_check(state, "INT", "Investigation", DC_MODERATE, _rng=rng)
    assert not result.passed
    assert result.total == 5


# ---------------------------------------------------------------------------
# Nat-20 / Nat-1 (§7.9 resolved)
# ---------------------------------------------------------------------------

def test_nat20_always_succeeds(state):
    state.attributes["INT"] = 1
    rng = FixedRng(20)                  # nat-20 vs DC 30 (impossible without it)
    result = resolve_check(state, "INT", None, 30, _rng=rng)
    assert result.nat20
    assert result.passed


def test_nat1_always_fails(state):
    state.attributes["INT"] = 10
    state.skills["Investigation"] = 1
    rng = FixedRng(1)                   # nat-1; 1+10+1=12 would normally pass DC 8
    result = resolve_check(state, "INT", "Investigation", DC_EASY, _rng=rng)
    assert result.nat1
    assert not result.passed


# ---------------------------------------------------------------------------
# Advantage / Disadvantage (§5.10)
# ---------------------------------------------------------------------------

def test_advantage_takes_higher(state):
    rng = FixedRng(8, 15)               # roll 8 and 15; advantage picks 15
    result = resolve_check(
        state, "STR", None, DC_HARD,
        adv_sources=[("Brine in Blood", 1)],
        _rng=rng,
    )
    assert result.die_used == 15
    assert result.die_rolls == [8, 15]
    assert result.net_adv == 1


def test_disadvantage_takes_lower(state):
    rng = FixedRng(14, 5)               # roll 14 and 5; disadvantage picks 5
    result = resolve_check(
        state, "CHA", "Diplomacy", DC_MODERATE,
        adv_sources=[("Hájje heritage stigma", -1)],
        _rng=rng,
    )
    assert result.die_used == 5
    assert result.die_rolls == [14, 5]
    assert result.net_adv == -1


def test_net_sign_two_adv_one_disadv_is_advantage(state):
    """2 advantage + 1 disadvantage = net +1 → advantage roll (§5.10)."""
    rng = FixedRng(7, 14)
    result = resolve_check(
        state, "CHA", None, DC_EASY,
        adv_sources=[
            ("Elf kinship", 1),
            ("Good equipment", 1),
            ("Outsider unease", -1),
        ],
        _rng=rng,
    )
    assert result.net_adv == 1
    assert result.die_used == 14         # took higher


def test_neutral_net_adv_is_straight_roll(state):
    rng = FixedRng(11)
    result = resolve_check(
        state, "STR", None, DC_MODERATE,
        adv_sources=[("Adv", 1), ("Disadv", -1)],
        _rng=rng,
    )
    assert result.net_adv == 0
    assert len(result.die_rolls) == 1


# ---------------------------------------------------------------------------
# Adv sources: labels are preserved in CheckResult
# ---------------------------------------------------------------------------

def test_adv_sources_carried_in_result(state):
    sources = [("Brine in Blood", 1), ("High ground", 1)]
    rng = FixedRng(10, 12)
    result = resolve_check(state, "STR", None, DC_EASY, adv_sources=sources, _rng=rng)
    assert result.adv_sources == sources


# ---------------------------------------------------------------------------
# Stat / flag / inventory mutations
# ---------------------------------------------------------------------------

def test_adjust_attribute_clamps_at_cap(state):
    state.attributes["STR"] = 9
    adjust_stat(state, "STR", 5)        # 9+5=14 → clamped to ATTR_CAP
    assert state.attributes["STR"] == ATTR_CAP


def test_adjust_attribute_clamps_at_one(state):
    state.attributes["STR"] = 2
    adjust_stat(state, "STR", -10)
    assert state.attributes["STR"] == 1


def test_adjust_skill_creates_if_missing(state):
    adjust_stat(state, "Diplomacy", 1)
    assert state.skills["Diplomacy"] == 1


def test_set_flag_and_has_flag(state):
    assert not has_flag(state, "found_anomaly")
    set_flag(state, "found_anomaly")
    assert has_flag(state, "found_anomaly")


def test_add_item_and_has_item(state):
    assert not has_item(state, "rope_coil")
    add_item(state, "rope_coil")
    assert has_item(state, "rope_coil")
    # Duplicates allowed (stackables)
    add_item(state, "rope_coil")
    assert state.inventory.count("rope_coil") == 2


# ---------------------------------------------------------------------------
# Picklability — required for Ren'Py save/load (§6 DoD)
# ---------------------------------------------------------------------------

def test_gamestate_is_picklable(state):
    state.attributes["INT"] = 7
    state.skills["Investigation"] = 1
    state.traits.add("brine_in_blood")
    state.flags.add("found_anomaly")
    state.inventory.append("rope_coil")
    restored = pickle.loads(pickle.dumps(state))
    assert restored.attributes["INT"] == 7
    assert "brine_in_blood" in restored.traits
    assert "found_anomaly" in restored.flags
    assert "rope_coil" in restored.inventory
