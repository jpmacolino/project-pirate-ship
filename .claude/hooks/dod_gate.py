#!/usr/bin/env python3
"""Stop hook: the human gate + give-up policy (§2).

When the agent tries to end its turn, run the DoD battery.
  - all green            -> allow stop (work is ready for human review)
  - failing, progressing -> exit 2: keep going, here's what's failing
  - failing, stuck N times-> allow stop, write BLOCKED report, flag the human

"Progress" = the set of failing checks changed since the last Stop. Same failure
set N times in a row (config.DOD_GIVE_UP_N) means we're spinning, not fixing.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".claude" / "state" / "dod_progress.json"
sys.path.insert(0, str(ROOT / "scripts"))
from evorath_checks import config  # noqa: E402

def run_battery():
    p = subprocess.run([sys.executable, "scripts/run_dod.py", "--json"],
                       cwd=ROOT, capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"passed": False, "results": {"runner": [p.stdout + p.stderr]}}

def sig(results):
    failing = sorted(k for k, v in results.items() if v)
    return hashlib.sha1("|".join(failing).encode()).hexdigest()[:12], failing

def load(): 
    try: return json.loads(STATE.read_text())
    except Exception: return {"sig": None, "count": 0}

def save(d):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(d))

def main():
    report = run_battery()
    if report.get("passed"):
        save({"sig": None, "count": 0})
        sys.exit(0)  # allow stop

    cur, failing = sig(report["results"])
    prev = load()
    count = prev["count"] + 1 if prev["sig"] == cur else 1
    save({"sig": cur, "count": count})

    summary = "; ".join(failing)
    if count >= config.DOD_GIVE_UP_N:
        out = ROOT / "BLOCKED.md"
        out.write_text(
            f"# DoD BLOCKED\n\nStuck on the same failures {count} turns running.\n\n"
            f"Failing checks: {summary}\n\n```\n{json.dumps(report['results'], indent=2)}\n```\n"
            "\nHuman review needed — see open spec questions (e.g. 7.1, 7.7).\n")
        save({"sig": None, "count": 0})
        print(json.dumps({"systemMessage":
            f"DoD blocked after {count} no-progress turns on: {summary}. "
            f"Wrote BLOCKED.md and stopped for human review."}))
        sys.exit(0)  # allow stop, flag the human

    # progressing (or new failure) -> keep working
    print(f"DoD not yet met (turn {count}). Failing: {summary}. Continue fixing.",
          file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()
