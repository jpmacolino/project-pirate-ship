# Evorath — Agent Constitution

A narrative-heavy RPG (Ren'Py + pure-Python systems) for the southern continent of
Evorath. This file is read every session. The full contract is `evorath-mvp-spec-draft.md`;
this is the operating summary.

## How this repo is built (§2)
- **One prompt per release.** Work the whole MVP unsupervised, then stop for human review.
  You do not declare the work shipped — only the human does. Test output never authorizes that.
- **Git history is the review surface.** One logical change per commit; conventional commit
  messages (`feat/fix/chore(scope): ...`); auto-commit as you go.
- **Commit gate.** No commit lands unless the DoD battery passes. It runs in `.githooks/pre-commit`.
  Do not bypass it (`--no-verify` is blocked).

## Architecture (§3, §4)
- Narrative lives in `.rpy` (declarative). All mechanics live in pure Python under
  `game/systems/` — the layer humans audit.
- **Narrative reaches mechanics ONLY through the API:** `check`/`check_skill`, `adjust_stat`,
  `set_flag`/`has_flag`, `add_item`/`has_item`. Never import systems internals into `.rpy`.
- **Content is DATA, not code.** Species/classes/origins/traits/items are entries in
  `game/data/`. New content is a data edit; the builder code never changes.

## The four agents
- `systems-engineer` — mechanics + tests (its critic is pytest; correctness is mechanical).
- `narrative-writer` — `.rpy`, chargen, the beach->road->gate beats. Hands each beat to `lore-reviewer`.
- `lore-reviewer` — read-only semantic critic vs. the lore bible (catches what a deny-list can't).
- `dod-runner` — the deterministic DoD tooling.
The narrative agent is **not** its own lore judge.

## Hard rules (also enforced by hooks/linters — write clean anyway)
- **No image generation, ever** (§5.7). You have no such tool. Reference only existing assets
  in `game/images` / `game/audio`. A missing referenced asset fails the build.
- **No proprietary named IP** (§5.11). Mechanics are free; named expression is not.
- **Haejje heritage stays abstract** — feared/tragic, never graphic (§5.12).
- **Advantage/disadvantage = net sign, count don't stack** (§5.10). Skills move the number;
  traits/situation toggle advantage. Every applied adv/disadv carries a player-visible label.

## Definition of Done (§6) — run `/dod`
pytest green · renpy lint clean · all 6 paths (3 species x 2 classes) reach the gate ·
save/load works · at least one creation flag alters a branch and NO orphan mechanical flags ·
every referenced asset exists.

## Still open (don't invent answers)
7.1 what physically sank the ship · 7.4 camp name · 7.5 creation math · 7.7 skill/trait
names+counts · 7.9 nat-20/nat-1. If a beat depends on one of these, flag it, don't guess.
