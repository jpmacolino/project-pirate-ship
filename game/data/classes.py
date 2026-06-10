"""Class definitions (§5.1, §5.12, §5.9).

Each entry drives CharacterBuilder.set_class().

attr_bump:   single attribute raised by +1.
skill_grant: single skill trained at creation.
lens_flag:   flag set when the class-lens debris read triggers (consumed in beach.rpy).
"""

CLASSES: dict[str, dict] = {
    "warrior": {
        "display_name": "Warrior",
        "attr_bump": "STR",
        "skill_grant": "Athletics",
        "lens_flag": "class:warrior",
        "lens_description": (
            "Martial eye — you read impact patterns no sea-creature leaves. "
            "The wreckage speaks a language of force, angle, and intention."
        ),
        "description": (
            "A fighter, a guard, a soldier — someone whose body is their first tool. "
            "You read the world through weight, momentum, and threat."
        ),
    },
    "mage": {
        "display_name": "Mage",
        "attr_bump": "SPR",
        "skill_grant": "Arcana",
        "lens_flag": "class:mage",
        "lens_description": (
            "Arcane sense — you feel the residue of a working in the wreck's timbers. "
            "Not merfolk mind-magic; something else, and unfamiliar."
        ),
        "description": (
            "A student of the arcane — whether self-taught or schooled. "
            "You see the invisible seams where magic has touched the world."
        ),
    },
}
