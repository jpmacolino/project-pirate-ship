#!/usr/bin/env python3
"""Definition-of-Done battery (§6) — the single source of truth.

Run by /dod (ergonomic readout), the git pre-commit hook (hard gate), and the
Stop hook (give-up policy). Each check is independent so partial failures are
legible.

  python scripts/run_dod.py            # full battery, human-readable
  python scripts/run_dod.py --json     # machine-readable (used by the Stop hook)
  python scripts/run_dod.py --static   # skip pytest/renpy (fast, content-only)

Exit code 0 = all green, nonzero = at least one failure.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evorath_checks import config, ip_content, flags, assets, layer  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str]) -> tuple[bool, str]:
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=900)
        return p.returncode == 0, (p.stdout + p.stderr).strip()
    except FileNotFoundError:
        return False, f"command not found: {cmd[0]} (skipped — install or set PATH)"
    except subprocess.TimeoutExpired:
        return False, f"timed out: {' '.join(cmd)}"


def battery(static_only: bool = False) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {}

    # --- static content checks (always run) ---
    ip = [str(f) for f in _scan_all_ip()]
    results["ip_and_content"] = ip
    results["orphan_flags"] = flags.check(ROOT)
    results["missing_assets"] = assets.check(ROOT)
    results["layer_contract"] = layer.check(ROOT)

    if static_only:
        return results

    # --- dynamic checks ---
    ok, out = _run([sys.executable, "-m", "pytest", "-q"])
    results["pytest"] = [] if ok else [out or "pytest failed"]

    ok, out = _run(config.renpy_cmd() + [".", "lint"])
    results["renpy_lint"] = [] if ok else [out or "renpy lint failed"]

    # TODO: 6-path headless playthrough + save/load (scripts/playthrough.py).
    # Stubbed until narrative content exists (depends on 7.1, 7.7).
    return results


def _scan_all_ip():
    found = []
    for g in config.NARRATIVE_GLOBS:
        for f in ROOT.glob(g):
            found.extend(ip_content.scan_file(f))
    return found


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    static_only = "--static" in argv
    results = battery(static_only=static_only)
    failed = {k: v for k, v in results.items() if v}

    if as_json:
        print(json.dumps({"passed": not failed, "results": results}, indent=2))
        return 0 if not failed else 1

    print("=" * 60)
    print("Evorath — Definition of Done")
    print("=" * 60)
    for name, errs in results.items():
        mark = "PASS" if not errs else "FAIL"
        print(f"  [{mark}] {name}")
        for e in errs[:25]:
            print(f"         - {e}")
    print("-" * 60)
    print("ALL GREEN" if not failed else f"{len(failed)} check(s) failing")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
