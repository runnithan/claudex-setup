---
id: save-checkpoint-reset-on-drift
created: 2026-06-07
status: active
supersedes: null
category: workflows
sources:
  - transcripts/simon-scrapes/how-anthropic-teams-actually-use-claude-code-day-to-day-for-non-engineers_20260607.txt
---

# Save Checkpoints Frequently and Reset (Not Rescue) When Sessions Drift

## TL;DR

Save state after each major step, let Claude run, then either accept or start completely fresh, don't try to correct a drifting session mid-flight.

## Why it matters

Anthropic's engineering, data science, and product teams report Claude nails it on the first try only ~33% of the time. Restarting fresh from a checkpoint after a bad output has a higher success rate than rescuing a drifting session through corrective prompts. Extends `rewind-instead-of-arguing-with-stale-context` with the checkpoint discipline that makes resets cheap.

## How to apply

Save checkpoints (git commits or session snapshots) after each major step. If output starts to drift from your goals, wrong structure, off-topic tangents, use `/rewind` to go back to the last checkpoint and restart with a slightly different prompt rather than iteratively correcting. The reset feels wasteful but is faster in practice.
