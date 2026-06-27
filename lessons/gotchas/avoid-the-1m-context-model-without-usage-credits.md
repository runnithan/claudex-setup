---
id: avoid-the-1m-context-model-without-usage-credits
created: 2026-06-27
status: active
supersedes: null
category: gotchas
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/issues/62063
  - https://github.com/anthropics/claude-code/issues/63896
---

# Without Usage Credits, Switch Off the 1M-Context Model or Sessions Wedge

## TL;DR

On plans without usage credits enabled, sessions that default to or switch to the 1M-context model fail with 'API Error: Usage credits required for 1M context' — and can wedge mid auto-compaction.

## Why it matters

Widely reported (issues #62063, #63896): fresh sessions and auto-compaction silently hit the 1M-context credit error, burning quota and blocking work mid-task for Pro/Max users who never asked for 1M context.

## How to apply

If you don't have usage credits enabled, select a standard-context model (via /model or `--model`, i.e. the non-`[1m]` variant) so compaction and fresh sessions don't error; the error itself advises 'use --model to switch to standard context.'

## Related

[[context-rot-prevention-compact-proactively]]
