# Evorath RPG — V1 Build Spec (Working Draft)

> **Status legend:** ✅ Settled · 🟡 Proposed (needs confirmation) · ❓ Open question · 📌 Bookmarked / not-yet-worked
>
> This is the **V1 release contract** — the second autonomous run (§2 of the MVP spec: one prompt per release). Threads are fleshed out collaboratively, one at a time, exactly as MVP was — not pre-decided. **§3 is worked; §§1, 2, 4–6 remain skeletal** (structure, scope-pointers, and references into the MVP spec) until taken up in turn.

> **── RELATIONSHIP TO THE MVP SPEC (read first) ──**
> **Non-destructive extraction.** `evorath-mvp-spec-draft.md` stays **wholly intact** as the
> as-built MVP record — nothing is removed from it. This doc is **additive**: it adopts the
> V1-scoped design that had accreted inside the MVP spec. For now it *references* MVP §-numbers
> rather than copying their text (avoids drift); full per-thread detail is extracted into this
> doc **as each thread is worked**, leaving the MVP original in place.
> **Extraction criterion = V1 *scope*, not "not yet built."** Unbuilt MVP items are finished as
> MVP, never extracted. (The trap that caused the untidiness: the consequence work straddling
> MVP §5.4/§5.5 and V1 §7.14.)

> **── HANDOFF / CURRENT STATE ──**
> **MVP: DONE** (oracle-validated — six paths clean incl. Hájje+Mage; full combination playthrough
>   coverage; deterministic §6 checks gate-enforced). MVP spec frozen as as-built record.
> **This session:** §3 continuity registry **shape designed** — entity-anchored, location-∪-NPC
>   (nested), bidirectional (set-site + check-site obligations), inference-first off the §5.7 naming
>   conventions. Instantiation (registry/check/reviewer files) deferred to environment-assembly.
> **Next:** the two-task consequences — road carry-flag + gate welcome/refusal (`camp_welcome`) —
>   authored against this scaffold (§4 failure-consequence teeth).
> **Open in §3:** offscreen-mention enforcement (3.4); reviewer subagent-vs-stance (3.6); concrete
>   schema fields/format (3.6); registry scaling beyond hand-declared obligations (V2+).

---

## 1. Purpose & Scope

📌 V1 opens the game out from the one-chapter MVP slice toward the §1-vision long game: the opening
area becomes explorable, the rolls gain mechanical teeth, and the systems deferred at MVP (stat
redesign, progression, inventory) come online. Concrete V1 scope boundary is set as threads below
are worked — **not assumed here.**

---

## 2. Carried From MVP — Settled Design, Awaiting V1 Build

> These are **design-settled** in the MVP spec and queued as **V1 build work** (Claude Code).
> Listed by MVP §-reference; we extract full detail per thread when each is dispatched.

- ✅ **Kernel reconciliation** — `resolve_check` attribute term → `ceil(attribute/2)`, cap +5; binary skills → three trained tiers (Skilled/Adept/Masterful, +2/+4/+6). *(MVP §5.9 ⚠️ build-reconciliation; the MVP code still runs full-value attrs + single-rank skills by design.)*
- ✅ **Progression** — 27→37 attribute budget, +1 attr on each even level, level cap 20, horizontal-only beyond. *(MVP §7.11 + Creation/Growth notes.)*
- ✅ **Viewable character sheet** — the V1 build surfaces the sheet. *(MVP §7.11 build note.)*
- ✅ **Inventory & encumbrance** — capacity `base + (STR×5) + racial_mod`; abstract integer weights; bundled light tier; single hard cap; wreck-supply reward detailing. *(MVP §7.15 — whole section is V1.)*

---

## 3. FOUNDATIONAL THREAD — Persistent Continuity / World-State Registry

> Raised and worked this session. **Upstream of every content thread below** — they assume it exists.
> Environment work (the cage), not game content. Three coupled layers around one shared artifact (the
> registry), designed as a unit because the registry's fields depend on what the check keys on and what
> the reviewer reads.

**Problem.** The state *mechanism* already works — flags on the picklable `GameState`, set/has,
persisted across save/load by Ren'Py's store. What is **not** guaranteed is that an autonomous builder,
authoring a scene many hours of content later, remembers to honor a flag set earlier; that past state
won't fit its context. Long-range callbacks are not enforced. (Ren'Py contributes only *adjacent*
primitives — `Character` = speaker, show-tag = sprite, store = save. A reactive *entity that remembers*
is ours to define in the pure-Python layer; §9.8's "`game/systems/` must never `import renpy`" keeps it
engine-independent and pytest-testable.)

**Principle (MVP §9.1).** Continuity is a property of the repo, not the agent's memory.

### 3.1 What enters the registry — ✅
Persistent / cross-scene flags only. Transient flags (set and consumed in the same chapter — e.g. the
road carry-flag, steady/worn) stay out; they carry no long-range obligation.

### 3.2 Obligation anchor — ✅ entity-anchored
Obligations are carried by **entities**, not announced by flags. Continuity is something entities
*carry* ("the lookout recognizes you"), and entity-anchoring gives the check its cleanest shape —
"every scene at entity E references E's flags" — versus scanning every flag for the places it mentions
and scattering the obligation across flag definitions.

### 3.3 Granularity — ✅ location ∪ NPC, nested
"NPCs live in locations." A flag attaches at the level it belongs to: `camp_welcome` is
**location-level** (the camp); "insulted the lookout" is **NPC-level**. A scene resolves the **union**
of its location's flags and the flags of whichever NPCs are present. Nesting handles edges for free —
NPC flags travel with the NPC (he remembers even elsewhere); location flags stay bound to the place.
*(Location hierarchy — region > camp > threshold — is a later extensibility option; V1 uses flat
single-locations.)*

### 3.4 How the check learns location + presence — 🟡 inference-first
The check fires only if it knows a scene's location and who is present. We get this almost for free from
the §5.7 content-naming conventions: background name = location (`bg_camp_edge` → camp); sprite show-tag
/ speaking Character = present NPC (`show lookout`). So the check **infers** the obligation set from
constructs CC already writes — no new annotation it might forget; the content-based naming does double
duty as continuity signal. **Residual gap:** an NPC *mentioned but not shown* (offscreen reference)
escapes inference; an explicit tag is the backstop. Model = inference-first, explicit-tag-where-
inference-can't-see. *(Open: whether to enforce offscreen mentions in V1 — low-stakes given the camp's
few entities.)*

### 3.5 Bidirectional obligations — ✅ ("how do we ensure CC always authors flags?")
Two failure modes, not one:
- **Honoring** an existing flag (return-to-camp) — registry + deterministic check cover this fully.
- **Creating** the flag — harder; "this moment deserved a persistent flag" isn't detectable from code
  after the fact.

We do **not** trust CC to *decide* when a flag is needed. Consequential decision points are a
human-owned design artifact (same status as the DoD itself, §9.1), recorded as **set-site obligations**
("the gate diplomacy outcome sets `camp_welcome`"). The check then enforces **both** directions —
set-sites set, check-sites honor. CC authors *against* declared obligations, never inventing them.
**Honest limit:** airtight only for *declared* consequences. A genuinely unforeseen one falls through
the deterministic net; the semantic reviewer (3.6) is a best-effort backstop, not a floor. The goal is
not "CC never misses a flag" (unachievable) but "every *designated* consequence is enforced mechanically,
and the reviewer catches a meaningful share of the rest."

### 3.6 The three layers — shape settled, instantiation deferred
- 🟡 **Registry** — machine-readable manifest. Fields it must carry: flag · owning entity · level
  (location/NPC) · set-site obligation · check-site scope. **Schema + check = the cage** (designed now,
  written at environment-assembly against settled V1 design — writing it today would drift). Registry
  **entries = filled during the build** as content is authored. Cage here, contents there (§9.7).
- 🟡 **DoD check** — deterministic enforcement of *both* obligation directions; extends
  `evorath_checks/`; PASS/SKIP/FAIL per MVP §9.5.
- 🟡 **Continuity reviewer** — semantic critic for missed callbacks a check can't see.
  *(Open: a 5th subagent vs. a stance added to `lore-reviewer`.)*

### 3.7 First worked example — the camp / lookout
`camp_welcome` (False = refused) is the registry's first record; the camp is the first
location-entity, the lookout the first NPC-entity nested in it. **Chat/build line:** we declare the
obligation here (the seam); CC authors the flag-set and the branching scenes during the run.

**Still to pin:** 3.4 offscreen enforcement · 3.6 reviewer subagent-vs-stance · 3.6 concrete schema
fields/format/location · registry scaling beyond hand-declared obligations (V2+, not V1).

---

## 4. 📌 Open V1 Threads — Content  *(each worked individually)*

- 📌 **Failure-consequence teeth** — give the Endurance/Diplomacy rolls real outcomes: road carry-flag
  (steady/worn) and gate **welcome/refusal** branch. *(Reclassified V1 — MVP ships these rolls
  consequence-light. MVP §5.4 / §5.5.)* Includes the **nat-20-under-disadvantage legibility** revisit
  (below, §5) — bites hardest once a roll gates an outcome.
- 📌 **Per-NPC trait-interaction system** — generalize the MVP's one hardcoded disposition into
  per-NPC reactions keyed to player traits. *(MVP §7.10.)*
- 📌 **Road→camp walk expansion** — longer trek with its own local exposure/terrain/fatigue
  consequence surface. *(MVP §7.14.)*
- 📌 **Adult-background → lifepath** — grow the single background question into a richer history
  lifepath (data additions). *(MVP §7.12.)*
- 📌 **Open-area exploration & town build-out** — the camp/opening area becomes explorable; the
  "town is a V1 problem." *(MVP §5.5, §8 non-goals.)*
- 📌 **Expression-variant sprites** — `lookout wary` etc. *(MVP §5.7 sprite convention.)*
- 📌 **Subclass branching · romance/relationship systems** — from §8 non-goals, as/if scoped into V1.

---

## 5. 📌 Open V1 Threads — Systems  *(each worked individually)*

- 📌 **INT/CHA non-combat secondary** — the "reach-10" lever (e.g. INT → ability capacity; CHA →
  Momentum/rapport). Design before the V1 prompt locks. *(MVP §7.11 open thread.)*
- 📌 **Exact creation math** — attribute bases, free-point pools, inventory base (15 vs 20) — focused
  systems pass against the authored content. *(MVP §7.5b / §7.15.)*
- 📌 **Skill set finalization** — derive the real skill list from the written slice; no orphan/dormant
  stats. *(MVP §7.7.)*
- 📌 **Overlap rule** — ratify redirect vs. stack (*leaning redirect*). *(MVP §7.5a.)*
- 📌 **Nat-20-under-disadvantage legibility** — confirmed behavior (takes lower die) is correct for
  MVP; revisit for legibility (§5.10) once the roll gates welcome/refusal. *(Pairs with §4
  failure-consequence teeth.)*

---

## 6. Build-Environment Implications (V1)

> Tracked alongside the threads; firm up as design settles. *(MVP §7.13 / §9.)*
- 📌 Continuity registry + DoD check + reviewer (from §3).
- 📌 Inventory/sheet DoD checks (weight band, bundle_size, capacity floor invariant). *(MVP §7.15.)*
- 📌 No-orphan-**stats** check — every confirm-screen stat earns a slice moment. *(MVP §7.13b.)*
- 📌 `/new-origin`-style data-scaffold workflow revisit. *(MVP §9.7 / §7.12.)*

---

*§3 worked; remaining threads skeletal. The file grows by extraction as each is taken up.*