---
id: three-compact-rule-and-new-session-for-complex-plans
created: 2026-04-25
status: active
supersedes: null
category: context-management
sources:
  - transcripts/ray-amjad/the-top-0-01-user-s-guide-to-claude-code_20260307.txt
---

# Use the 3-Compact Rule: After 3 Compactions, Start a New Session With a Summary

## TL;DR

Each compaction loses nuance. After 3, the context summary is too thin; start fresh with a written plan carrying forward only what matters.

## Why it matters

Compaction preserves the gist but loses detail. After 3 compactions, you have a summary of a summary of a summary, important edge cases, implementation decisions, and context that shaped the approach have been discarded. Starting a new session with a deliberately written plan handoff preserves exactly what you want to carry forward.

## How to apply

After the third compaction: ask Claude to write a handoff document covering: current state, decisions made and why, files modified and their purpose, remaining work, and known risks. Start a new session and paste only this handoff document as the initial context. This is more reliable than relying on compaction to preserve what matters, you control what carries forward. Keep handoff documents in a `.claude/handoffs/` folder for multi-session projects.
