---
id: disable-the-workflow-keyword-trigger
created: 2026-06-27
status: active
supersedes: null
category: gotchas
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/issues/63725
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Disable the 'Workflow keyword trigger' So the Word 'workflow' Stops Launching Agents

## TL;DR

Saying the word 'workflow' in any prompt was spuriously launching the dynamic Workflow tool (burning quota); a /config 'Workflow keyword trigger' setting now disables just the keyword trigger while keeping the feature available for explicit use.

## Why it matters

Confirmed gotcha (issue #63725): 'workflow' is a common English/UX/CI word, so keying off it auto-spawned multi-agent workflows and depleted quota. The blunt `disableWorkflows` over-corrects by removing the feature entirely.

## How to apply

In /config, turn off the 'Workflow keyword trigger' setting so the word stops auto-triggering a dynamic workflow, while you can still invoke the Workflow tool explicitly.

## Related

[[use-dynamic-workflows-for-high-value-complex-work]]
