## Evorath — Camp threshold (§5.5, §5.8, §5.10, §5.12)
## The MVP curtain: the fishing camp's edge, one reactive NPC (lookout).
## Species bias, origin payoff, anomaly callback — all §6 DoD requirements.

label camp_threshold:
    scene bg_camp_edge
    with dissolve

    "You step off the coastal path onto the camp's edge."
    "The sand here is packed and well-worn."

    show lookout at lookout_at_camp
    with dissolve

    "A figure has been watching you come up the coast from a raised wooden platform — a simple perch just above the dune line."
    "Elf. One of the older ones: weathered skin, hair gone white, a net-hook held loosely at one side."
    "No weapon drawn. But the eyes haven't moved off you since you came around the headland."

    ## ── INITIAL REACTION BY SPECIES ────────────────────────────────────────────

    if has_flag("species:elf"):
        lookout_npc "From the sea. {i}Haei{/i} — you're one of ours?"
        "The word carries real warmth under the wariness. You're kin, visibly."
        lookout_npc "The wreck north of here? I spotted the smoke at dawn. I thought — well."
        lookout_npc "Come close, let me look at you."
        $ _gate_adv = [("Elf kinship — the camp knows its own", 1)]

    elif has_flag("species:human"):
        lookout_npc "You walked up from the wreck."
        "A statement, not a question. You've been visible for most of the last half-hour."
        lookout_npc "We don't get many people washed up on this shore. Usually they don't walk away from it."
        lookout_npc "State your business."
        $ _gate_adv = []

    elif has_flag("species:hajje"):
        "The lookout goes very still."
        "Not reaching for anything — but the calculation behind the eyes is immediate, unmistakable."
        lookout_npc "..."
        "Three long seconds of silence while the lookout takes in your hands, your hair, your eyes."
        lookout_npc "You came off the wreck."
        "Another statement. The voice is flat — not cruel, exactly. Old fear doesn't need to be cruel."
        $ _gate_adv = [("Hájje heritage stigma", -1)]
        "You have seen that look before. You will see it again."
        "Disadvantage is not a wall. It is a hill. You have climbed harder ground."

    ## ── GATE SOCIAL CHECK ──────────────────────────────────────────────────────

    "You need to say something. What you say matters."

    $ _gate_cr = check("CHA", "Diplomacy", 12, adv_sources=_gate_adv)
    call screen dice_result(_gate_cr)

    ## ── ORIGIN-FLAG DIALOGUE (§6 DoD: creation flag alters a branch) ───────────

    if _gate_cr.nat20:
        if has_flag("species:hajje"):
            "You speak plainly, directly, without apology — and something about the way you stand disarms the old fear."
            lookout_npc "..."
            lookout_npc "All right."
        else:
            "Whatever you say, you say it exactly right. The tension goes out of the lookout's shoulders."
            lookout_npc "Ha. You survived that. Come in, come in."
        $ set_flag("camp_admitted")

    elif _gate_cr.nat1:
        "The words come out wrong — too tired, too raw, something that lands as aggression."
        lookout_npc "Easy."
        "You catch yourself."
        if has_flag("species:hajje"):
            lookout_npc "I — look. You came off a wreck. I'm not going to leave you on the beach."
            lookout_npc "But you stay near the edge, you hear me?"
        else:
            lookout_npc "You don't look threatening. More: waterlogged and lost."
            lookout_npc "We have water. Come inside."
        $ set_flag("camp_admitted")

    elif _gate_cr.passed:
        if has_flag("origin:merchant"):
            "You explain yourself quickly — what you were carrying, where you were going. The honest version."
            lookout_npc "A merchant. From the crossing."
            lookout_npc "We've had three ships go missing this season. Did you — did you see anything?"
            $ set_flag("camp_admitted")
        elif has_flag("origin:crewmate"):
            "You name the ship. The route. Your role."
            lookout_npc "Crew. I can tell — the way you walk."
            lookout_npc "We found wreckage last Pertga. Empty hull, drifting. You're the first we've seen alive from this one."
            $ set_flag("camp_admitted")
        elif has_flag("origin:immigrant"):
            "You explain: from Erathal, south passage, new start. The short version."
            lookout_npc "Erathal."
            "Something in the lookout's face shifts — not warm, exactly, but recognising."
            lookout_npc "Long way to come to wash up here. All right."
            $ set_flag("camp_admitted")
        else:
            lookout_npc "Right. You'd better come in."
            $ set_flag("camp_admitted")

    else:
        ## Failed non-nat-1: lukewarm admission
        if has_flag("species:hajje"):
            "The silence stretches."
            lookout_npc "You came off a wreck. I'm not going to leave you on the beach."
            lookout_npc "But I'll want to know more before you go further into camp."
        else:
            "The lookout watches you for a long moment."
            lookout_npc "You're a survivor. Come in — but don't wander."
        $ set_flag("camp_admitted")

    ## ── ANOMALY CALLBACK (if player found the evidence) ──────────────────────

    if has_flag("found_merfolk_evidence"):
        lookout_npc "You've heard, then — the lost ships. Another season of it."
        lookout_npc "People say merfolk. I say — something is wrong, and I'd rather know what."

        if has_flag("found_anomaly"):
            "Something about the way [pn_they] says it."
            menu:
                "Show [pn_them] the device fragment.":
                    "You reach into your pack and hold out the fragment — the warped, fused piece of metal."
                    lookout_npc "What is that."
                    "Not a question."
                    if has_flag("read_arcane_signature"):
                        "[pn_they.capitalize()] stares at it for three seconds."
                        lookout_npc "There's a working in this. Not any working I know."
                        "The lookout looks at you differently now. Still wary. But something else."
                        lookout_npc "You'd better come in."
                        $ set_flag("camp_shared_doubt")
                    elif has_flag("read_impact_pattern"):
                        lookout_npc "The angle on this burn. This wasn't a creature."
                        lookout_npc "I said that, three losses ago. Nobody listened."
                        $ set_flag("camp_shared_doubt")
                    else:
                        lookout_npc "I don't know what this is. But you're right — it's not a tooth."
                        $ set_flag("camp_shared_doubt")
                "Say nothing — keep what you know to yourself for now.":
                    "The moment passes."

    jump epilogue


label epilogue:
    hide lookout
    with dissolve

    "The camp opens around you."
    "Small fires. The smell of fish and woodsmoke. Voices in the distance."

    ## Outcome flags — consumed here for the orphan_flags checker
    if has_flag("camp_admitted"):
        "You are in. Provisionally, grudgingly, or warmly — you are in."
    if has_flag("road_endurance_ok"):
        "The walk from the wreck left no lasting mark on you."
    if has_flag("camp_shared_doubt"):
        "You have already planted something in this community — a question, a doubt."

    "The eldest of this community survived the merfolk war. Their children were born into the memory of it."
    "And somewhere north of here, a wreck that doesn't add up."
    "They believe it was merfolk. Of course they do."
    "You are not sure."

    "The new year is three weeks away. The world is warming at its edges."
    "You are alive."
    "That will have to be enough, for now."

    with Pause(1.5)

    "— End of Chapter One (MVP) —"

    return
