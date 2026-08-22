---
id: loops-as-abstraction-over-prompts
created: 2026-06-11
status: active
supersedes: null
category: workflows
sources:
  - transcripts/ray-amjad/how-the-top-1-actually-run-claude-code-now_20260610.txt
---

# Design Loops as the Unit of Work, Not Prompts

## TL;DR

Stop thinking in individual prompts and start designing self-contained loops, input (spec) → build → test/review → fix → output, with persisted memory and an explicit exit condition, then compose outer loops that feed work into inner loops.

## Why it matters

Manual prompting keeps you inside the loop as its scheduler and memory. When the loop itself is the designed artifact (inputs, checks, memory file/channel, exit condition), you design it once and step back; the system runs unattended and survives session boundaries because decisions live in files, not in your head.

## How to apply

For a recurring job, write down the loop contract: what spec it consumes, what actions it takes, what check decides pass/fail, where it records what it did (a log file, thread, or Slack channel), and what condition ends it (e.g., "passed code review twice"). Implement it with the primitives you already have, `/loop`, `/goal`, scheduled routines, or a GSD phase. Then build outer loops that produce specs for it (e.g., a weekly routine that scans for new issues and queues them as specs for the build loop).
