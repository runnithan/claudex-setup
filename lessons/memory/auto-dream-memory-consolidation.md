---
id: auto-dream-memory-consolidation
created: 2026-06-03
status: active
supersedes: auto-memory-and-autodream-for-session-continuity
category: memory
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-nobody-knew-they-needed_20260603.txt
  - transcripts/simon-scrapes/master-claude-memory-in-23-minutes_20260603.txt
---

# Let Auto-Dream Consolidate Memory So It Doesn't Rot

## TL;DR

Auto memory captures learnings per session; Auto-dream periodically consolidates them, merging new signal, resolving contradictions, pruning stale entries, and converting relative dates to absolute, so the store stays clean. It triggers only when both ≥24h have passed AND >5 sessions have run since the last consolidation.

## Why it matters

Incrementally-captured memories accumulate noise and contradictions over many sessions, which degrades recall and silently eats startup context. Auto-dream is a background consolidation pass (modelled on memory consolidation during sleep): read-only on your code, write-only to memory files, and lock-guarded against concurrent runs. The dual trigger (≥24h AND >5 sessions) keeps it occasional rather than firing every session.

## How to apply

Toggle it in `/memory` (an Auto-dream on/off control), it runs in the background while you keep working. Keep `MEMORY.md` (or `memory.md`) as a small index pointing to per-topic memory files so each consolidation stays scoped and the index never balloons. Pair with a `SessionStart` hook that injects the memory index (not the full memories). This feature is unannounced/version-specific, verify exact command and setting names before relying on them.
