import json, shlex, sys

# git commit options that consume the FOLLOWING token as a value
VALUE_OPTS = {"-m", "--message", "-F", "--file", "-c", "--reedit-message",
              "-C", "--reuse-message", "-t", "--template"}

def is_bypass(cmd: str) -> bool:
    try:
        toks = shlex.split(cmd)
    except ValueError:
        toks = cmd.split()
    if "commit" not in toks:
        return False
    skip_next = False
    for tok in toks:
        if skip_next:                      # this token is a value, not a flag
            skip_next = False
            continue
        if tok in VALUE_OPTS:
            skip_next = True
            continue
        if tok == "--no-verify":
            return True
        # single-dash short cluster (-n, -nm, ...); 'n' = --no-verify for git commit
        if len(tok) > 1 and tok[0] == "-" and tok[1] != "-" and "n" in tok[1:]:
            return True
    return False