---
id: match-tool-parameters-in-permission-rules
created: 2026-06-27
status: active
supersedes: null
category: permissions
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Write Permission Rules That Match Tool Parameters, e.g. Agent(model:opus)

## TL;DR

Permission rules now support `Tool(param:value)` (with `*` wildcards) to match a tool's input parameters, not just its name — so you can allow/deny by argument.

## Why it matters

Previously a rule could only allow or deny a whole tool; you couldn't, say, block Opus subagents while allowing Sonnet ones. Parameter matching makes permission rules surgical.

## How to apply

Add rules like `Agent(model:opus)` to a deny list to block Opus subagent spawns, using `*` where needed (e.g. `Tool(param:*)`). Per changelog 2.1.178: 'Added Tool(param:value) syntax for permission rules to match a tool's input parameters (with * wildcard), e.g. Agent(model:opus) to block Opus subagents.'

## Related

[[auto-mode-permissions-for-unsupervised-runs]], [[disallowed-tools-in-skill-frontmatter]]
