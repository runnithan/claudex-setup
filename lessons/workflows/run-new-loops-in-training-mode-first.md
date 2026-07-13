---
id: run-new-loops-in-training-mode-first
created: 2026-07-01
status: active
supersedes: null
category: workflows
sources:
  - transcripts/austin-marchese/stop-prompting-claude-start-loop-engineering_YAS4ojuhbW4_20260628.txt
---

# Run a New Loop in Training Mode (Pause-and-Approve Each Step) Before Unleashing It

## TL;DR

When you first run a new loop or loop-orchestrating skill, gate it behind a `training_mode` flag that makes it pause and ask for approval before each major action. Validate the logic over a couple of runs, then flip the flag off and let it run unattended — so a wrong condition or off-by-one doesn't burn tokens (or fire real side effects) across a whole batch.

## Why it matters

Loops act autonomously and at volume, so a subtle logic error — bad filter, wrong stop condition, mis-scoped write — doesn't fail once, it fails N times. For loops that hit APIs, send emails, or write to a database, those are real and sometimes costly side effects. A single per-step approval checkpoint during break-in catches the mistake before it compounds.

## How to apply

Add a `training_mode: true` flag at the top of the loop skill. When set, the loop prints "About to [action] — approve to continue?" before each batch-affecting step and waits; you approve, skip, or stop to debug. After 2-3 clean runs, set `training_mode: false` (in the skill or CLAUDE.md) and let it run unattended. Keep it strict for loops that make external calls, spend money, or mutate persistent state. Complements the "verifiable finish line + safety cap" rule for `/goal`: the cap bounds runaway, training mode validates correctness first.
