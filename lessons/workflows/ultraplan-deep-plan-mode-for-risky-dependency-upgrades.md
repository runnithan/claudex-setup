---
id: ultraplan-deep-plan-mode-for-risky-dependency-upgrades
created: 2026-04-25
status: superseded
supersedes: null
category: workflows
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-ultra-plan-for-claude-code_20260424.txt
superseded_by: ultraplan-variant-is-server-ab-tested-extract-deep-prompt-as-skill
---

# Use /ultraplan for Dependency Upgrades and High-Blast-Radius Changes

## TL;DR

/ultraplan spins up 4 subagents on the cloud (code archaeologist, file finder, risk identifier, critique reviewer) for a deeper plan than local mode.

## Why it matters

For changes affecting many files simultaneously (dependency upgrades, major refactors), the deep-plan variant of Ultraplan spawns four subagents: one to understand existing architecture, one to find all files needing modification, one to identify risks and dependencies, one to critique the plan for missing steps. This catches more potential issues than local plan mode for high-blast-radius changes. It is also 2x faster than local plan mode.

## How to apply

Type `/ultraplan [your prompt]` to launch. A web session URL is provided; visit it to see the plan with inline comment capability. Leave comments on specific sections, press 'Approve plan', then either run in cloud or teleport back to terminal. Alternatively, from local plan mode, select 'Refine with Ultraplan on Claude Code web' to validate an existing local plan. Use only for high-risk dependency migrations, major refactors, or changes with uncertain blast radius, not for routine changes where local plan mode is fine.
