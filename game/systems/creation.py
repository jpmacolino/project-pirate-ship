"""Character-builder logic (§5.2, §5.12).

Accumulates creation choices and resolves them into a final GameState.
Data (species/class/origin definitions) lives in game/data/; this module
is engine-only — never touch the data registries from here.

Workflow:
    builder = CharacterBuilder()
    builder.set_species(species_id, attr_choices=None, skill_choice=None)
    builder.set_class(class_id)
    builder.set_origin(origin_id)
    builder.set_background(bg_id)
    builder.set_flavor(sex, upbringing, name)
    builder.allocate_free_points({attr: delta, ...}, free_skills=[...])
    state = builder.build()

Open question §7.5 residual — overlap rule RESOLVED: redirect.
When two sources grant the same skill the duplicate becomes a free-pick
recorded in self.pending_free_skills.  The confirm screen resolves it via
allocate_free_points(free_skills=[...]).
"""
from __future__ import annotations

from .mechanics import (
    ALL_SKILLS,
    ATTR_BASE, ATTR_CAP, ATTRIBUTES,
    FREE_POINT_POOL, FREE_POINT_MAX_PER_ATTR,
    SKILL_TRAINED, GameState, set_flag,
)


class CreationError(ValueError):
    """Raised for invalid builder state or constraint violations."""


class CharacterBuilder:
    """Accumulates creation choices; call build() to get the final GameState."""

    def __init__(self) -> None:
        self._state = GameState()
        # Raw attr bumps accumulated before build()
        self._attr_bumps: dict[str, int] = {}
        # Skills granted (name -> source label)
        self._granted_skills: dict[str, str] = {}
        # Trait IDs granted
        self._granted_traits: list[str] = []
        # Flags to set on build
        self._creation_flags: list[str] = []
        # Pending free skill picks from overlap redirects
        self.pending_free_skills: int = 0
        # Tracking which steps are done (for validation)
        self._steps_done: set[str] = set()
        # Stored free-point allocations (applied at build)
        self._free_alloc: dict[str, int] = {}
        self._free_skill_picks: list[str] = []

    # ------------------------------------------------------------------
    # Step 1 — species
    # ------------------------------------------------------------------

    def set_species(
        self,
        species_id: str,
        attr_choices: list[str] | None = None,
        skill_choice: str | None = None,
    ) -> "CharacterBuilder":
        """Apply species definition.

        attr_choices: required for human (list of 2 attribute names).
        skill_choice: required for human (skill name).
        """
        from game.data.species import SPECIES  # late import — data, not engine

        spec = SPECIES.get(species_id)
        if spec is None:
            raise CreationError(f"Unknown species: {species_id!r}")

        self._state.species = species_id
        self._creation_flags.append(f"species:{species_id}")

        # Attribute bumps
        bumps = spec["attr_bumps"]
        if bumps == "choose_two":
            if not attr_choices or len(attr_choices) != 2:
                raise CreationError("Human species requires exactly 2 attr_choices")
            if attr_choices[0] == attr_choices[1]:
                raise CreationError("Human species attr_choices must be two distinct attributes")
            for a in attr_choices:
                if a not in ATTRIBUTES:
                    raise CreationError(f"Unknown attribute: {a!r}")
            for a in attr_choices:
                self._attr_bumps[a] = self._attr_bumps.get(a, 0) + 1
        else:
            for attr, val in bumps.items():
                self._attr_bumps[attr] = self._attr_bumps.get(attr, 0) + val

        # Skill grants
        raw_grants = spec["skill_grants"]
        if raw_grants == "choose_one":
            if not skill_choice:
                raise CreationError("Human species requires a skill_choice")
            self._grant_skill(skill_choice, f"species:{species_id}")
        else:
            for sk in raw_grants:
                self._grant_skill(sk, f"species:{species_id}")

        self._steps_done.add("species")
        return self

    # ------------------------------------------------------------------
    # Step 2 — class
    # ------------------------------------------------------------------

    def set_class(self, class_id: str) -> "CharacterBuilder":
        from game.data.classes import CLASSES

        cls = CLASSES.get(class_id)
        if cls is None:
            raise CreationError(f"Unknown class: {class_id!r}")

        self._state.class_ = class_id
        self._creation_flags.append(f"class:{class_id}")

        # Class attr bump
        attr = cls["attr_bump"]
        self._attr_bumps[attr] = self._attr_bumps.get(attr, 0) + 1

        # Class skill grant
        self._grant_skill(cls["skill_grant"], f"class:{class_id}")

        self._steps_done.add("class")
        return self

    # ------------------------------------------------------------------
    # Step 3 — origin
    # ------------------------------------------------------------------

    def set_origin(self, origin_id: str) -> "CharacterBuilder":
        from game.data.origins import ORIGINS

        orig = ORIGINS.get(origin_id)
        if orig is None:
            raise CreationError(f"Unknown origin: {origin_id!r}")

        self._state.origin = origin_id
        self._creation_flags.append(f"origin:{origin_id}")

        self._grant_skill(orig["skill_grant"], f"origin:{origin_id}")

        # Gate-reaction flag
        self._creation_flags.append(orig["gate_flag"])

        self._steps_done.add("origin")
        return self

    # ------------------------------------------------------------------
    # Step 4 — adult background / trait
    # ------------------------------------------------------------------

    def set_background(self, bg_id: str) -> "CharacterBuilder":
        from game.data.backgrounds import BACKGROUNDS

        bg = BACKGROUNDS.get(bg_id)
        if bg is None:
            raise CreationError(f"Unknown background: {bg_id!r}")

        self._state.background_id = bg_id
        self._creation_flags.append(f"background:{bg_id}")

        trait_id = bg["trait_id"]
        if trait_id:
            self._granted_traits.append(trait_id)

        self._steps_done.add("background")
        return self

    # ------------------------------------------------------------------
    # Step 5 — flavor (sex, upbringing, name)
    # ------------------------------------------------------------------

    def set_flavor(self, sex: str, upbringing: str, name: str = "the survivor") -> "CharacterBuilder":
        self._state.sex = sex
        self._state.upbringing = upbringing
        self._state.name = name
        self._creation_flags.append(f"upbringing:{upbringing}")
        self._steps_done.add("flavor")
        return self

    # ------------------------------------------------------------------
    # Step 6 — confirm screen: allocate free points
    # ------------------------------------------------------------------

    def allocate_free_points(
        self,
        allocations: dict[str, int],
        free_skills: list[str] | None = None,
    ) -> "CharacterBuilder":
        """Validate and store free-point allocations (applied at build()).

        allocations: {attr_name: delta} — total <= FREE_POINT_POOL,
                     each delta <= FREE_POINT_MAX_PER_ATTR.
        free_skills:  skill picks for overlap redirects.
        """
        total = sum(allocations.values())
        if total > FREE_POINT_POOL:
            raise CreationError(
                f"Free-point total {total} exceeds pool of {FREE_POINT_POOL}"
            )
        for attr, delta in allocations.items():
            if attr not in ATTRIBUTES:
                raise CreationError(f"Unknown attribute in allocation: {attr!r}")
            if delta > FREE_POINT_MAX_PER_ATTR:
                raise CreationError(
                    f"Cannot put more than {FREE_POINT_MAX_PER_ATTR} free points "
                    f"into {attr!r} (tried {delta})"
                )
        fs = free_skills or []
        if len(fs) < self.pending_free_skills:
            raise CreationError(
                f"Need {self.pending_free_skills} free skill pick(s), got {len(fs)}"
            )
        seen: set[str] = set()
        for sk in fs:
            if sk in self._granted_skills:
                raise CreationError(
                    f"Free skill pick {sk!r} duplicates a fixed grant"
                )
            if sk in seen:
                raise CreationError(
                    f"Free skill pick {sk!r} chosen more than once"
                )
            seen.add(sk)
        self._free_alloc = dict(allocations)
        self._free_skill_picks = list(fs)
        self._steps_done.add("free_points")
        return self

    # ------------------------------------------------------------------
    # Preview (used by charsheet_confirm screen)
    # ------------------------------------------------------------------

    def preview(self) -> dict:
        """Return pre-free-point stats for the confirm screen display.

        Returns a dict with:
          attributes: {attr: current_value}  (base + bumps)
          skills:     {skill: rank}
          traits:     [trait_id, ...]
          pending_free_skills: int
        """
        attrs = {k: ATTR_BASE + self._attr_bumps.get(k, 0) for k in ATTRIBUTES}
        return {
            "attributes": attrs,
            "skills": dict(self._granted_skills),      # name -> source_label
            "traits": list(self._granted_traits),
            "pending_free_skills": self.pending_free_skills,
        }

    # ------------------------------------------------------------------
    # Final build
    # ------------------------------------------------------------------

    def build(self) -> GameState:
        """Resolve all accumulated choices into a final GameState."""
        required = {"species", "class", "origin", "background", "flavor"}
        missing = required - self._steps_done
        if missing:
            raise CreationError(f"Incomplete build — missing steps: {missing}")

        state = self._state

        # Apply attribute bumps (racial + class)
        for attr, delta in self._attr_bumps.items():
            state.attributes[attr] = min(
                ATTR_CAP, state.attributes.get(attr, ATTR_BASE) + delta
            )

        # Apply free-point allocations
        for attr, delta in self._free_alloc.items():
            state.attributes[attr] = min(
                ATTR_CAP, state.attributes.get(attr, ATTR_BASE) + delta
            )

        # Apply granted skills
        for sk in self._granted_skills:
            state.skills[sk] = SKILL_TRAINED

        # Apply free skill picks from overlap redirects
        for sk in self._free_skill_picks:
            state.skills[sk] = SKILL_TRAINED

        # Apply traits
        for trait_id in self._granted_traits:
            state.traits.add(trait_id)

        # Stamp all creation flags
        for flag in self._creation_flags:
            set_flag(state, flag)

        return state

    # ------------------------------------------------------------------
    # Query helpers (used by .rpy to build menus without touching internals)
    # ------------------------------------------------------------------

    def free_skill_options(self, already_chosen: list[str] | None = None) -> list[str]:
        """Return skills available for a free pick.

        Excludes skills already granted by species/class/origin and any skills
        already selected in earlier picks this session.
        """
        excluded = set(self._granted_skills) | set(already_chosen or [])
        return [s for s in ALL_SKILLS if s not in excluded]

    @staticmethod
    def species_choice_needs(species_id: str) -> dict:
        """What flexibility choices this species requires, driven by choose_* sentinels.

        Returns {"needs_attr_choice": bool, "needs_skill_choice": bool}.
        Called by narrative to determine whether to show the flexibility step;
        the sentinel values in species data, not the species name, drive the result.
        """
        from game.data.species import SPECIES
        spec = SPECIES.get(species_id)
        if spec is None:
            raise CreationError(f"Unknown species: {species_id!r}")
        return {
            "needs_attr_choice": spec["attr_bumps"] == "choose_two",
            "needs_skill_choice": spec["skill_grants"] == "choose_one",
        }

    @staticmethod
    def all_attributes() -> list[str]:
        """All valid attribute names, for populating choice UIs."""
        return list(ATTRIBUTES)

    @staticmethod
    def all_skills() -> list[str]:
        """All valid skill names, for populating choice UIs."""
        return list(ALL_SKILLS)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _grant_skill(self, skill: str, source: str) -> None:
        """Grant a skill; if already granted, redirect to a free pick."""
        if skill in self._granted_skills:
            self.pending_free_skills += 1
        else:
            self._granted_skills[skill] = source
