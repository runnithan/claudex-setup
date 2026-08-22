---
id: avoid-role-based-subagents-coordination-overhead
created: 2026-04-25
status: active
supersedes: null
category: agents
sources:
  - transcripts/john-kim/how-i-use-claude-code-meta-staff-engineer-tips_20260307.txt
  - transcripts/simon-scrapes/every-claude-code-workflow-explained-u0026-when-to-use-each_20260424.txt
---

# Avoid Role-Based Subagents for Coordination Tasks, Hub-Spoke Bottlenecks Emerge

## TL;DR

Naming subagents 'designer' / 'backend' / 'tester' creates coordination overhead via the main agent; use agent teams for multi-role work instead.

## Why it matters

Subagents cannot communicate with each other, everything routes through the main agent. If three role-based subagents each need to share state, the main agent must serialize and relay context between them. This bottleneck grows with the number of coordination messages needed and degrades the main agent's context. Agent teams solve this with direct messaging but at higher token cost.

## How to apply

Use role-based subagents only for truly independent parallel work (e.g., five parallel competitive research agents that don't need to talk to each other). For work that requires coordination between roles (frontend needs to know what backend built), use agent teams or sequential single-session work. When you catch yourself having the main agent relay messages between subagents repeatedly, switch to an agent team or redesign the task to be parallelizable without coordination.
