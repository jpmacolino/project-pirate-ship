# Evorath Build Environment — Scaffolding

First draft of the guardrail layer (§9 candidate). Drop this tree into your repo
root in `c:/dev/<project>/`.

## One-time setup
```
# Windows (PowerShell)
scripts/setup_hooks.ps1
# macOS/Linux/Git Bash
bash scripts/setup_hooks.sh
```
Then set `RENPY_SDK` to your Ren'Py SDK folder so `renpy lint` resolves. If `python`
isn't on PATH on Windows, change `"python"` to `"py"` in `.claude/settings.json`.

## What enforces what
| Spec rule | Where it's enforced | Strength |
|---|---|---|
| pytest + renpy lint + all checks | `.githooks/pre-commit` | hard (any commit) |
| no `--no-verify` bypass | PreToolUse hook | hard (agent) |
| IP + content guard on .rpy | PostToolUse hook + linter | hard |
| no orphan flags / missing assets / layer breaks | `run_dod.py` linters | hard |
| no image generation | tool simply absent from agents | hard (capability) |
| lore/canon consistency | `lore-reviewer` agent | semantic critic |
| commit discipline, abstract Haejje, API-only | CLAUDE.md | soft (write-clean) |

## Layout
```
CLAUDE.md                      agent constitution (read every session)
.claude/
  settings.json                hook wiring (exec-form Python, cross-platform)
  agents/                      systems, narrative, lore-reviewer, validation
  hooks/                       block_no_verify, content_lint, dod_gate (Stop), session_context
  skills/                      /dod, /playthrough, /new-origin
.githooks/pre-commit           authoritative commit gate
scripts/
  run_dod.py                   the DoD battery (one source of truth)
  playthrough.py               headless path harness (STUB until content exists)
  evorath_checks/              shared deterministic checks (config, ip_content, flags, assets, layer)
game/data/creation_data.py     §5.12 mappings as data
```

## Embedded decisions to confirm
- `config.DOD_GIVE_UP_N = 3` — Stop-hook allows stop after 3 no-progress turns (the give-up policy).
- `config.OVERLAP_RULE = "redirect"` — duplicate skill grant becomes a free pick (7.5, leaning).
- `"drow"` is on the IP deny-list as a borderline term — confirm or drop in the IP pass.
- Provisional everything tied to 7.1/7.5/7.7: creation math, skill/origin names, the playthrough harness.
