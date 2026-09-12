#!/usr/bin/env python3
"""PreToolUse[Bash] guard: block destructive git push forms.

The permissions.deny prefix patterns in settings.json catch the common spellings
(`git push --force`, `git push -f`, and the four added beside them), but a prefix
pattern cannot see a flag written after the remote (`git push origin --force`) and
cannot express a refspec shape at all (`+main`, `:old-branch`). This hook closes
both, so the deny list stays as the cheap first tier and this is the durable one.

Deliberately scoped to DESTRUCTIVE forms only. A plain `git push` is untouched: a
hook cannot tell whether the owner approved in the current turn, and blocking
ordinary pushes would make the guard something people switch off.
"""
import json
import re
import sys

DESTRUCTIVE = ("--force", "--force-with-lease", "--delete", "--mirror", "--prune")


def block(segment):
    sys.stderr.write(
        "Destructive git push blocked: " + segment + "\n"
        "Force, delete, mirror, prune and rewritten-refspec pushes rewrite or destroy "
        "remote history, which no local undo recovers. Report what you wanted to run "
        "and why, and let the owner run it.\n")
    sys.exit(2)


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        sys.exit(0)
    if data.get("tool_name", "") != "Bash":
        sys.exit(0)
    command = data.get("tool_input", {}).get("command", "")
    for segment in re.split(r"[;&|]{1,2}|\n", command):
        segment = segment.strip()
        if not re.match(r"^git\s+(-\S+\s+\S*\s*)*push\b", segment):
            continue
        args = segment.split()
        after = args[args.index("push") + 1:] if "push" in args else []
        if any(a in DESTRUCTIVE for a in after) or "-f" in after:
            block(segment)
        for a in after:
            if a.startswith("+") or a.startswith(":"):
                block(segment)
    sys.exit(0)


if __name__ == "__main__":
    main()
