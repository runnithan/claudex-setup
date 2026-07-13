---
id: effort-control-for-token-intensive-work
created: 2026-06-11
status: superseded
supersedes: null
superseded_by: max-effort-is-a-trap-quality-plateaus-at-high
category: commands
sources:
  - transcripts/tristen-o-brien/claude-just-dropped-opus-4-8-master-it-in-6-minutes_20260610.txt
---

# Use /effort to Match Thinking Depth to Task Risk

## TL;DR

`/effort` sets how deeply the model reasons: low is fast and shallow, the default is high, and extra-high/max are slower but markedly more careful — switch up for risky or complex changes, back down for routine ones, and check the cost with `/usage` afterwards.

## Why it matters

Effort is a per-task dial, not a set-and-forget setting. Running max effort on trivial edits wastes time and tokens; running low effort on intricate logic ships missed edge cases. Deliberately matching the dial to the blast radius of the change gets both speed and care where each belongs.

## How to apply

Before a risky change (migrations, auth, concurrency, tricky refactors), run `/effort` and pick extra-high or max; drop back to the default for everyday work. Pair with `/usage` after heavy runs to learn what each effort level actually costs on your tasks, so the choice becomes calibrated rather than guessed.
