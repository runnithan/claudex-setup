---
id: stop-hook-8-block-cap
created: 2026-06-21
status: active
supersedes: null
category: automation
source_type: canonical
sources:
  - https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
---

# Stop Hooks Stop Blocking After 8 Consecutive Rejects — Raise the Cap or Add a Real Exit

## TL;DR

A Stop hook that keeps blocking is force-overridden after 8 consecutive blocks and the turn ends with a warning; raise `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` if you need more, but don't rely on the hook alone to gate completion.

## Why it matters

The changelog confirms the turn now ends with a warning after 8 consecutive blocks. A verification Stop hook your work can't satisfy within 8 tries will silently let an incomplete turn end, defeating the gate.

## How to apply

Design Stop-hook checks so a passing state is reachable within a few iterations. If a legitimately long check loop is expected, raise `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`. Pair the hook with a `/goal` condition or explicit verification step rather than treating 'block forever' as guaranteed.

## Related

[[hooks-for-automation-and-guardrails]], [[goal-verifiable-finish-lines-with-safety-caps]]
