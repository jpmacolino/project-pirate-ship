## Evorath — diegetic character builder (§5.2, §5.12)
## "Light amnesia": identity resurfaces through the opening as fragments.
## Called from beach.rpy (beach_wake) via: call chargen_start

label chargen_start:
    ## builder is already set to CharacterBuilder() by beach_wake before this call.

    ## ── Fragment 1: SPECIES (looking at hands / reflection) ──────────────────

    "You push yourself upright."
    "Sand under your palms. Salt on your lips. The low winter sun over the water."
    "There is debris everywhere — timber, rope, a shattered crate, things that don't matter yet."
    "You reach for a shard of mirror-bright hull plating half-buried in the sand."
    "In it, something looks back. Your hands."

    ## Collect species identity. Fixed species (no choose_* sentinels) call
    ## set_species() immediately; species with choose_* sentinels defer to
    ## just before the confirm screen so the flexibility step feels like
    ## part of that weighted resolution moment.
    $ _species_id = None
    menu:
        "Long-fingered, with the faint luminance of elven skin. Your hair has come loose — pale gold or silver in the dawn light.":
            $ _species_id = "elf"
            "An elf. Thalvath-born, or so the feeling says."
            "That much comes back quickly."

        "Broad, weathered — a human's hands. Calloused from work you almost remember.":
            $ _species_id = "human"
            "Human hands. Practical. Nothing especially remarkable about them."
            "What you're made of comes back in pieces — not as a single thing, but as choices."

        "Dark-veined at the knuckles. Unnervingly still. Pale skin; black hair matted with seawater.":
            $ _species_id = "hajje"
            "Hájje. You have spent years learning what that means to people who don't know you."
            "Their fear is old, and inherited, and not yours to carry — but you carry it anyway."

    ## Check sentinels now so the deferred branch below can reuse the result.
    $ _species_needs = CharacterBuilder.species_choice_needs(_species_id)
    if not (_species_needs["needs_attr_choice"] or _species_needs["needs_skill_choice"]):
        $ builder.set_species(_species_id)

    ## ── Fragment 2: SEX ────────────────────────────────────────────────────────

    "The tide pulls at something near you. You let it go."
    "What do they call you — or rather, how do you think of yourself?"

    menu:
        "She / her.":
            python:
                pn_they = "she"; pn_them = "her"; pn_their = "her"
                pn_theyre = "she's"; pn_reflexive = "herself"
                player_state_sex = "female"
        "He / him.":
            python:
                pn_they = "he"; pn_them = "him"; pn_their = "his"
                pn_theyre = "he's"; pn_reflexive = "himself"
                player_state_sex = "male"
        "They / them.":
            python:
                pn_they = "they"; pn_them = "them"; pn_their = "their"
                pn_theyre = "they're"; pn_reflexive = "themselves"
                player_state_sex = "nonbinary"

    ## ── Fragment 3: CLASS (what knowledge surfaces first) ──────────────────────

    "You start to stand. Your body knows things your mind is still catching up to."
    "What comes back first — the kind of knowledge that lives in muscle and instinct?"

    menu:
        "Combat. Weight, leverage, threat — you see an angle before you know you're looking.":
            $ builder.set_class("warrior")
            "A fighter's eye. The wreck around you is already a problem you're solving."

        "Magic. There is a tremor in the air here, a wrongness you can almost name.":
            $ builder.set_class("mage")
            "A mage's awareness. The world has a texture most people can't feel. You feel it."

    ## ── Fragment 4: ORIGIN (why were you on that ship) ─────────────────────────

    "The ship. The one burning in your memory alongside the cold water."
    "Why were you aboard?"

    menu:
        "Commerce. Goods, a contract — you were doing business on that crossing.":
            $ builder.set_origin("merchant")
            "A merchant. Freeport was your destination; that much is certain."

        "It was your ship. Or close enough — you were crew.":
            $ builder.set_origin("crewmate")
            "A sailor. You knew every creak of that hull. Past tense, now."

        "A new start. You came from Erathal; the south was supposed to be the beginning of something.":
            $ builder.set_origin("immigrant")
            "An immigrant. Erathal behind you; Thalvath ahead — until the sea had other plans."

    ## ── Fragment 5: UPBRINGING (flavor — colors text) ─────────────────────────

    "Older memories now. The kind that don't have hard edges."
    "What was home, when you were young?"

    menu:
        "Two parents. Warm enough, in its way.":
            $ _upbringing = "two_parents"
        "One parent. You made it work.":
            $ _upbringing = "single_parent"
        "None to speak of. You learned to carry yourself.":
            $ _upbringing = "orphan"

    ## ── Fragment 6: ADULT BACKGROUND (the trait that pays off in this chapter) ──

    "The voyage feels far away already. But before the voyage — what had your life been?"

    menu:
        "Life at sea. Docks, boats, the salt in everything.":
            $ builder.set_background("sea_life")
            "The sea is not a stranger. It's where you have always lived."
        "Hard years. Struggle, scarcity, surviving what should have broken you.":
            $ builder.set_background("hard_years")
            "Hardship has made you dense as iron."
        "Books and study. Libraries, apprenticeship, the quiet thrill of understanding.":
            $ builder.set_background("scholarly")
            "The world rewards careful attention. You've always found more in a room than most."

    ## ── Fragment 7: NAME ────────────────────────────────────────────────────────

    "A name."
    "It comes back eventually, as names do."
    $ _player_name = renpy.input("Your name:", default="", length=30).strip()
    if not _player_name:
        $ _player_name = "the survivor"

    ## Apply flavor step to builder now that we have all pieces
    $ builder.set_flavor(player_state_sex, _upbringing, _player_name)

    ## ── Confirm screen ──────────────────────────────────────────────────────────

    "Everything coheres — slowly, like a face emerging from dark water."
    "Who you are. What you know. How you got here."

    ## Flexibility step: deferred from Fragment 1 for species with choose_* sentinels.
    ## Positioned here so it reads as part of the same weighted resolution moment.
    if _species_needs["needs_attr_choice"] or _species_needs["needs_skill_choice"]:
        call screen species_flexibility(
            CharacterBuilder.all_attributes(),
            CharacterBuilder.all_skills()
        )
        $ _flex = _return
        $ builder.set_species(_species_id, attr_choices=_flex["attrs"], skill_choice=_flex["skill"])

    $ _pre = builder.preview()
    call screen charsheet_confirm(
        _pre["attributes"], _pre["skills"], _pre["traits"], _pre["pending_free_skills"]
    )
    $ _alloc = _return

    ## Free skill picks for overlap redirects (if any)
    ## Loop runs pending_free_skills times; each pass filters out already-held skills.
    python:
        _free_skills = []
        _fpick_n = 0

    if builder.pending_free_skills > 0:
        "Your training spans more than one discipline — knowledge resurfaces in fragments."

    label _free_skill_pick_loop:
        if _fpick_n < builder.pending_free_skills:
            $ _fp_available = builder.free_skill_options(_free_skills)
            menu:
                "Appraisal — reading value, markets, and goods." if "Appraisal" in _fp_available:
                    $ _free_skills.append("Appraisal")
                "Arcana — magical theory and sensitivity." if "Arcana" in _fp_available:
                    $ _free_skills.append("Arcana")
                "Athletics — strength, agility, physical mastery." if "Athletics" in _fp_available:
                    $ _free_skills.append("Athletics")
                "Diplomacy — the art of talk and negotiation." if "Diplomacy" in _fp_available:
                    $ _free_skills.append("Diplomacy")
                "Endurance — stamina, hardiness, the long road." if "Endurance" in _fp_available:
                    $ _free_skills.append("Endurance")
                "Seamanship — vessels, tides, maritime navigation." if "Seamanship" in _fp_available:
                    $ _free_skills.append("Seamanship")
                "Survival — living off the land, reading conditions." if "Survival" in _fp_available:
                    $ _free_skills.append("Survival")
            $ _fpick_n += 1
            jump _free_skill_pick_loop

    ## Finalise character
    $ builder.allocate_free_points(_alloc, free_skills=_free_skills)
    $ player_state = builder.build()
    $ player_state.name = _player_name

    ## ── Upbringing flavour (consumed here; flag already in player_state) ─────────
    if has_flag("upbringing:two_parents"):
        "A house with two parents. The memory is distant, but it was warm."
    elif has_flag("upbringing:single_parent"):
        "One parent. The house was smaller for it. Still a house."
    elif has_flag("upbringing:orphan"):
        "No house to look back on. You learned early to build your own shelter."

    ## ── Static flag declarations (creation flags already in player_state; ───────
    ## ── literals here satisfy the orphan_flags static checker) ─────────────────
    if False:
        $ set_flag("species:elf")
        $ set_flag("species:human")
        $ set_flag("species:hajje")
        $ set_flag("class:warrior")
        $ set_flag("class:mage")
        $ set_flag("origin:merchant")
        $ set_flag("origin:crewmate")
        $ set_flag("origin:immigrant")
        $ set_flag("background:sea_life")
        $ set_flag("background:hard_years")
        $ set_flag("background:scholarly")
        $ set_flag("upbringing:two_parents")
        $ set_flag("upbringing:single_parent")
        $ set_flag("upbringing:orphan")

    return
