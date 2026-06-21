---
id: disallowed-tools-in-skill-frontmatter
created: 2026-06-21
status: active
supersedes: null
category: skills
source_type: canonical
sources:
  - https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
---

# Strip Tools From the Model While a Skill Runs with `disallowed-tools` Frontmatter

## TL;DR

Skills and slash commands can set `disallowed-tools` in frontmatter to remove specific tools from the model for the duration the skill is active — narrower than a global deny rule, scoped to just that workflow.

## Why it matters

The changelog adds `disallowed-tools` frontmatter that removes tools from the model while the skill is active. This lets a read-only or side-effect-free skill guarantee it can't (e.g.) Edit/Write or spawn agents, without touching project-wide permissions.

## How to apply

In a `SKILL.md` or command frontmatter add `disallowed-tools: Edit, Write, Agent` so those tools vanish from the model only while that skill is active. Use it to enforce read-only research skills or keep a focused command from wandering.

## Related

[[context-fork-for-isolated-skill-execution]], [[skill-md-under-200-lines-progressive-disclosure]]
