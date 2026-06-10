## Evorath — Road beat (§5.4)
## Wreck → path east along the north shore → camp threshold.
## The sea is to the left; the wreck's headland drops behind.
## Background continuity note (§5.4): player explicitly turns east here,
## making the scene transition from bg_beach_wreck to bg_coast_path coherent.

label road:
    scene bg_coast_path
    with dissolve

    "You turn east."
    "The sea is immediately to your left — close enough to hear the surf over the sand and shingle."
    "Behind you, the wreck's headland drops away. Ahead, the coast curves gently."
    "The path is real but rough: exposed rock, tide-dragged weed, sand that slides underfoot."
    "Winter light. The air is warmer than it has any right to be — this is the south, even in Frozga."

    "Somewhere ahead, perhaps half an hour's walk, you can see the line of the camp."
    "Small shapes — dark against the pale sand — that might be boats, tents, drying racks."

    ## ── ROAD ENDURANCE BEAT ────────────────────────────────────────────────────

    "The path turns rocky where the coast juts out."
    "The wind off the water picks up. Your wet clothes don't help."

    ## Build advantage sources for the Endurance check
    python:
        _road_adv = []
        if has_flag("background:hard_years"):
            _road_adv.append(("Hard Years", 1))
        if has_flag("origin:crewmate"):
            _road_adv.append(("Sea legs — rough ground is no stranger", 1))

    $ _road_cr = check("END", "Endurance", 10, adv_sources=_road_adv)
    call screen dice_result(_road_cr)

    if _road_cr.nat20:
        "The walk that should tire you barely registers."
        "You arrive at the camp edge moving easily, shoulders back, still taking in the landscape."
        "Whatever hardship has shaped you, it left you with iron in the legs."
        $ set_flag("road_endurance_ok")

    elif _road_cr.passed:
        "You pick your way through without slipping, settling into the rhythm of the coast."
        "By the time the camp comes into view you are breathing easily."
        $ set_flag("road_endurance_ok")

    elif _road_cr.nat1:
        "You slip on the wet rock and go down hard on one knee."
        "It doesn't break anything, but the fall rattles you. You arrive at the camp limping slightly."
        "Of all the ways to arrive."

    else:
        "The ground gives you trouble — slick rock, hidden hollows, the wind in your face."
        "You arrive at the camp's edge wind-bitten and tired, but you arrive."

    ## ── TRANSITION ────────────────────────────────────────────────────────────

    "The camp is real."
    "A dozen-odd tents in muted canvas, sea-weathered. Drying racks heavy with fish and net."
    "Boats beached above the tide line — small, deep-keeled, built for these waters."
    "Warding-stakes at the waterward edge: carved stakes and small sea-charms facing the surf."
    "Old habit. Old fear."
    "You've heard of the merfolk war. This community lived it."

    jump camp_threshold
