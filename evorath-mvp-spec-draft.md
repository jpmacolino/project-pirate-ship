# Evorath RPG — MVP Build Spec (Working Draft)

> **Status legend:** ✅ Settled · 🟡 Proposed (needs your confirmation) · ❓ Open question · 📌 Bookmarked for V1+
>
> This is the MVP scope only. The world bible and later releases (V1+) are tracked separately. Nothing here is final; it's the living contract for the first autonomous release.

> **── HANDOFF / CURRENT STATE ──**
> **Settled (add):** art/style lock — FLUX.2 hosted (§7.6a resolved), style bible direction
>   locked, all 3 MVP backgrounds done (§5.7). PC never shown in narrative — combat-token
>   only (§5.7). Curtain = camp threshold, not gate (§5.5). Background-continuity-by-narration
>   note (§5.4). Camp sea-defenses now canon (bible).
> **Next up:** remaining MVP art, each its own focused chat — (1) the NPC sprite (elf lookout,
>   needs a short character brief), (2) UI (art + Ren'Py GUI). Then the build, in Claude Code.
> **Still open:** 7.5 micro-math · 7.7 skill/stat reconciliation (after story) · 7.9 nat-20/nat-1
>   · 7.13 build-env firm-ups.

---

## 1. Vision & Staging

✅ A narrative-heavy RPG set in the world of **Evorath**, on its southern continent **Thalvath** *(name provisional)*, ~1650 MT. Sword-and-sorcery tone: vibrant, adventurous, magic and mythical creatures.

✅ The long-term game is **open-ended**: any playable species, base classes that branch into specialized subclasses, a set story spine with wide exploration around it. The MVP does **not** attempt this — it builds the order the vision itself implies:

| Element | MVP | Later releases |
|---|---|---|
| Species | Human, Elf, Hájje | Full native roster, then non-native |
| Classes | Warrior, Mage (base only) | Subclass branching |
| Story | Set, railroaded opening | Open exploration of the opening area, then beyond |
| World | One beach + road + first town gate | Towns built out, regions opened |

🟡 **Tone & rating posture.** Target tone is **hopeful, adventurous, broadly accessible** (~ESRB Teen / PEGI 12 equivalent). Dark canon (e.g. the Yezurkstal origin) *exists in the bible* but stays deep background — never surfaced graphically. Practical payoff: a Teen-band tone keeps digital storefronts low-friction — digital games are rated free via the **IARC** questionnaire (ESRB/PEGI coalition); **Google Play requires an IARC rating**, **Steam** uses its own content survey and doesn't require one. The content that would raise the age band / add friction (graphic violence, sexual content) is exactly what the content guardrail (§5.12) already fences off. So tone discipline = distribution ease.

🟡 **Presentation posture — "visible tabletop."** Surface the mechanics rather than hide them: show dice rolls, DCs, attributes/skills, advantage/disadvantage. Rationale: the core loop *is* skill checks, the system is already characterful, and visible rolls (cf. Disco Elysium, BG3) create tension and serve player agency. **Boundary:** this is a *presentation/UX* posture, NOT a mandate to port the full tabletop system. No GM (every DC/advantage is pre-authored), combat still deferred — adapt a subset, don't port wholesale. Consequence: visible numbers raise the tuning bar (no unwinnable-by-design checks; DCs in sane bands) — a likely future validation-layer check.

## 2. Build & Autonomy Model

✅ **One prompt per release.** Claude Code works unsupervised through the entire MVP, then stops and considers its work done for human review. After MVP is validated, V1 proceeds the same way.

✅ **The git history is the review surface.** One logical change per commit, conventional commit messages, auto-committed by CC.

✅ **Commit gate (enforced by hook):** no commit lands unless `pytest` passes and `renpy lint` is clean.

## 3. Tech Stack

✅ **Ren'Py.** Narrative authored in Ren'Py script (declarative DSL); all game systems in **pure Python** (the layer you audit).

✅ Delivery targets: desktop (Windows/macOS/Linux), Web/HTML5, Steam, Android/Play Store. (iOS available later.)

## 4. Layer Contract

🟡 The narrative script calls into a **stable Python mechanics API** — proposed surface:

- `check_skill(skill, dc)` → pass/fail
- `adjust_stat(stat, delta)`
- `set_flag(name)` / `has_flag(name)`
- `add_item(item_id)` / `has_item(item_id)`

🟡 Everything content-shaped is **data, not engine code**: species, classes, character-builder questions, and items are defined as data structures. New species/questions in later releases add data, never touch the builder.

## 5. MVP Scope

### 5.1 Playable Characters
- ✅ Species: **Human, Elf, Hájje**
- ✅ Classes: **Warrior, Mage** (base only)

### 5.2 Character Builder (diegetic opening → explicit confirm)
- ✅ Framing: **light amnesia.** Creation is paced through the opening as fragments resurfacing, not a menu wall.
- ✅ **Two-phase flow:** (1) diegetic opening sets identity + backstory through narrative choices; (2) at the close of the opening, the "character sheet" resolves into an explicit confirm-and-tune screen (the fragments cohering into a clear self — fiction and mechanic reinforce each other).
- ✅ **Sticky vs. tunable split:** narrative *facts* (species, ship-reason, origin) are identity and set story flags — they lock once chosen (no un-choosing on a stat screen, which would orphan dependent flags). The *numbers* (attributes, skills, + a pool of free points) are what the confirm screen exposes for adjustment. Story sets who you are and pre-weights the build; the screen shapes the build, not the past.
- ✅ Three-layer authoring: **Schema** (pre-authored) · **Mechanical mappings** (pre-authored, precise) · **Prose** (you or the agent, per item).
- ✅ Every option tagged **mechanical** or **flavor**. Mechanical options are load-bearing and specified by you; flavor options the agent may expand against the lore bible.
- 🟡 Questions (draft set): sex · species · class · "Why were you on the ship?" (merchant / crewmate / immigrant from Erathal / …) · upbringing (two parents / single parent / orphan / …). **"Where did you grow up?" cut from MVP** (see 7.2; held for V1+).

### 5.3 Opening Scene — The Beach
- ✅ Player wakes on shore amid ship debris. Searches the wreckage.
- ✅ Exercises the core loop: observation/thoroughness → skill check → reward (gear + clues). Thorough vs. basic players get different finds.

### 5.4 Chapter Arc
1. ✅ **Beach** — wake, paced chargen, debris search.
2. 🟡 **The road** — 1–2 beats (a choice + a skill check) that exercise the loop a second time under different conditions.
3. ✅ **First town gate** — arrival = MVP curtain.
- 🟡 **Background continuity is carried by narration, not camera-matching.** The beach and
  road backgrounds are framed from different vantage points (wake shot looks seaward at the
  wreck; road shots look along the coast). This is canon-consistent: the camp lies east of
  the wreck on Tethryn's north shore (bible/§7.4), so the player turns and heads east, sea on
  the left — exactly as the road art shows; the beach shot's right-side headland is that same
  eastward direction. **Constraint for narrative-writer:** the `.rpy` must make the movement
  explicit (wake facing the sea at the wreck → head east along the coast, sea to the left,
  toward the distant headland → camp threshold) so background cuts read coherently. No spatial
  contradiction permitted between described direction and shown orientation. Sequence +
  described direction = the narrative's job; the art is consistent with it.

### 5.5 MVP Curtain — The Town Gate
- 🟡 The gate hosts **one reactive NPC encounter** that pays off a creation flag (species / Erathal origin / ship-reason changes the exchange). This proves the chargen→consequence loop end to end.
- 🟡 The town itself is **not built** for MVP — a threshold and one NPC, then "end of MVP." The town is a V1 problem.

### 5.8 Narrative Spine (MVP) — settled structure
- ✅ **The merfolk red herring.** The wreck *appears* to be merfolk work; it isn't. A hidden force (identity/motive TBD — see 7.1) is framing them.
- ✅ **Plausibility engine:** a centuries-old merfolk-vs-landbound war is the bad blood that makes the frame stick — people *want* to believe the sea-folk did it.
- ✅ **Frame mechanics from the bible:** Merfolk (illusion/mind-magic) are the frame-ee: a feared enemy from the 1289–1294 war who vanished after the truce — unseen for centuries but for dismissed sailor's tales. Mind-magic (their worst war weapon) keeps 'they lured the ship' believable; their very absence makes the charge un-disprovable. A **recent pattern of lost ships** is the cultural fuel — coastal communities are already uneasy and primed to blame the sea-folk, so the frame catches fast." (Siren dropped: merfolk are a distinct species/faction, not to be conflated with siren folklore.)
- ✅ **Two-layer debris search** (ties to §5.3): a **basic** search lands the obvious "merfolk attack" reading (herring swallowed); a **thorough** search also surfaces one detail that doesn't fit merfolk methods (doubt seeded, meaning unknown). Thoroughness buys the deeper mystery layer.
- ✅ **Charged gate:** player reaches a town already primed to blame the sea-folk (uneasy about lost ships), carrying firsthand "I was attacked" experience. Thoughtful players exit Ch.1 as the lone doubter — the V1 hook.
- ✅ **Emotional arc:** lost/vulnerable → resourceful → arriving-but-not-belonging.

### 5.6 Systems Exercised by the Slice
✅ Character creation · stats · skill checks · choices · inventory · flags · save/load.

### 5.7 Art & Assets (MVP)
- ✅ **Style bible — direction locked.** Stylized hand-painted fantasy illustration:
  semi-realistic, clean readable shapes, visible painterly brushwork; warm-dawn palette
  (golds, soft teals, sand-beige, cool shadow); soft diffused light; illustrated-VN /
  concept-art register, explicitly NOT photorealistic. Chosen functionally — forgiving of
  custom-species anatomy, holds consistency across a set, reads at background/sprite/token
  scale, fits the §1 hopeful-Teen tone. The confirmed beach prompt is the **seed style
  language** every other asset inherits.
- ✅ **Two visual registers (named, not a defect):** FLUX = illustrative layer (backgrounds,
  sprites, UI); Inkarnate = cartographic layer (post-MVP overworld map; battle maps if combat
  lands). Inkarnate commercial rights covered by the paid subscription; it stays a human-hand
  tool (no API, outside the agent asset lane).
- ✅ **PC is never shown in narrative — combat token only.** The player character has no
  narrative sprite; its sole on-screen representation is a token on the combat board (V2+,
  with combat). MVP and pre-combat releases need zero PC art. Bounds art volume (no
  species × class × sex sprite combinatorics) and reserves narrative sprites for NPCs.
- ✅ **Decoupled from the build.** Art is authored/locked *outside* the autonomous run. The agent never generates images — it only references existing files in an approved asset folder. The "every referenced asset exists" check (§6) is the entire enforcement story for MVP. No generator in the autonomous path → no ToS risk, no per-run cost, no fragility.
- ✅ **Manual authoring in the automatable family.** The MVP set is generated by hand (via a UI, no scripting) using the *same model family* we'll automate with later — **FLUX or Stable Diffusion**, NOT MidJourney. This is what makes post-MVP replication reliable: style does not transfer across model families via prompt text, and the consistency tooling (LoRAs, reference-image conditioning) lives in the FLUX/SD ecosystem, not MidJourney's closed model.
- ✅ **The locked set doubles as the style bible** and as future reference/training material to pin the look downstream.
- ✅ **License discipline:** ship only on commercially-clear licenses (e.g. FLUX Schnell = Apache-2.0; SD3.5/SDXL = Stability Community License, free under $1M revenue). Avoid non-commercial variants (e.g. FLUX Dev local license).
- ✅ **MVP art surface is small:** ~3 backgrounds (beach, road, town gate), 1–2 NPC sprites, UI. A fixed set, generated and locked in one focused session.
- ✅ **Asset convention (locked set):** backgrounds live in `game/images/bg/`, named
  `bg_<place>[_<qualifier>]` — content-based (named for what they depict, not story order).
  MVP backgrounds complete: bg_beach_wreck, bg_coast_path, bg_camp_edge. The §6
  "every referenced asset exists" check enforces filename ↔ script-reference match; the
  narrative references these names (e.g. `scene bg camp edge`) and conforms to it.

### 5.9 System Kernel (MVP)
- ✅ **Resolution:** d20 + Attribute + Skill vs. DC (difficulty bands 5–30, per the system bible). Advantage/disadvantage = roll 2d20, take higher/lower; **every trigger explicitly authored** (no GM). Refines §4 `check_skill` → roughly `check(attribute, skill, dc, adv=None)`.
- ✅ **Six primary attributes as data; slice exercises most.** INT (read the wreckage), CHA (the gate), STR (physical feats), SPR (Mage arcane read), **END (endurance: trekking, harsh elements, stamina, toxin resistance — non-combat-relevant in its own right, not merely an HP feeder)**, DEX (nimble moments). Combat-only secondary stats (HP/SP/MC/PR/MR/EC) deferred with combat.
- ✅ **Class as lens (works without combat):** the off-note that doesn't fit merfolk is reachable by any class via a thorough Investigation check; a **Mage** additionally senses the arcane signature (SPR + Arcana), a **Warrior** reads the impact pattern no sea-creature leaves (martial eye). Same buried truth, different lens — class matters, mystery deepens, the 6 paths play differently. (No class locked out of the core clue — satisfies the 6-path DoD.)
- 🟡 **Skills (provisional, see 7.7):** Investigation (INT), Athletics (STR), Diplomacy (CHA), Arcana (SPR), Endurance/Survival (END). Reconcile against the written story.
- ✅ **Creation → sheet:** attributes base 1 → species + class bumps → diegetic story answers pre-weight (mappings TBD, 7.5) → confirm screen reveals the sheet + free points to tune (6 pts, max +2 to one, cap 10). Narrative facts locked; numbers adjustable.

### 5.10 Advantage / Disadvantage Model (MVP)
- ✅ **Mechanic (from system bible):** Advantage = roll 2d20, take the **higher**; Disadvantage = roll 2d20, take the **lower**. Binary state — there is **no 3d20+**. Advantage is a switch (on / off / inverted), never a stacking dice resource.
- ✅ **Resolution = count, don't stack (net sign).** Gather *all* applicable sources simultaneously, tally net direction, roll once. Any net positive → advantage; any net negative → disadvantage; zero → straight roll. **Magnitude never matters, only sign** (3 adv + 1 disadv = a single advantage). Never resolve pairwise/in sequence (order would wrongly imply stacking).
- ✅ **One axis per source (anti-compounding principle):** **skills move the number** (flat modifier); **traits/situation toggle advantage**. The same source never grants both. A skilled, well-equipped fisher gets a high Fishing *modifier* (skill) **and** advantage (trait/equipment) — from two different sources, which is correct and still tunable.
- ✅ **MVP trigger set:** **species** bias (gate prejudice → disadvantage; goodwill → advantage) · **environmental** (weather, light, sea state, terrain) · **equipment** (right tool for the job; ties to debris finds → inventory loop) · **one signature trait** ("Brine in Blood": advantage on sea/boat tasks — see §5.12). Full **rapport** + deeper **trait tree** → V1; more → V2+.
- ✅ **Deferred trigger — Momentum.** The bible's spendable advantage resource (player spends Momentum for advantage on demand) is tangled with combat/progression economy → **deferred with combat**; noted so the later texture (earned, spendable edge) isn't lost.
- ✅ **Legibility rule (visible-tabletop):** every applied adv/disadv carries a short authored **label** shown to the player ("Advantage: proper tools" / "Disadvantage: the camp distrusts your kind"; signature traits get proper names like "Brine in Blood"). Disadvantage especially must always read as fair and understandable the instant it lands — invisible disadvantage feels like cheating. So each trigger needs a label string, not just a boolean.

### 5.11 IP / Mechanics Guardrail (standing)
- ✅ **Mechanics are free; expression and named IP are not.** Game mechanics aren't copyrightable (d20 rolls, DCs, advantage/disadvantage, crit/fumble, conditions). The D&D **SRD is also released under CC-BY-4.0** (irrevocable), so the core d20 chassis is doubly safe. **Rule:** write every rule in our own voice (already the case); never paste rulebook text; never use proprietary named IP (Beholder, Illithid/Mind Flayer, Forgotten Realms, etc.). Evorath's own roster (Hájje, Lizock, Toada…) sidesteps this entirely. Candidate for the lore/asset validation layer (deny-list of protected proper nouns).

### 5.12 Creation Mappings (MVP)
- ✅ **Two-layer data architecture:** **species → attributes** (stable); **sub-species / origin → skills & traits** (variable). Future-proofs the V1 elf-variant expansion (new variants are pure data slotted into an existing seam; builder untouched). **MVP models the sub-species layer but populates one entry** (sea-faring elf as the default southern elf).
- ✅ **Skill-granting model:** symmetric — **race grants 1 skill, class grants 1, origin grants 1** (= 3 fixed grants) **+ a modest player allocation** at the confirm screen (feeds the "modify if desired" flow). Nets ~4–5 skills touched at creation. No 4th *fixed* grant — breadth comes from allocation. (Exact count/values reconcile against content at 7.7.)
- 🟡 **Overlap rule (needs confirm):** when two sources grant the same skill (e.g. Hájje race + Mage class both → Arcana), **redirect** (duplicate becomes a free pick — tuning-safe, fits "adaptable = choice") vs. **stack** (doubles; more build identity, riskier in a visible-dice game). *Leaning redirect.*
- ✅ **Attributes (each race bumps two; creation math itself is newly-owned, provisional):** **Elf → DEX/CHA**; **Hájje → SPR/DEX** (DEX overlap with Elf is fine — they split CHA vs SPR); **Human → choose any two** (the flexible identity).
- ✅ **Racial skills:** **Elf → Survival** (sea-faring default; chosen over Athletics partly to avoid colliding with Warrior); **Hájje → Arcana**; **Human → choice of skill** (mirrors the attribute choice — Human + Immigrant are the two flexible builds).
- ✅ **Class skills + lens (combat kit deferred):** **Warrior → Athletics** + martial-eye debris read; **Mage → Arcana** + arcane-signature debris read (SPR+Arcana).
- ✅ **Origins = 3 for MVP (merchant / crewmate / immigrant), each grants 1 skill + a gate-reaction flag (the DoD payoff):** **Merchant →** a trade/business skill (Appraisal/Barter — name pending 7.7), reads as outsider-with-means; **Crewmate →** sea/ship knowledge (Seamanship-ish) that *applies* to the wreck read → natural leg-up via modifier (not a bolted-on advantage); **Immigrant (from Erathal) →** *chosen* skill + outsider flag (sharper gate friction). Ship-reason flag is the load-bearing mechanical payoff at the gate.
- ✅ **Brine in Blood = sea-faring Elf's racial trait** (🟡 vs. tying it to crewmate origin): advantage on sea/boat tasks; pays off in MVP on the beach debris search (sea-wrack) → not an orphan. Demonstrates the adv side of the model; Hájje gate bias demonstrates the disadv side; equipment/environment open to all. Broader per-race starting traits → V1.
- ✅ **Traits = a 4th creation step (adult-background question).** A single question ("Before the voyage, what had your life been?"), ~3 options, each granting **one** trait; each trait must pay off in the beach→road→gate slice (no orphans). Distinct from childhood *upbringing* (flavor). Seeds the V1 lifepath (7.12). MVP option sketch (roster provisional, reconciles at 7.7): *life at sea/dockwork* → **Brine in Blood** (adv on sea/boat tasks; pays off on the beach); *hard years* → hardiness/street-wise (road endurance/exposure beat, END); *books & study* → learned/arcane-attuned (deeper clues / arcane read).
- ✅ **Brine in Blood = background trait, not race/origin-locked.** Anyone choosing the sea-life background gets it (resolves the earlier Elf-vs-crewmate question). Still guarantees the advantage-side demo (whoever picks it) while Hájje gate bias guarantees the disadvantage side — both halves of the model exercised, independently selectable.
- ✅ **Traits are intentionally asymmetric (design principle).** Unlike skills (symmetric grants), traits are *meant* to be imbalanced: race itself functions as a trait; some classes grant more than others; narrative events can bestow them; some origins may grant extras (V1+). This is why traits sit on the *advantage-toggle* axis, not the tunable-number axis.
- ✅ **Upbringing (two parents / single parent / orphan) = flavor for MVP.** Colors text / opens dialogue; no stat effect. Mechanical upbringing → V1+.
- ✅ **Sex = flavor for MVP.** Narrative/pronoun flag, no stats. Future hook → the per-NPC trait-interaction system (7.10).
- ✅ **Hájje bias (MVP) = village-level species disposition,** hardcoded: Elf favorable / Human neutral / Hájje disadvantage on the gate social check. Fairness cap holds *by definition* (disadvantage can still succeed — a hill, not a wall). First concrete instance of the future per-NPC system (7.10).
- ✅ **Canon note (Hájje origin):** Hájje descend from **Yezurkstal** (big-bad of the novels), an abomination of immense power conceived through atrocity and dark-deity meddling, who propagated the line by magic and domination — not generic dark elves. This earned, feared heritage gives the gate bias an in-world rationale. 
- ✅ **Spec and the agent-readable lore bible record the abstracted fact only.** Any
  full-scope canon the author keeps lives **outside the agent's reach** — not in the
  repo, not in any path the `lore-reviewer` or `narrative-writer` loads — so the
  guardrail isn't defeated by the agent reading the very content it must never expand.
  (The `lore-reviewer` reads the bible; see §9.2.)
- ✅ **Content guardrail (Hájje heritage):** the origin involves sexual violence — a theme an unsupervised agent must NOT expand or depict. The agent may reference the Hájje's feared/tragic heritage *in the abstract*; it must never generate graphic depictions, and the theme stays deep background unless deliberately authored forward. Enforce via the lore/content-validation layer, not a prompt.
- ✅ **MVP attribute allocation (direction set; math provisional):** lean *open* (Fallout-SPECIAL-style) — small fixed racial bumps + the bulk free-assigned at the confirm screen. Leveling / earned attributes / class restrictions are progression (see 7.11), deferred. Exact bases & pool sizes → focused systems pass.

## 6. Definition of Done (machine-checkable)
- ✅ `pytest` green and `renpy lint` clean.
- 🟡 Slice playable start → town gate for **all 3 species × 2 classes (6 paths)** without error.
- 🟡 Save/load works mid-chapter.
- 🟡 **At least one creation flag demonstrably alters a branch** — and **no orphan mechanical flags** (every mechanical flag has a consumer; lint-checkable).
- 🟡 Every referenced asset (image/sound) exists.

## 7. Open Questions / Decisions Pending
- ✅ **7.1 Story spine — RESOLVED.** Mechanism pinned: the ship was destroyed by a **deployed
  magical device** (directed destructive magic, not a creature), staged to read as a merfolk
  attack. The thorough-search off-note: directed non-creature impact + residual destructive
  arcana of an **unfamiliar signature** (wrong, not whose), plus physical device fragments.
  Basic reading is free; the off-note is earned (resolution mechanic → build, §5.9).
  **Perpetrator identity/motive = author canon** — outside the agent-readable bible, **not
  revealed in MVP**. Recorded abstractly in the lore bible (the-frame).
- ✅ **7.2 Settlements fork — RESOLVED (defer).** "Where did you grow up?" is **omitted from MVP** entirely (not just flavor-only) and held for V1+, when geography is settled and rapport can be mechanical. Safe to defer at zero cost: the builder is data-driven (§4), so adding onboarding questions later is pure data entry, never a builder code change. Onboarding question set expected to grow across V1/V2.
- ✅ **7.3 Combat — DEFERRED (decided).** MVP is pure narrative + skill checks; no combat system. Combat is a large system reserved for a later release.
- ✅ **7.4 First settlement — SETTLED.** A small, **seasonal/mobile fishing encampment** a short way **east** of the wreck: tents, drying racks, beached boats, fisher families, maybe a small garden plot. Fishes local grounds for some seasons, then relocates X km down-shore to fresh grounds (grounded in real migratory-fishery practice). Design payoffs: (1) **impermanence is the in-fiction reason the "town" isn't built out** — not a shortcut; (2) - 🟡 **MVP curtain = the camp threshold, not a gate.** The seasonal fishing camp has no gate
  or wall (impermanent tents — the in-fiction reason the "town" isn't built out; §7.4). The
  curtain is the camp's edge, where a wary elf lookout clocks a stranger from the surf.
  "Gate" language retired throughout §5.5 in favor of "threshold / camp edge." (3) sea-dependent + already-suspicious (real fishing camps lived with territorial friction, boat theft, sabotage) makes it the hottest possible **frame-amplifier** (§5.8); (4) **stranger-from-the-sea** friction stacks onto species/origin friction at the threshold. **Name — RESOLVED:** none. A seasonal, mobile camp carries no fixed proper name; it's referred to by the island (**Tethryn**) or descriptively ("the fishing camp"). The camp is now fleshed out in the lore bible (an exclusively-elven, generational maritime community whose eldest survived the merfolk war). 
  - **Camp sea-defenses (canon).** The seasonal fishing camp keeps modest, improvised defenses
  facing the water: weathered warding-stakes and small carved sea-charms set toward the surf,
  plus a simple raised lookout perch. They read as an expression of the world's commonplace
  domestic warding (cf. runestones), born of lingering merfolk-war fear rather than any present
  threat — merfolk have been unseen since the 1294 truce. **Frame tie-in:** a camp visibly
  braced against the sea deepens the plausibility of the staged "merfolk attack" (the-frame /
  §5.8) — people already primed to fear the sea-folk.
- 🟡 **7.5 Mechanical mappings — mostly RESOLVED into §5.12.** Settled: species attributes, racial/class/origin skills, origin gate-flags, upbringing/sex as flavor, Hájje bias, Human full flexibility, open attribute-allocation direction, **trait structure (adult-background question; Brine in Blood as a background trait; traits intentionally asymmetric)**. **Residual micro-decisions:** (a) overlap rule — redirect vs. stack (*leaning redirect*); (b) exact creation math (attribute bases, pool sizes) → focused systems pass; (c) provisional skill/trait names reconcile at 7.7.
- ✅ **7.6 Art — model decision RESOLVED.** FLUX over Stable Diffusion (FLUX.2 family),
  generated **hosted**. Local ruled out (8GB-VRAM card can't run FLUX.2 well; hosted also
  removes the constraint and suits the small MVP asset count). License discipline on the
  hosted path: commercial clarity comes from the **host's output terms**, confirmed in
  writing per host — not inferred from the model's open-weights license. Shippable tiers:
  Pro/Flex (hosted, commercial) or Klein (Apache-2.0); **FLUX.2 Dev is non-commercial —
  excluded.** Pro's multi-reference input (~8–10 reference images) is the planned route to
  downstream character/token consistency (the fix for prompt-only failure on novel creatures).
  **Still open:** (b) full in-the-loop pipeline for later releases (unchanged).
- 📌 **7.7 Skill set — bookmarked (revisit after MVP story is written).** Current list is intentionally light (early draft). Don't finalize MVP skills abstractly — derive them from the written content. Once the full slice exists, audit that (a) every skill the beats call on exists, and (b) every stat shown on the confirm screen earns at least one moment in the slice — no orphan/dormant stats (visible-tabletop fairness). Long-term: flesh out the general skill list for the whole game.
- 📌 **7.8 Advantage/Disadvantage design — RESOLVED into §5.10.** (Trigger taxonomy, net-sign resolution, one-axis-per-source, labels.) Remaining growth (full rapport, deep trait tree) is V1+ content, not an open MVP question.
- ❓ **7.9 Natural 20 / Natural 1 rule.** Does a nat 20 auto-succeed / nat 1 auto-fail (and/or carry a crit/fumble flavor beat)? Free design choice — confirmed not an IP issue (§5.11), and direction is conventional, not inherited. Matters more in a *visible-dice* game (a seen nat 20 should probably *mean* something). Interacts with tuning. Lean: embrace some crit/fumble feel; exact form TBD (auto-success only? bonus debris find on a nat 20 search? flavor only?).
- 📌 **7.10 Per-NPC trait-interaction system — bookmarked (V1+).** General system: individual NPCs carry reactions keyed to player traits (sex, species, origin) — e.g. a chauvinist who dismisses a female PC, a xenophobe who distrusts outsiders. **MVP hardcodes one instance** (village anti-Hájje/outsider disposition, §5.12); **V1 generalizes** the hardcoded instance into the per-NPC system. MVP feature is the seed, not throwaway.
- 📌 **7.11 Progression system — bookmarked (V1+).** Leveling, earned attribute/skill points, and class-restricted advancement. The open Fallout-SPECIAL-style allocation model (§5.12) is the *creation-time* half; this is the *growth* half. Deferred with combat (no leveling in a one-chapter slice).
- 📌 **7.12 Adult-background → lifepath (V1+).** MVP's single background question (one trait, ~3 options — see §5.12 once confirmed) is the seed; V1 grows it into a richer "personal history as an adult" lifepath (more nodes/questions, richer trait grants) — pure data additions. Distinct from childhood *upbringing* (flavor).
- 📌 **7.13 Build-environment firm-ups — bookmarked.** Guardrail layer (subagents,
  hooks, the human-owned DoD gate via run_dod.py) is designed; these reconcile later:
  - (a) **Check patterns vs. real conventions** — orphan-flag/asset/layer checks encode
    provisional Ren'Py + API patterns. Reconcile against the actual project layout and
    API surface once settled (early systems pass).
  - (b) **No-orphan-stats check** (ties to 7.7) — run_dod doesn't yet verify every
    confirm-screen stat earns a moment in the slice. Add after the story is written.
  - (c) **6-path playthrough + save/load harness** — stubbed; authored during the build,
    then wired into run_dod.
  - (d) **Deny-list / content patterns** — confirm borderline terms (e.g. "drow") in the IP pass.
  - (e) **DOD_GIVE_UP_N** (default 3) — confirm the Stop-hook give-up threshold.
  - (f) **Conventions the gate enforces** (asset folder layout, API names) are set up
    front — environment decisions, not build outputs.

## 8. Explicit Non-Goals (MVP)
Full species roster · subclasses · free exploration of the opening area · explorable town hub · multiple chapters · romance/relationship systems · combat depth (pending 7.3).

## 9. Build Environment & Guardrails

> The autonomous run (§2) happens *inside* this layer. §9 is the cage and the
> contract; everything in §5 is what the agent builds inside it.

### 9.1 Enforcement principle
- ✅ **Enforcement is a property of the repo, not the agent's goodwill.** Durable
  gates are git-native and fire on any commit; Claude Code hooks sit on top as fast
  feedback. Layered, not single-point.
- ✅ **The agent never authors the gate it's judged by.** DoD checks and deny-lists
  are human-owned environment; the agent writes the work the gate measures — including
  its own feature tests, with the git history (§2) as the review surface. *(Boundary:
  feature tests = build; the cross-cutting DoD/safety gate = environment.)*

### 9.2 Subagents (four)
- ✅ Four, each earning its slot by **context isolation** or a **distinct evaluative
  stance** — never by analogy to a job title:
  - **`systems-engineer`** — producer; pure-Python mechanics (§3, §4, §5.9–5.10).
    Its critic is `pytest` (correctness is mechanical → no LLM reviewer needed).
  - **`narrative-writer`** — producer; `.rpy` and the beach→road→gate beats
    (§5.2–5.8). Reaches mechanics through the API only.
  - **`lore-reviewer`** — read-only **semantic critic** vs. the (abstract) lore bible;
    catches canon/frame/tone drift a deny-list can't.
  - **`dod-runner`** — read-only DoD **runner/triage**; isolates the battery's verbose
    output, returns only failures + owning agent. Read-only ⇒ can't game the gate.
- ✅ **Chaining is orchestrated by the main session** (subagents can't spawn subagents):
  narrative-writer writes a beat → main invokes lore-reviewer → main relays findings.
- ✅ **Names follow the role convention.** Delegation is driven by the `description`
  field; the name is the handle for explicit invocation (@-mention, `--agent`) and for
  `SubagentStart/Stop` matchers.
- ✅ Definitions are doc-compliant: trigger-style `description`, minimal `tools`,
  intentional `model` (dod-runner → haiku), `memory: project` for the two that
  accumulate patterns (lore-reviewer, dod-runner), "When invoked → checklist → output".

### 9.3 Claude Code hooks (`.claude/settings.json`)
- ✅ **PreToolUse** on `git commit` → deny `--no-verify`/`-n` (plug the gate bypass).
- ✅ **PostToolUse** on `Edit|Write` → IP/content scan of `.rpy` at authoring time
  (`decision: block` feeds the violation back to fix).
- ✅ **Stop** → run the DoD battery; keep working until green; after `DOD_GIVE_UP_N`
  no-progress turns, write `BLOCKED.md` and stop for human review.
  (🟡 `DOD_GIVE_UP_N = 3` — confirm.)
- ✅ **SessionStart** → re-orient a resumed run (branch, working-tree state, open
  questions, any `BLOCKED.md`).

### 9.4 Authoritative gate (`.githooks/pre-commit`)
- ✅ Git-native pre-commit runs `run_dod.py`; fires on **any** commit (agent, human,
  CI) — the hard floor, distinct from `.claude/hooks` which fire only while CC acts.
  Committed + versioned, wired via `core.hooksPath = .githooks`.

### 9.5 DoD battery (`run_dod.py`) — human-owned
- ✅ Single orchestrator; all three consumers (git hook, Stop hook, dod-runner) call it,
  so they agree by construction. Runs the deterministic detectors in `evorath_checks/`
  + `pytest` + `renpy lint` (+ future playthrough). `--json` for hooks, `--static` to
  skip slow tools.
- 📌 Firm-ups tracked at **7.13**.
- ✅ **Progressive strictness (PASS / SKIP / FAIL).** Each check resolves to one of three
  outcomes: **PASS** (ran, clean), **SKIP** (the tool or its inputs don't exist yet —
  loud in the report, does not block), **FAIL** (present and broken — blocks the commit).
  This lets the gate run from day one: pre-content, `pytest` with no tests and
  `renpy lint` with no SDK/`.rpy` SKIP rather than block. Each check becomes *required*
  automatically as the project fills in (tests appear → pytest must pass; `.rpy` +
  `RENPY_SDK` present → lint must pass). **Boundary:** SKIP is a bootstrap convenience,
  not a way to dodge the gate — the authoritative "all green *including* pytest + renpy
  lint" is enforced at final review / CI, where the tools and content are present.

### 9.6 Constitution (`CLAUDE.md`)
- ✅ Loaded every session; encodes the layer contract, commit discipline, and the hard
  rules (no image generation — enforced by *omitting the tool*, not a rule; abstract
  Hájje; no named IP; net-sign adv/disadv), plus the DoD and the open questions.
  CLAUDE.md is the *soft* (prompt) layer; the hard versions live in hooks/linters.

### 9.7 Scope boundary — environment vs. build
- ✅ **Environment (pre-authored, human-owned):** `CLAUDE.md`, `settings.json`, the 4
  agents, the 4 hooks, `.githooks/pre-commit`, `run_dod.py`, `evorath_checks/`.
- ✅ **Build (Claude Code authors during the run):** game systems + their tests,
  narrative `.rpy`, **all game data incl. the §5.12 creation mappings**, the 6-path
  playthrough harness.
- 🟡 **No skills for MVP** — the work they'd wrap is covered by `dod-runner` or is V1
  content; a `/new-origin`-style data-scaffold workflow revisits at V1 alongside 7.12.

### 9.8 Setup & Python environment
- ✅ **Two Python contexts, kept separate:**
  - **Runtime** — Ren'Py's bundled Python (3.12 in current 8.5.x). Comes with the SDK,
    not pip/venv-managed; runs game/ at play time and powers `renpy lint`. Point
    `RENPY_SDK` at the SDK folder.
  - **Dev/tooling** — a normal venv (match Python 3.12) running `pytest`, `run_dod.py`,
    and `evorath_checks/`.
- ✅ **Why the split is safe:** mechanics are pure stdlib Python (§3/§4), so they behave
  identically under either interpreter and unit-test under plain `pytest` without launching
  the engine. **Constraint:** `game/systems/` must never `import renpy` — keeps it
  engine-independent and testable. (Candidate `layer.py` check; see 7.13.)
- ✅ **One-time setup (per clone):** install Python 3.12 *on PATH* (so the hooks, the git
  gate, and the venv all resolve `python` — else switch `python`→`py` in `settings.json`
  and the pre-commit script); `git config core.hooksPath .githooks`;
  `chmod +x .githooks/pre-commit` (*nix); `python -m venv .venv` + `pip install pytest`;
  set `RENPY_SDK`; gitignore `.venv/` and `.claude/state/`.
- ✅ **Smoke test:** `run_dod.py --static` is stdlib-only (no pytest/SDK); the full battery
  needs the venv + `RENPY_SDK`.
  - 🟡 **Gate invokes the project env's python by path** (`.venv/Scripts/python`) in the
  settings.json hooks and the pre-commit script — so the gate is correct regardless of
  what's activated. Currently it works only because you commit from the activated venv
  (PATH inherited). Pending.

  ### 9.9 Lore bible (interface)
- ✅ Separate, human-authored reference (world bible tracked outside this spec — see
  header), but the MVP build depends on an **MVP-scoped slice**: only the canon the
  beach→road→gate slice and guardrails need. Rest is author-canon / V1, parked.
- ✅ **Status — drafted** (`lore_bible.md`): Setting · Geography · The Frame · Factions & Peoples · Timeline & Calendar · Tone & Register · Glossary. Two-tier discipline held throughout — author-only canon stays out of every section.
- ✅ **Two tiers by location** (§5.12): agent-readable abstract lore in repo `lore/`
  where lore-reviewer/narrative-writer load it; author-only full canon outside any path
  an agent reads.
- ✅ **Format (as built):** modular markdown by domain (factions, species, geography, timeline,
  the-frame, tone, glossary), canon-status tags, deferred material marked. Guardrail-
  critical facts (abstract Hájje heritage, frame's true cause incl. 7.1, tone band)
  stated explicitly. Glossary/proper-noun index seeds the IP deny-list (§5.11).
- 🟡 lore-reviewer reads on demand; small critical core may preload via `skills`/CLAUDE.md.
  Replaces the `docs/lore-bible.md` placeholder in the agent definition.