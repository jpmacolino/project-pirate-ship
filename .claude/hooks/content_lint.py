#!/usr/bin/env python3
"""PostToolUse hook (Edit|Write): IP + content guard on narrative files.

Fires right after the agent writes a .rpy, so violations are caught at
authoring time — before they ever reach a commit. Non-.rpy writes pass through.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from evorath_checks import ip_content  # noqa: E402

def main():
    data = json.load(sys.stdin)
    path = data.get("tool_input", {}).get("file_path", "")
    if not path.endswith(".rpy"):
        sys.exit(0)
    findings = ip_content.scan_file(path)
    if findings:
        reason = "Content guardrail violation(s):\n" + "\n".join(f"  {f}" for f in findings)
        reason += ("\nNamed IP is forbidden (§5.11); Haejje heritage stays abstract, "
                   "never graphic (§5.12). Rewrite before continuing.")
        print(json.dumps({"decision": "block", "reason": reason}))
        return
    sys.exit(0)

if __name__ == "__main__":
    main()
