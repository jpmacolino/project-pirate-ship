"""Trait registry (§5.12, §5.10).

Traits toggle advantage/disadvantage (the advantage axis — §5.10).
They are intentionally asymmetric across species/classes/backgrounds.

Each trait entry:
  id:           canonical ID used in GameState.traits and has_flag checks.
  display_name: shown to the player on the character sheet.
  description:  one sentence for the confirm screen.
  payoff:       where the trait triggers in the MVP slice (for design audit).

Brine in Blood is the canonical MVP advantage demo (§5.12).
"""

TRAITS: dict[str, dict] = {
    "brine_in_blood": {
        "id": "brine_in_blood",
        "display_name": "Brine in Blood",
        "description": "Advantage on sea- and boat-related tasks.",
        "payoff": "beach debris search (sea-wrack), road coastal travel",
    },
    "hard_years": {
        "id": "hard_years",
        "display_name": "Hard Years",
        "description": "Advantage on Endurance checks; hardship is no surprise to you.",
        "payoff": "road endurance beat",
    },
    "deep_read": {
        "id": "deep_read",
        "display_name": "Deep Read",
        "description": "Advantage on Investigation and Arcana when puzzling out unknown workings.",
        "payoff": "beach thorough search; arcane anomaly read",
    },
}
