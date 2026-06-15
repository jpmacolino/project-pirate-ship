"""Tests for game/systems/creation.py and game/data/ content (§5.12, §7.5)."""
import pytest

from systems.creation import CharacterBuilder, CreationError
from systems.mechanics import ALL_SKILLS, ATTRIBUTES, ATTR_BASE, FREE_POINT_POOL, FREE_POINT_MAX_PER_ATTR


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


# ---------------------------------------------------------------------------
# Multi-slot free-pick (§5.12 redirect rule generics) — the fix target
# ---------------------------------------------------------------------------

def test_hajje_mage_immigrant_double_overlap():
    """All three sources grant Arcana → pending_free_skills must be 2, not 1."""
    b = CharacterBuilder()
    b.set_species("hajje")      # Arcana
    b.set_class("mage")         # Arcana → overlap 1
    b.set_origin("immigrant")   # Arcana → overlap 2
    assert b.pending_free_skills == 2


def test_double_overlap_both_slots_fillable():
    """With pending_free_skills==2 both picks apply and the final sheet has no dupes."""
    b = CharacterBuilder()
    b.set_species("hajje")
    b.set_class("mage")
    b.set_origin("immigrant")
    b.set_background("scholarly")
    b.set_flavor("she", "two_parents")
    b.allocate_free_points({}, free_skills=["Diplomacy", "Endurance"])
    state = b.build()
    assert state.skills.get("Arcana") == 1
    assert state.skills.get("Diplomacy") == 1
    assert state.skills.get("Endurance") == 1
    # no duplicates — every key is unique in a dict, so count == len of unique values
    assert len(state.skills) == len(set(state.skills))


def test_double_overlap_expected_total_skills():
    """Hájje+Mage+Immigrant: 1 fixed grant (Arcana) + 2 free picks = 3 total skills."""
    b = CharacterBuilder()
    b.set_species("hajje")
    b.set_class("mage")
    b.set_origin("immigrant")
    b.set_background("scholarly")
    b.set_flavor("she", "two_parents")
    b.allocate_free_points({}, free_skills=["Survival", "Athletics"])
    state = b.build()
    assert len(state.skills) == 3


def test_free_skill_cannot_duplicate_fixed_grant():
    """Picking a skill already granted by species/class/origin must raise."""
    b = CharacterBuilder()
    b.set_species("hajje")      # Arcana
    b.set_class("mage")         # Arcana → overlap → pending=1
    b.set_origin("crewmate")    # Seamanship
    b.set_background("scholarly")
    b.set_flavor("she", "two_parents")
    with pytest.raises(CreationError, match="duplicates a fixed grant"):
        b.allocate_free_points({}, free_skills=["Arcana"])


def test_free_skill_cannot_pick_same_skill_twice():
    """Two picks of the same free skill must raise even if that skill isn't a fixed grant."""
    b = CharacterBuilder()
    b.set_species("hajje")
    b.set_class("mage")
    b.set_origin("immigrant")   # pending_free_skills = 2
    b.set_background("scholarly")
    b.set_flavor("she", "two_parents")
    with pytest.raises(CreationError, match="chosen more than once"):
        b.allocate_free_points({}, free_skills=["Diplomacy", "Diplomacy"])


def test_free_skill_options_excludes_granted_and_prior_picks():
    """free_skill_options filters out fixed grants AND any skills already chosen."""
    b = CharacterBuilder()
    b.set_species("hajje")      # Arcana
    b.set_class("mage")         # Arcana overlap
    b.set_origin("crewmate")    # Seamanship
    options_first = b.free_skill_options()
    assert "Arcana" not in options_first
    assert "Seamanship" not in options_first
    assert "Diplomacy" in options_first

    # Simulate having already chosen Diplomacy on the first pick
    options_second = b.free_skill_options(already_chosen=["Diplomacy"])
    assert "Arcana" not in options_second
    assert "Seamanship" not in options_second
    assert "Diplomacy" not in options_second   # excluded because already chosen
    assert "Endurance" in options_second


def test_free_skill_options_all_skills_in_pool():
    """free_skill_options returns a subset of ALL_SKILLS."""
    b = CharacterBuilder()
    b.set_species("elf")
    b.set_class("warrior")
    b.set_origin("merchant")
    for sk in b.free_skill_options():
        assert sk in ALL_SKILLS


def test_non_overlapping_combo_no_free_picks_needed():
    """Elf+Warrior+Merchant: no overlaps → pending_free_skills==0, empty free list OK."""
    b = CharacterBuilder()
    b.set_species("elf")        # Survival
    b.set_class("warrior")      # Athletics
    b.set_origin("merchant")    # Appraisal
    assert b.pending_free_skills == 0
    b.set_background("sea_life")
    b.set_flavor("she", "two_parents")
    b.allocate_free_points({})  # no free_skills argument
    state = b.build()
    assert state.skills.get("Survival") == 1
    assert state.skills.get("Athletics") == 1
    assert state.skills.get("Appraisal") == 1


# ---------------------------------------------------------------------------
# §7.13(b) invariant: player receives every choice the data promises
# ---------------------------------------------------------------------------

def test_species_choice_needs_human():
    """Human must report both attr and skill choices required."""
    needs = CharacterBuilder.species_choice_needs("human")
    assert needs["needs_attr_choice"] is True
    assert needs["needs_skill_choice"] is True


def test_species_choice_needs_fixed_species():
    """Fixed species (elf, hajje) must report no choices required."""
    for sid in ("elf", "hajje"):
        needs = CharacterBuilder.species_choice_needs(sid)
        assert needs["needs_attr_choice"] is False, sid
        assert needs["needs_skill_choice"] is False, sid


def test_species_choice_needs_matches_data_sentinels():
    """Choice-needs must be driven by choose_* sentinels in species data, not species name."""
    from data.species import SPECIES
    for sid, spec in SPECIES.items():
        needs = CharacterBuilder.species_choice_needs(sid)
        assert needs["needs_attr_choice"] == (spec["attr_bumps"] == "choose_two"), sid
        assert needs["needs_skill_choice"] == (spec["skill_grants"] == "choose_one"), sid


def test_human_set_species_raises_without_attr_choices():
    """Missing attr_choices for human must raise immediately — no silent default."""
    b = CharacterBuilder()
    with pytest.raises(CreationError):
        b.set_species("human")


def test_human_set_species_raises_without_skill_choice():
    """Missing skill_choice for human must raise immediately — no silent default."""
    b = CharacterBuilder()
    with pytest.raises(CreationError, match="skill_choice"):
        b.set_species("human", attr_choices=["STR", "DEX"])


def test_human_set_species_rejects_duplicate_attrs():
    """Human cannot pick the same attribute twice."""
    b = CharacterBuilder()
    with pytest.raises(CreationError, match="distinct"):
        b.set_species("human", attr_choices=["STR", "STR"], skill_choice="Diplomacy")


def test_human_both_attr_choices_applied():
    """Both human attr picks get +1 on the final sheet."""
    b = CharacterBuilder()
    b.set_species("human", attr_choices=["INT", "CHA"], skill_choice="Seamanship")
    b.set_class("mage")        # SPR+1, Arcana
    b.set_origin("merchant")   # Appraisal
    b.set_background("hard_years")
    b.set_flavor("she", "two_parents")
    b.allocate_free_points({})
    state = b.build()
    assert state.attributes["INT"] == ATTR_BASE + 1, "first attr choice not applied"
    assert state.attributes["CHA"] == ATTR_BASE + 1, "second attr choice not applied"
    # Sanity: mage's own bump (SPR) is untouched by human picks
    assert state.attributes["SPR"] == ATTR_BASE + 1


def test_human_skill_choice_granted_directly():
    """Non-overlapping human skill choice must appear in final skills."""
    b = CharacterBuilder()
    b.set_species("human", attr_choices=["STR", "DEX"], skill_choice="Diplomacy")
    b.set_class("warrior")     # Athletics, STR
    b.set_origin("merchant")   # Appraisal
    b.set_background("sea_life")
    b.set_flavor("he", "two_parents")
    b.allocate_free_points({})
    state = b.build()
    assert state.skills.get("Diplomacy") == 1, "non-overlapping skill choice silently dropped"


def test_human_skill_choice_overlap_redirects_not_drops():
    """Overlapping human skill choice must redirect (pending +1) — not silently drop."""
    b = CharacterBuilder()
    b.set_species("human", attr_choices=["STR", "END"], skill_choice="Athletics")
    b.set_class("warrior")     # Athletics → overlap with human's skill_choice
    assert b.pending_free_skills == 1, "skill choice overlap was silently dropped instead of redirected"
    b.set_origin("merchant")   # Appraisal
    b.set_background("hard_years")
    b.set_flavor("she", "two_parents")
    b.allocate_free_points({}, free_skills=["Diplomacy"])
    state = b.build()
    assert state.skills.get("Athletics") == 1   # still present (from first grant)
    assert state.skills.get("Diplomacy") == 1   # redirect pick applied
