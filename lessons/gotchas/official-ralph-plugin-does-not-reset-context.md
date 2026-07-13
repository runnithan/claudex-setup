---
id: official-ralph-plugin-does-not-reset-context
created: 2026-07-02
status: active
supersedes: null
category: gotchas
sources:
  - transcripts/sean-kochel/how-to-run-a-ralph-loop-step-by-step_7TwIrPQnFfg_20260702.txt
---

# Know the Official Ralph/Loop Plugin Doesn't Reset Context Each Iteration

## TL;DR

Per the creator, the official Ralph/loop plugin isn't a true Ralph loop because it doesn't spawn a fresh context window each iteration.

## Why it matters

The defining property of a Ralph loop is a clean context window per pass that reads only the task file's state. Without it you get context accumulation, not a true loop — so the "loop" degrades over iterations the way a single long session does.

## How to apply

For genuine context-reset loops use a bash script or a managing tool like `ralph-tui` (`bun install -g ralph-tui`) rather than the official plugin. `ralph-tui` also gives a guided create-PRD → task-list flow and a per-run iteration cap you can raise/lower to pull the plug when it stalls. Verify any loop tool actually starts a fresh window per pass before trusting it for long autonomous runs.

## Related

[[autonomous-ui-loop-acceptance-must-exercise-rendered-ui]], [[match-autonomous-loops-to-disposable-or-verifiable-work]], [[loops-as-abstraction-over-prompts]]
