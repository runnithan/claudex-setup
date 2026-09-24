#!/usr/bin/env python3
"""
Validate that the repo's SHIPPED config artifacts are well-formed.

This is a structural sanity check, not a schema validator: it confirms the
artifacts a user copies into their `.claude/` (agents, skills, commands) carry
the frontmatter Claude Code needs, and that the plugin/marketplace manifests
parse as JSON with their required keys. The CI `validate` workflow does the
JSON/shell/python syntax gating; this complements it by checking *semantics*.

Stdlib only — no PyYAML. The frontmatter parser is deliberately minimal: it
reads the leading `---`-fenced block and pulls out top-level `key: value`
pairs, which is all these artifacts use.

Run from anywhere:

    python scripts/validate-artifacts.py

Exits 0 with a PASS summary if every check passes; prints each problem with its
file path and exits 1 if any check fails.
"""

import json
import sys
from pathlib import Path

# Repo root is the parent of this script's directory (scripts/).
REPO_ROOT = Path(__file__).resolve().parent.parent


def parse_frontmatter(text):
    """Minimal leading-`---` frontmatter parse.

    Returns (fields, error):
      - fields: dict of top-level `key: value` pairs (None if no frontmatter)
      - error: a string describing a malformed block, else None

    Only top-level scalar keys are captured; nested/list YAML is ignored for
    field extraction but does not count as an error.
    """
    # Normalize newlines so CRLF checkouts (Windows) parse identically.
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    if not lines or lines[0].strip() != "---":
        return None, None  # No frontmatter block.

    # Find the closing fence.
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break
    if close_idx is None:
        return None, "frontmatter opened with '---' but never closed"

    fields = {}
    for raw in lines[1:close_idx]:
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # Only treat top-level (non-indented) `key: value` lines as fields.
        if line[0] in (" ", "\t", "-"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, None


def read_text(path):
    return path.read_text(encoding="utf-8")


def check_encoding(path):
    """Flag byte-level faults that make Claude Code silently skip an artifact.

    Neither fault raises an error at load time. The file is ignored and the
    agent/skill/command simply never appears, which reads as the model
    disregarding instructions rather than as a config fault:

      - A UTF-8 BOM was silently fatal for agents, skills and commands until
        Claude Code 2.1.239. Windows editors and PowerShell's `Out-File` emit
        one by default.
      - CRLF breaks plain-scalar frontmatter (a block scalar survives it, which
        is why the damage is partial and easy to misread). Editing through the
        Windows share is enough to introduce it.

    Checked on raw bytes deliberately: parse_frontmatter() normalises both away
    so the parser stays tolerant, which would otherwise leave this validator
    reporting PASS on a file Claude Code refuses to load.

    Returns a list of human-readable problems (empty when clean).
    """
    raw = path.read_bytes()
    problems = []
    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append(
            "starts with a UTF-8 BOM (Claude Code skips the file); "
            "strip the first 3 bytes, e.g. sed -i '1s/^\\xEF\\xBB\\xBF//' <file>"
        )
    if b"\r\n" in raw:
        problems.append(
            "has CRLF line endings (breaks plain-scalar frontmatter); "
            "convert with sed -i 's/\\r$//' <file> or dos2unix"
        )
    return problems


def rel(path):
    """Repo-relative path with forward slashes, for stable cross-platform output."""
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__.strip())
        print("\nUsage: python scripts/validate-artifacts.py")
        print("Exits 0 if every artifact is well-formed, 1 otherwise.")
        return 0

    problems = []
    counts = {"agents": 0, "skills": 0, "commands": 0, "manifests": 0}

    # --- agents/*.md: require frontmatter with name + description. ----------
    for path in sorted(REPO_ROOT.glob("agents/*.md")):
        counts["agents"] += 1
        problems.extend(f"{rel(path)}: {p}" for p in check_encoding(path))
        fields, err = parse_frontmatter(read_text(path))
        if err:
            problems.append(f"{rel(path)}: {err}")
            continue
        if fields is None:
            problems.append(f"{rel(path)}: missing '---' YAML frontmatter block")
            continue
        for required in ("name", "description"):
            if not fields.get(required):
                problems.append(f"{rel(path)}: frontmatter missing '{required}:'")
        # If tools: is present, sanity-check it's a comma list or '*'.
        tools = fields.get("tools")
        if tools is not None:
            t = tools.strip()
            if t != "*" and not all(part.strip() for part in t.split(",") if t):
                problems.append(
                    f"{rel(path)}: 'tools:' must be '*' or a comma-separated "
                    f"list (got {tools!r})"
                )

    # --- skills/**/SKILL.md: require frontmatter with name + description. ---
    for path in sorted(REPO_ROOT.glob("skills/**/SKILL.md")):
        counts["skills"] += 1
        problems.extend(f"{rel(path)}: {p}" for p in check_encoding(path))
        fields, err = parse_frontmatter(read_text(path))
        if err:
            problems.append(f"{rel(path)}: {err}")
            continue
        if fields is None:
            problems.append(f"{rel(path)}: missing '---' YAML frontmatter block")
            continue
        for required in ("name", "description"):
            if not fields.get(required):
                problems.append(f"{rel(path)}: frontmatter missing '{required}:'")

    # --- .claude/commands/*.md: frontmatter optional, but must parse. ------
    for path in sorted((REPO_ROOT / ".claude" / "commands").glob("*.md")):
        counts["commands"] += 1
        problems.extend(f"{rel(path)}: {p}" for p in check_encoding(path))
        _, err = parse_frontmatter(read_text(path))
        if err:
            problems.append(f"{rel(path)}: {err}")

    # --- .claude-plugin/plugin.json: name + version. -----------------------
    plugin_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    if not plugin_path.exists():
        problems.append(f"{rel(plugin_path)}: file not found")
    else:
        counts["manifests"] += 1
        try:
            plugin = json.loads(read_text(plugin_path))
            for required in ("name", "version"):
                if required not in plugin:
                    problems.append(f"{rel(plugin_path)}: missing required key '{required}'")
        except json.JSONDecodeError as e:
            problems.append(f"{rel(plugin_path)}: invalid JSON ({e})")

    # --- .claude-plugin/marketplace.json: name + owner + plugins. ----------
    market_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    if not market_path.exists():
        problems.append(f"{rel(market_path)}: file not found")
    else:
        counts["manifests"] += 1
        try:
            market = json.loads(read_text(market_path))
            for required in ("name", "owner", "plugins"):
                if required not in market:
                    problems.append(f"{rel(market_path)}: missing required key '{required}'")
            plugins = market.get("plugins")
            if not isinstance(plugins, list) or not plugins:
                problems.append(f"{rel(market_path)}: 'plugins' must be a non-empty array")
        except json.JSONDecodeError as e:
            problems.append(f"{rel(market_path)}: invalid JSON ({e})")

    total = sum(counts.values())

    if problems:
        print(f"FAIL — {len(problems)} problem(s) found:\n", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(
            f"\nChecked {total} artifact(s): "
            f"{counts['agents']} agents, {counts['skills']} skills, "
            f"{counts['commands']} commands, {counts['manifests']} manifests.",
            file=sys.stderr,
        )
        return 1

    print(
        f"PASS — {total} artifact(s) well-formed: "
        f"{counts['agents']} agents, {counts['skills']} skills, "
        f"{counts['commands']} commands, {counts['manifests']} manifests."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
