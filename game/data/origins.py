"""Origin definitions (§5.12).

Each entry drives CharacterBuilder.set_origin().

skill_grant: skill trained at creation.
gate_flag:   story flag consumed at the camp threshold for reactive dialogue.
             This is the §6 DoD payoff: at least one creation flag alters a branch.
"""

ORIGINS: dict[str, dict] = {
    "merchant": {
        "display_name": "Merchant",
        "skill_grant": "Appraisal",
        "gate_flag": "origin:merchant",
        "description": (
            "You were aboard on business — goods, debts, a contract. "
            "You know how to read value in a room, and how to present yourself as worth dealing with."
        ),
    },
    "crewmate": {
        "display_name": "Ship's Crew",
        "skill_grant": "Seamanship",
        "gate_flag": "origin:crewmate",
        "description": (
            "This was your ship — or close enough. You know every line and timber "
            "of a vessel like this one. The sea is not strange to you."
        ),
    },
    "immigrant": {
        "display_name": "Immigrant from Erathal",
        "skill_grant": "Arcana",
        "gate_flag": "origin:immigrant",
        "description": (
            "You were crossing from Erathal, looking for a new start in the south. "
            "An outsider twice over: from the north, and now washed up on an island "
            "that wasn't even your destination."
        ),
    },
}
