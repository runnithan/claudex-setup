---
id: nest-skills-per-subproject-with-dir-qualified-names
created: 2026-06-27
status: active
supersedes: null
category: skills
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Put Skills in Nested .claude/skills Dirs in a Monorepo; Use dir:name on Clashes

## TL;DR

Skills in nested `.claude/skills` directories now load when you're working on files in that subtree, and on a name clash the nested skill becomes addressable as `<dir>:<name>` so both stay available.

## Why it matters

In a monorepo you can now scope skills to a subproject instead of cramming everything into the repo-root .claude/skills, and a subproject can override or coexist with a same-named root skill.

## How to apply

Place subproject-specific skills under that subproject's `.claude/skills/`; when two skills share a name, invoke the nested one with its directory-qualified `<dir>:<name>` form. Per changelog 2.1.178.

## Related

[[skill-md-under-200-lines-progressive-disclosure]]
