---
id: agent-teams-for-cross-domain-collaboration
created: 2026-04-25
status: active
supersedes: null
category: agents
sources:
  - transcripts/ray-amjad/learn-claude-code-agent-teams-in-12-minutes_20260307.txt
  - transcripts/simon-scrapes/how-to-use-claude-code-agent-teams-in-13-mins-opus-4-6_20260307.txt
  - transcripts/john-kim/claude-code-s-new-agent-teams-are-insane-opus-4-6_20260424.txt
  - transcripts/simon-scrapes/every-claude-code-workflow-explained-u0026-when-to-use-each_20260424.txt
---

# Use Agent Teams Only for 7-8/10 Complexity Tasks Needing Cross-Agent Communication

## TL;DR

Teams enable agent-to-agent messaging; they cost 4-7x more tokens than a single session, reserve for genuinely collaborative multi-domain work.

## Why it matters

Standard subagents can only report back to the main agent (hub-spoke bottleneck). Agent teams use a shared task list and mailbox so agents can communicate directly with each other. This enables a frontend agent and backend agent to coordinate without every message routing through the main orchestrator. But the token cost is substantial, use only when the coordination overhead is genuinely needed.

## How to apply

Enable in settings.json: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Describe the team in natural language: 'Create a performance agent team. One specializes in UI performance, one in debugging, one in UX quality.' Navigate between teammates with Shift+Up/Down. Use `teamMode: teamX` + tmux for split-pane view. Start with 3-5 teammates max; scale linearly with token cost. Best for: cross-domain builds (frontend + backend + testing), competing hypothesis debugging (send same bug to 5 parallel agents with different starting assumptions), read-only parallel investigation (context is shared via messages, not full history).
