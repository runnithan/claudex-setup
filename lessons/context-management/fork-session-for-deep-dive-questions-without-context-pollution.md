---
id: fork-session-for-deep-dive-questions-without-context-pollution
created: 2026-04-25
status: active
supersedes: null
category: context-management
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-nobody-knew-they-needed_20260424.txt
  - transcripts/ray-amjad/my-claude-code-workflow-for-2026_20260307.txt
---

# Use --fork-session for Deep-Dive Tangents That Need Tool Access

## TL;DR

`claude -c --fork-session` in a new pane creates a copy of the current session for multi-turn explorations that leave no trace in the main conversation.

## Why it matters

/btw handles single-turn questions, but if you need to ask a follow-up, generate a Mermaid diagram, or explore a different approach with tool calls, you need a full fork. Fork sessions share the prompt cache of the original session (cheap to start) but their conversation history is completely separate, changes don't cross back.

## How to apply

Press Ctrl+D to split the window. In the new pane: `claude -c --fork-session`. This loads a copy of the current session. Ask your deep-dive question, generate artifacts, explore the alternative path. When done, press Ctrl+W to close the fork. Nothing from the fork enters the original conversation. Alternatively, use `/fork` inside the session which will present the fork command to run in a new pane. Pairs well with worktrees: fork into a different worktree to explore an alternative implementation without conflicts.
