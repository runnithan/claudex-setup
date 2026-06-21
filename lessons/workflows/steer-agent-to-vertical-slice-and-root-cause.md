---
id: steer-agent-to-vertical-slice-and-root-cause
created: 2026-06-21
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://martinfowler.com/articles/exploring-gen-ai/13-role-of-developer-skills.html
---

# Steer the Agent Toward a Vertical Slice and Root Cause, Away From Brute-Force Fixes

## TL;DR

Watch for three failure patterns mid-task — premature broad implementation, brute-force symptom fixes, and confident misdiagnosis — and redirect Claude toward one validated slice and the underlying cause.

## Why it matters

Thoughtworks' field observations show supervised agents reliably drift into these traps (converting all UI components at once instead of one vertical slice; bumping a memory setting instead of asking why memory is high; blaming Docker architecture settings when the real cause was node_modules built for the wrong arch). Left alone, the agent ships breadth without depth and patches symptoms.

## How to apply

When Claude proposes a sweeping change, make it do one component end-to-end (a vertical slice that integrates with the backend) and prove it before fanning out. When it reaches for a knob, make it state the root cause first. Stop the session when you feel overwhelmed — revise the prompt and start fresh, or fall back to manual.

## Related

[[finish-every-migration-you-start]], [[save-checkpoint-reset-on-drift]]
