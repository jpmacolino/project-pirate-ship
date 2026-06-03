#!/usr/bin/env python3
"""Definition-of-Done battery (§6) — the single source of truth.

Run by /dod, the git pre-commit hook (hard gate), and the Stop hook (give-up
policy). Each check is independent so partial failures are legible.

  python scripts/run_dod.py            # full battery, human-readable
  python scripts/run_dod.py --json     # machine-readable (used by the Stop hook)
  python scripts/run_dod.py --static   # skip pytest/renpy (fast, content-only)

Outcomes per check:
  PASS  the check ran and is clean
  SKIP  the tool or its inputs don't exist yet (bootstrap) — loud, does NOT block
  FAIL  the thing is present and broken — blocks the commit

Exit code 0 = no failures (skips are fine), nonzero = at least one FAIL.
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evorath_checks import config, ip_content, flags, assets, layer  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str]) -> tuple[int | None, str]:
    """Returns (returncode, combined output). returncode is None when the
    command itself can't be found (e.g. the tool isn't installed)."""
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=900)
        return p.returncode, (p.stdout + p.stderr).strip()
    except FileNotFoundError:
        return None, f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"timed out: {' '.join(cmd)}"


def battery(static_only: bool = False) -> tuple[dict[str, list[str]], dict[str, str]]:
    results: dict[str, list[str]] = {}   # check -> failure messages (empty = not failing)
    skipped: dict[str, str] = {}         # check -> reason (loud, non-blocking)

    # --- static content checks (always run; stdlib only) ---
    results["ip_and_content"] = [str(f) for f in _scan_all_ip()]
    results["orphan_flags"] = flags.check(ROOT)
    results["missing_assets"] = assets.check(ROOT)
    results["layer_contract"] = layer.check(ROOT)

    if static_only:
        return results, skipped

    # --- pytest ---
    rc, out = _run([sys.executable, "-m", "pytest", "-q"])
    if rc == 0:
        results["pytest"] = []
    elif rc == 5:                                       # pytest: no tests collected
        results["pytest"] = []
        skipped["pytest"] = "no tests collected yet"
    elif rc is not None and "No module named pytest" in out:
        results["pytest"] = []
        skipped["pytest"] = "pytest not installed (pip install pytest)"
    else:
        results["pytest"] = [out or "pytest failed"]

    # --- renpy lint ---
    has_rpy = any(list(ROOT.glob(g)) for g in config.NARRATIVE_GLOBS)
    if not has_rpy:
        results["renpy_lint"] = []
        skipped["renpy_lint"] = "no .rpy files yet"
    else:
        rc, out = _run(config.renpy_cmd() + [".", "lint"])
        if rc is None:
            results["renpy_lint"] = []
            skipped["renpy_lint"] = "Ren'Py SDK not found (set RENPY_SDK or add renpy to PATH)"
        else:
            results["renpy_lint"] = [] if rc == 0 else [out or "renpy lint failed"]

    # TODO: 6-path headless playthrough + save/load (scripts/playthrough.py),
    # authored during the build; SKIP until it exists.
    return results, skipped


def _scan_all_ip():
    found = []
    for g in config.NARRATIVE_GLOBS:
        for f in ROOT.glob(g):
            found.extend(ip_content.scan_file(f))
    return found


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    static_only = "--static" in argv
    results, skipped = battery(static_only=static_only)
    failed = {k: v for k, v in results.items() if v}

    if as_json:
        print(json.dumps(
            {"passed": not failed, "results": results, "skipped": skipped}, indent=2))
        return 0 if not failed else 1

    print("=" * 60)
    print("Evorath — Definition of Done")
    print("=" * 60)
    for name, errs in results.items():
        mark = "FAIL" if errs else ("SKIP" if name in skipped else "PASS")
        note = f"  ({skipped[name]})" if name in skipped else ""
        print(f"  [{mark}] {name}{note}")
        for e in errs[:25]:
            print(f"         - {e}")
    print("-" * 60)
    if failed:
        print(f"{len(failed)} check(s) failing")
    elif skipped:
        print(f"ALL GREEN ({len(skipped)} skipped — see notes)")
    else:
        print("ALL GREEN")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))