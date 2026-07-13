---
id: skill-frequency-test-inner-loop
created: 2026-07-01
status: active
supersedes: null
category: skills
sources:
  - transcripts/austin-marchese/how-claude-code-s-creator-actually-automates-his-work_jdLFeBkiy3M_20260628.txt
---

# Apply the Inner-Loop Test Before Turning a Task Into a Skill

## TL;DR

Only build a skill if it passes all three checks: you do the task 2-3+ times a week, it follows the same pattern each time, and preloaded context (examples, rules, prior runs) would improve the output. Otherwise just re-prompt — every skill you add is maintenance debt.

## Why it matters

Skills sprawl. Each one has to be discovered, maintained, and kept from overlapping others, and a rarely-used or one-off skill adds that cost while returning almost nothing. The frequency + repeatability + context test is a cheap go/no-go filter that keeps your skill set small and high-leverage instead of a graveyard of clever-but-unused automations.

## How to apply

Before packaging a process as a skill, ask: (1) Do I actually do this 2-3+ times per week? (2) Does it follow the same shape every time (not ad-hoc)? (3) Would preloaded context — examples, gotchas, prior outputs — measurably improve the result? Build the skill only if all three are yes; if it's a once-a-month task or changes every time, re-prompt instead. This complements "one skill per specific goal" and "reverse-engineer skills from successful runs" by deciding *whether* a skill should exist at all.
