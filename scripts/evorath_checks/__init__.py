"""Shared check logic for the Evorath build environment.

Imported by both the Claude Code hooks (.claude/hooks/) and the deterministic
DoD battery (scripts/run_dod.py). Keeping the logic here means the fast-feedback
hook and the authoritative git/pre-commit gate run *identical* checks.
"""
