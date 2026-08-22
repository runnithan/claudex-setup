---
id: model-selection-opus-sonnet-haiku-use-cases
created: 2026-04-25
status: active
supersedes: null
category: model-selection
sources:
  - transcripts/ray-amjad/huge-claude-code-update-opus-4-5-desktop-app-more_20260307.txt
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-that-makes-sonnet-feel-like-opus_20260424.txt
  - transcripts/ray-amjad/my-claude-code-workflow-for-2026_20260307.txt
  - transcripts/simon-scrapes/every-claude-code-workflow-explained-u0026-when-to-use-each_20260424.txt
---

# Match the Model to the Task: Opus for Planning/Reasoning, Sonnet for Execution, Haiku for Bulk

## TL;DR

Use /model opusplan to run Opus only in plan mode; Sonnet handles execution; Haiku for read-only subagents. The advisor tool escalates automatically.

## Why it matters

Opus 4.5/4.6 is the best model for complex reasoning, planning, and ambiguous problems but costs more. Sonnet 4.5/4.6 is fast and capable for implementation tasks. Haiku is cheap and fast for read-only tasks (the built-in Explore subagent uses Haiku). The advisor tool lets Sonnet stay in execution mode and only escalate to Opus (or a more powerful future model) when truly stuck.

## How to apply

Use `/model opusplan` to set Opus for plan mode only, Sonnet for everything else. For intensive sessions, use Opus throughout but switch to Sonnet for quick fixes. For subagents that only explore/read, specify Haiku in the agent frontmatter. Enable `/advisor` to configure an advisor model (Opus or stronger) that Sonnet calls when stuck, it sees the full conversation history and returns structured feedback. Combine with `ultrathink` prefix to increase reasoning budget on hard problems.
