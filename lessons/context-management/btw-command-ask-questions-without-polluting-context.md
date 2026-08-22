---
id: btw-command-ask-questions-without-polluting-context
created: 2026-04-25
status: active
supersedes: null
category: context-management
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-nobody-knew-they-needed_20260424.txt
---

# Use /btw to Ask Questions Mid-Session Without Polluting the Context

## TL;DR

/btw answers single-turn questions in a side channel using the session's prompt cache, no context pollution, no interruption to Claude's work.

## Why it matters

Interrupting Claude mid-task with a question adds the Q&A noise to the conversation history, polluting the context with information the model didn't need for the task, only you needed it. If done repeatedly, this can fill the context window and degrade future outputs. /btw is a side channel that uses the prompt cache of the main session (making it cheap), doesn't interrupt the agent, and leaves no trace in the conversation history.

## How to apply

While Claude is working, type `/btw [your question]` and press Enter. A small window appears with the answer. Dismiss with Escape, Enter, or Space. Limitations: single-turn only (no follow-up questions), no tool access (cannot read new files). For multi-turn deep dives or artifact generation, use `claude -c --fork-session` in a split pane instead. If /btw reveals a fundamental misconception, use /rewind to roll back and reprompt rather than arguing with stale context.
