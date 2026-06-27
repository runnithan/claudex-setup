---
id: reverse-engineer-skills-from-successful-runs
created: 2026-06-27
status: active
supersedes: null
category: skills
sources:
  - transcripts/nate-herk-ai-automation/i-turned-claude-opus-4-8-into-my-entire-ai-operating-system_0WDkwMxj13s_20260627.txt
  - transcripts/nate-herk-ai-automation/higgsfield-just-turned-claude-into-a-creative-agency_xn6Z5PYyAIE_20260626.txt
---

# Reverse-Engineer Skills From Successful Runs Instead of Designing Them Up Front

## TL;DR

After Claude builds something end-to-end that you're happy with, ask it to turn that conversation into a reusable skill — capturing the actual prompt flow, tool sequence, and error handling it used.

## Why it matters

Skills designed in advance often miss the real-world decisions that made a run work. Reverse-engineering from a proven output encodes what Claude actually did, including the edge cases it handled, so the skill reproduces that quality rather than a theoretical best practice.

## How to apply

Once a task lands well, prompt: 'Extract what we just did into a skill — the exact steps, tools, and error handling — and save it under .claude/skills/<name>/.' Review and tighten the generated skill, then invoke it by name next time instead of re-deriving the workflow.

## Related

[[skill-goal-oriented-not-railroaded]], [[skills-encode-lived-experience-not-obvious-behavior]]
