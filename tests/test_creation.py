"""Tests for game/systems/creation.py and game/data/ content (§5.12, §7.5)."""
import pytest

from systems.creation import CharacterBuilder, CreationError
from systems.mechanics import ATTRIBUTES, ATTR_BASE, FREE_POINT_POOL, FREE_POINT_MAX_PER_ATTR


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_elf_warrior(allocations=None, free_skills=None):
    b = CharacterBuilder()
    b.set_species("elf")
    b.set_class("warrior")
    b.set_origin("merchant")
    b.set_background("sea_life")
    b.set_flavor("she", "two_parents")
    b.allocate_free_points(allocations or {}, free_skills or [])
    return b.build()


def make_hajje_mage(allocations=None, free_skills=None):
    b = CharacterBuilder()
    b.set_species("hajje")
    b.set_class("mage")
    b.set_origin("crewmate")
    b.set_background("scholarly")
    b.set_flavor("he", "orphan")
    # Hájje + Mage both grant Arcana → 1 redirect free-skill pick required
    resolved_free = free_skills if free_skills is not None else ["Diplomacy"] * b.pending_free_skills
    b.allocate_free_points(allocations or {}, free_skills=resolved_free)
    return b.build()


def make_human_warrior(allocations=None, free_skills=None):
    b = CharacterBuilder()
    b.set_species("human", attr_choices=["STR", "END"], skill_choice="Seamanship")
    b.set_class("warrior")
    b.set_origin("immigrant")
    b.set_background("hard_years")
    b.set_flavor("they", "single_parent")
    b.allocate_free_points(allocations or {}, free_skills or [])
    return b.build()


# ---------------------------------------------------------------------------
# Attribute bumps
# ---------------------------------------------------------------------------

def test_elf_warrior_attr_bumps():
    state = make_elf_warrior()
    # Elf: DEX+1, CHA+1; Warrior: STR+1
    assert state.attributes["STR"] == ATTR_BASE + 1
    assert state.attributes["DEX"] == ATTR_BASE + 1
    assert state.attributes["CHA"] == ATTR_BASE + 1
    # Others unchanged
    assert state.attributes["INT"] == ATTR_BASE
    assert state.attributes["SPR"] == ATTR_BASE
    assert state.attributes["END"] == ATTR_BASE


def test_hajje_mage_attr_bumps():
    state = make_hajje_mage()
    # Hájje: SPR+1, DEX+1; Mage: SPR+1 → SPR gets +2 total
    assert state.attributes["SPR"] == ATTR_BASE + 2
    assert state.attributes["DEX"] == ATTR_BASE + 1


def test_human_warrior_attr_choices():
    state = make_human_warrior()
    # Human: STR+1, END+1; Warrior: STR+1 → STR gets +2
    assert state.attributes["STR"] == ATTR_BASE + 2
    assert state.attributes["END"] == ATTR_BASE + 1


# ---------------------------------------------------------------------------
# Skill grants
# ---------------------------------------------------------------------------

def test_elf_warrior_skills():
    state = make_elf_warrior()
    # Elf → Survival; Warrior → Athletics; Merchant → Appraisal
    assert state.skills.get("Survival") == 1
    assert state.skills.get("Athletics") == 1
    assert state.skills.get("Appraisal") == 1


def test_hajje_mage_skills():
    state = make_hajje_mage()
    # Hájje → Arcana; Mage → Arcana (overlap!); Crewmate → Seamanship
    # Overlap → redirect: one pending free skill used. crewmate gives Seamanship.
    assert state.skills.get("Arcana") == 1
    assert state.skills.get("Seamanship") == 1


def test_hajje_mage_overlap_redirect():
    """Hájje + Mage both grant Arcana → one pending_free_skills."""
    b = CharacterBuilder()
    b.set_species("hajje")
    b.set_class("mage")
    assert b.pending_free_skills == 1


def test_overlap_redirect_free_skill_applied():
    b = CharacterBuilder()
    b.set_species("hajje")
    b.set_class("mage")
    b.set_origin("crewmate")
    b.set_background("scholarly")
    b.set_flavor("she", "two_parents")
    b.allocate_free_points({}, free_skills=["Diplomacy"])
    state = b.build()
    assert state.skills.get("Diplomacy") == 1


def test_overlap_redirect_raises_without_free_skill():
    b = CharacterBuilder()
    b.set_species("hajje")
    b.set_class("mage")
    b.set_origin("crewmate")
    b.set_background("scholarly")
    b.set_flavor("she", "two_parents")
    with pytest.raises(CreationError, match="free skill"):
        b.allocate_free_points({})    # no free_skills provided


def test_immigrant_origin_grants_arcana():
    state = make_human_warrior.__wrapped__ if hasattr(make_human_warrior, "__wrapped__") else None
    b = CharacterBuilder()
    b.set_species("human", attr_choices=["INT", "CHA"], skill_choice="Diplomacy")
    b.set_class("mage")
    b.set_origin("immigrant")
    b.set_background("scholarly")
    b.set_flavor("she", "two_parents")
    # Mage → Arcana; Immigrant → Arcana; overlap redirect
    assert b.pending_free_skills == 1
    b.allocate_free_points({}, free_skills=["Athletics"])
    state = b.build()
    assert state.skills.get("Arcana") == 1
    assert state.skills.get("Athletics") == 1


# ---------------------------------------------------------------------------
# Free-point allocation validation
# ---------------------------------------------------------------------------

def test_free_points_cap_per_attr():
    b = CharacterBuilder()
    b.set_species("elf")
    b.set_class("warrior")
    b.set_origin("merchant")
    b.set_background("sea_life")
    b.set_flavor("she", "two_parents")
    with pytest.raises(CreationError, match="more than"):
        b.allocate_free_points({"STR": FREE_POINT_MAX_PER_ATTR + 1})


def test_free_points_pool_exceeded():
    b = CharacterBuilder()
    b.set_species("elf")
    b.set_class("warrior")
    b.set_origin("merchant")
    b.set_background("sea_life")
    b.set_flavor("she", "two_parents")
    with pytest.raises(CreationError, match="exceeds pool"):
        b.allocate_free_points({"STR": 2, "DEX": 2, "INT": 2, "CHA": 2})


def test_free_points_applied_correctly():
    state = make_elf_warrior(allocations={"STR": 2, "INT": 1})
    assert state.attributes["STR"] == ATTR_BASE + 1 + 2   # racial+class bump + free
    assert state.attributes["INT"] == ATTR_BASE + 1


# ---------------------------------------------------------------------------
# Traits
# ---------------------------------------------------------------------------

def test_sea_life_background_grants_brine_in_blood():
    state = make_elf_warrior()
    assert "brine_in_blood" in state.traits


def test_scholarly_background_grants_deep_read():
    state = make_hajje_mage()
    assert "deep_read" in state.traits


def test_hard_years_background_grants_hard_years_trait():
    state = make_human_warrior()
    assert "hard_years" in state.traits


# ---------------------------------------------------------------------------
# Creation flags
# ---------------------------------------------------------------------------

def test_creation_flags_set_for_elf_warrior():
    state = make_elf_warrior()
    assert "species:elf" in state.flags
    assert "class:warrior" in state.flags
    assert "origin:merchant" in state.flags
    assert "background:sea_life" in state.flags
    assert "upbringing:two_parents" in state.flags


def test_creation_flags_set_for_hajje_mage():
    state = make_hajje_mage()
    assert "species:hajje" in state.flags
    assert "class:mage" in state.flags
    assert "origin:crewmate" in state.flags
    assert "background:scholarly" in state.flags


def test_origin_gate_flag_set():
    """Gate-reaction flag from origin must be set — this is the §6 DoD payoff."""
    state = make_elf_warrior()          # origin=merchant
    assert "origin:merchant" in state.flags


# ---------------------------------------------------------------------------
# Missing step raises CreationError
# ---------------------------------------------------------------------------

def test_build_raises_if_species_missing():
    b = CharacterBuilder()
    b.set_class("warrior")
    b.set_origin("merchant")
    b.set_background("sea_life")
    b.set_flavor("she", "two_parents")
    b.allocate_free_points({})
    with pytest.raises(CreationError, match="species"):
        b.build()


# ---------------------------------------------------------------------------
# Data integrity
# ---------------------------------------------------------------------------

def test_all_species_have_required_keys():
    from data.species import SPECIES
    for sid, spec in SPECIES.items():
        assert "attr_bumps" in spec, sid
        assert "skill_grants" in spec, sid


def test_all_classes_have_required_keys():
    from data.classes import CLASSES
    for cid, cls in CLASSES.items():
        assert "attr_bump" in cls, cid
        assert "skill_grant" in cls, cid


def test_all_origins_have_required_keys():
    from data.origins import ORIGINS
    for oid, orig in ORIGINS.items():
        assert "skill_grant" in orig, oid
        assert "gate_flag" in orig, oid


def test_all_backgrounds_reference_valid_traits():
    from data.backgrounds import BACKGROUNDS
    from data.traits import TRAITS
    for bid, bg in BACKGROUNDS.items():
        tid = bg["trait_id"]
        assert tid in TRAITS, f"Background {bid!r} references unknown trait {tid!r}"
