---
name: canon-recurring-points
description: Recurring canon facts to fast-check in every lore review — sourced from lore_bible.md and evorath-mvp-spec-draft.md
metadata:
  type: project
---

Core canon facts that recur across beat reviews. Verify each:

**Frame Integrity (§5.8 / lore_bible.md "The Frame")**
- Basic search MUST yield merfolk-attributed surface evidence only (set_flag("found_merfolk_evidence")).
- Thorough / anomaly path MUST yield: (1) physical fragment — a *made* thing, not biological; (2) arcane residue — destructive school, wrong for merfolk illusion/mind-magic, signature *unfamiliar* (not attributed to anyone). Neither detail names a culprit.
- Merfolk are framed; they did NOT cause the wreck. No narrative text may imply otherwise as fact.

**Merfolk canon (lore_bible.md "Merfolk since")**
- Merfolk have been *vanished* since the 1294 MT truce — ~360 years. They are half-legendary, NOT "integrated into society" (spec §5.8 explicitly revises that older phrasing).
- Their signature power = illusion / mind-magic. Any "arcane residue" the player finds must explicitly read as the WRONG school for merfolk.
- "Siren" as a named folkloric reference is dropped — merfolk are a distinct species/faction; do not conflate with siren mythology.

**Camp disposition (lore_bible.md "Factions & Relations")**
- Elf = warm/kin. Human = neutral (live-and-let-live, NOT suspicious). Hájje = disadvantage rooted in inherited heritage fear — specifically NOT generic xenophobia.
- The camp is exclusively elven, ~dozen ashore (others on boats). One reactive NPC at the threshold.
- Elders LIVED through the merfolk war (1289–1294 MT; ~360 years past for elves who live ~1000 years).

**Hájje guardrail (§5.12 / lore_bible.md §5.12)**
- Appearance: pale skin, black hair, black eyes — visually elven, which deepens the camp's unease.
- Heritage (Yezurkstal) stays ABSTRACT: "feared/tragic" only. Never graphic, never depicted, never expanded.
- Thalvath Hájje: descended from those who fled, settled inland, peaceable. They AVOID THE SEA — doubly out of place at a coastal fishing camp.
- Disadvantage must read as FELT INJUSTICE — the world is kind; this fear is the unfair crack in it.

**Geography / direction sequence (spec §5.4)**
- North shore of Tethryn. Wreck on northwest shore.
- Camp lies EAST of the wreck. Player turns east; sea is to the LEFT heading east. Camp is east; town (V1+) is south.
- Road background (bg_coast_path) shows sea to the left — must match described direction.

**Timeline / season**
- Late Frozga, 1650 MT (last weeks of winter). Frozga = "cold/dead" in Ancient Elvish.
- Climate is mild for the south — warmer than the name implies, especially for someone from Erathal.
- New year (1 Pertga) is ~3 weeks away.

**Tone guardrail**
- Teen/hopeful. Vibrant, adventurous sword-and-sorcery. Not grimdark.
- Prejudice must land as felt injustice, never punishing or hopeless.
- No graphic violence, no sexual content, no graphic heritage depiction.

**IP guardrail (§5.11)**
- Use only Evorath proper nouns (Tethryn, Thalvath, Erathal, Freeport, Merfolk, Hájje, Frozga, Pertga, MT, Yezurkstal [name-only]).
- Never: Beholder, Illithid/Mind Flayer, Forgotten Realms, or any other proprietary named IP.

**Why:** These are the highest-frequency failure modes found when reviewing the MVP narrative beats. Captures all points from lore_bible.md + spec that a deny-list cannot catch.
**How to apply:** Run this checklist against every .rpy beat before issuing findings. Flag deviations by file:line.
