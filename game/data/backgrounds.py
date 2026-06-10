"""Adult-background question (§5.12 / §7.12).

The fourth creation step: "Before the voyage, what had your life been?"
Each option grants exactly one trait that pays off in the beach→road→gate slice.

trait_id must exist in game/data/traits.TRAITS.
The creation flag background:<bg_id> is consumed in the narrative.
"""

BACKGROUNDS: dict[str, dict] = {
    "sea_life": {
        "display_name": "Life at Sea",
        "choice_text": "Life at sea — dockwork, fishing, crewing, the salt in everything.",
        "trait_id": "brine_in_blood",
        "description": (
            "You know the smell of tar and brine better than any hearth-fire. "
            "The sea is not a stranger — it is where you have always lived."
        ),
    },
    "hard_years": {
        "display_name": "Hard Years",
        "choice_text": "Hard years — struggle, scarcity, surviving things that should have broken you.",
        "trait_id": "hard_years",
        "description": (
            "You have been hungry, cold, afraid — and here you still are. "
            "Hardship has made you dense as iron."
        ),
    },
    "scholarly": {
        "display_name": "Books and Study",
        "choice_text": "Books and study — libraries, apprenticeship, the quiet thrill of understanding.",
        "trait_id": "deep_read",
        "description": (
            "The world is a problem that rewards careful attention. "
            "You have always found more in a room than most people notice."
        ),
    },
}
