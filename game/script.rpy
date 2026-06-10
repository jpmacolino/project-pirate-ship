## Evorath — main script entry point.
## Image declarations, store initialisation, NPC definitions, label start.

## ─── Image declarations (§5.7 asset convention) ───────────────────────────
## Explicit paths so the §6 asset checker can verify every file exists.

image bg_beach_wreck  = "images/bg/bg_beach_wreck.png"
image bg_coast_path   = "images/bg/bg_coast_path.png"
image bg_camp_edge    = "images/bg/bg_camp_edge.png"
image lookout         = "images/sprites/lookout.png"

## ─── Store initialisation ─────────────────────────────────────────────────

init python:
    ## player_state is the live GameState (set by chargen, saved/loaded by Ren'Py).
    ## The evorath_api.rpy wrappers reference it by name at call time.
    player_state = None
    builder      = None

    ## Pronouns — set during chargen from sex choice.
    pn_they      = "they"
    pn_them      = "them"
    pn_their     = "their"
    pn_theyre    = "they're"
    pn_reflexive = "themselves"

## ─── NPC character objects ────────────────────────────────────────────────

define lookout_npc = Character("Lookout", color="#c8a96e")

## ─── Entry point ──────────────────────────────────────────────────────────

label start:
    $ player_state = None
    $ builder = None
    jump beach_wake
