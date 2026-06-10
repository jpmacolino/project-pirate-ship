"""Species definitions (§5.1, §5.12).

Each entry drives CharacterBuilder.set_species().

attr_bumps:   dict {attr: +delta} | "choose_two" (Human).
skill_grants: list of skill IDs  | "choose_one" (Human).

§5.12 design:
  Elf   → DEX+1, CHA+1 / Survival
  Hájje → SPR+1, DEX+1 / Arcana
  Human → player picks 2 attrs / player picks 1 skill

Lore note: Hájje appearance (pale-skinned, black hair, black eyes) is in
the lore bible §Species; the builder records only the mechanical identity.
"""

SPECIES: dict[str, dict] = {
    "elf": {
        "display_name": "Elf",
        "attr_bumps": {"DEX": 1, "CHA": 1},
        "skill_grants": ["Survival"],
        "description": (
            "Sea-faring southern elves of Tethryn — long-lived, graceful, and at home "
            "on the water. Their centuries of maritime tradition show in quiet confidence."
        ),
    },
    "hajje": {
        "display_name": "Hájje",
        "attr_bumps": {"SPR": 1, "DEX": 1},
        "skill_grants": ["Arcana"],
        "description": (
            "A people of feared heritage who long ago fled that legacy and settled inland. "
            "They carry deep spiritual awareness—and a weight others rarely let them forget."
        ),
    },
    "human": {
        "display_name": "Human",
        "attr_bumps": "choose_two",       # player picks at chargen
        "skill_grants": "choose_one",     # player picks at chargen
        "description": (
            "Widespread and adaptable, humans are the world's most flexible people. "
            "No single tradition defines them; what they are is what they chose to be."
        ),
    },
}
