## Evorath — Beach scene (§5.3, §5.8, §5.9)
## Wake → diegetic chargen → debris search → road

label beach_wake:
    scene bg_beach_wreck
    with dissolve

    ## Opening narration — late Frozga, north shore of Tethryn, early morning
    "You don't remember falling."
    "You remember the ship — the crack of something vast, the tilting deck, the cold water rushing up —"
    "And then nothing."
    "Now: sand under your hands. Salt on your lips. The pale winter sun barely above the water."
    "The sea smells wrong — scorched, underneath the brine."
    "Behind you, wreckage."

    with Pause(0.5)

    ## Diegetic character creation
    $ builder = CharacterBuilder()
    call chargen_start

    ## After chargen, brief reorientation
    "You are standing on the north shore of some island."
    "The wreck is behind you — or rather, scattered around you."
    "Nothing is on fire any more. That happened while you were unconscious."
    "There is a coastal path leading east. Somewhere inland, smoke from a fire."
    "But first — the wreck."

    ## ── DEBRIS SEARCH ─────────────────────────────────────────────────────────

    "What's left of the hull is beached thirty yards away. Most of it is underwater."
    "The tide has brought things in."

    menu:
        "Search thoroughly — you have time and you need to know what happened.":
            $ _search_thorough = True
        "Grab what you need and go — someone must have seen the wreck.":
            $ _search_thorough = False

    ## Build advantage sources for the Investigation check
    python:
        _search_adv = []
        if has_flag("background:sea_life"):
            _search_adv.append(("Brine in Blood", 1))
        if has_flag("background:scholarly") and _search_thorough:
            _search_adv.append(("Deep Read", 1))

    ## The core beach Investigation check
    if _search_thorough:
        "You work methodically through the debris — planking, rigging, cargo that has come ashore."
        $ _beach_dc = 14
    else:
        "You sweep quickly, taking what's obvious."
        $ _beach_dc = 10

    $ _beach_cr = check("INT", "Investigation", _beach_dc, adv_sources=_search_adv)
    call screen dice_result(_beach_cr)

    ## ── RESULT BRANCHES ────────────────────────────────────────────────────────

    if _beach_cr.nat1:
        ## Nat-1: fumble — barely anything
        "You stumble across the uneven sand, slip on wet timber."
        "By the time you recover your footing, the tide has pulled things back."
        "You manage a length of rope. That's all."
        $ add_item("rope_coil")
        "Not merfolk-attacked so much as just... unlucky."

    elif _beach_cr.passed or _beach_cr.nat20:
        ## Pass or nat-20: standard finds
        "A waterlogged pack — the wax-canvas inner pocket held. Dried rations and a waterskin."
        "A ship's knife, salt-pitted but sound."
        $ add_item("waterlogged_pack")
        $ add_item("salvage_knife")
        $ add_item("rope_coil")

        "The hull shows signs of violent impact — something hit this ship hard."
        "Not a reef. Not a sandbar. Impact from above the waterline, directed."
        "The old dread settles like ballast in the stomach of every coastal soul: merfolk."
        $ set_flag("found_merfolk_evidence")

        if _beach_cr.nat20:
            "Near the stern — an officer's compass in a sealed leather case. Still true."
            $ add_item("officers_compass")
            "You were here. You survived. Maybe that's worth something."

        ## ── THOROUGH SEARCH: the anomalous detail ─────────────────────────────
        if _search_thorough and (_beach_cr.passed and _beach_cr.total >= 14 or _beach_cr.nat20):
            "But here — deeper in the wreck, where the force was strongest —"
            "Something doesn't fit."
            "A piece of the hull, warped in a way no sea-creature causes. Bent inward, fused."
            "And embedded in the timber, a fragment: metal, warped at one end as though by tremendous directed heat."
            "Not a tooth. Not a claw. A made thing."
            $ add_item("device_fragment")
            $ set_flag("found_anomaly")

            "You hold it for a moment. It is cold. It tells you nothing except: this was not a creature."

            ## ── CLASS LENS (if anomaly found) ─────────────────────────────────
            if has_flag("class:warrior"):
                "Your fighter's eye fills in the rest: the angle, the force, the single point of origin."
                "Whatever struck this ship didn't circle it. Didn't harry it. Struck once, precisely, at the waterline."
                "Sea-creatures don't do that."
                $ set_flag("read_impact_pattern")

            elif has_flag("class:mage"):
                "Your arcane sense nags at you like a splinter."
                "There is residue here — destructive arcana, burned into the timber."
                "You know what merfolk magic feels like, or you know the stories: illusion, compulsion — the mind-magic of the deep war."
                "This is not that. The signature is unfamiliar. Wrong school. Wrong texture entirely."
                $ set_flag("read_arcane_signature")

    else:
        ## Failed non-nat-1: finds basics but misses the anomaly
        "You find a rope and a waterlogged pack — enough to matter."
        "The wreck looks like every other ship that came to grief near a coastline."
        "Merfolk, probably. People will say merfolk."
        $ add_item("rope_coil")
        $ add_item("waterlogged_pack")
        $ set_flag("found_merfolk_evidence")

    ## ── TRANSITION TO ROAD ────────────────────────────────────────────────────

    "You stand on the beach for a moment, looking east."
    "The coastal path is clear. The smoke inland has settled into something more deliberate — a camp fire."
    "Wherever you are, someone lives here. And you need shelter, water, answers."

    jump road
