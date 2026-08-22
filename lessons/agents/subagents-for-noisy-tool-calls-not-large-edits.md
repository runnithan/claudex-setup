---
id: subagents-for-noisy-tool-calls-not-large-edits
created: 2026-04-25
status: active
supersedes: null
category: agents
sources:
  - transcripts/ray-amjad/my-claude-code-workflow-for-2026_20260307.txt
  - transcripts/ray-amjad/anthropic-just-dropped-the-biggest-subagent-upgrade-yet_20260424.txt
  - transcripts/ray-amjad/claude-code-s-new-default-subagents-this-week-s-news_20260307.txt
  - transcripts/simon-scrapes/every-claude-code-workflow-explained-u0026-when-to-use-each_20260424.txt
---

# Delegate Noisy Tool Calls to Subagents; Avoid Subagents for Large Code Edits

## TL;DR

Subagents keep main context lean by handling research, log analysis, and exploration; they are poor at large edits due to compression loss.

## Why it matters

Every noisy tool call, file searches, web research, log reading, that happens in the main session fills the context window with irrelevant output. Subagents run in isolated contexts and return only a condensed summary. But the 50,000 tokens of nuance in the main conversation gets compressed to ~2,000 tokens in a subagent's initial prompt, meaning complex code edits lose too much detail through this compression.

## How to apply

Use subagents for: codebase exploration (Explore subagent is built-in and read-only), web research, log analysis, reviewing diffs. Avoid subagents for: large multi-file refactors that need the full conversation nuance, design iterations that depend on decisions made earlier in the session. Keep the main session for synthesis and decision-making; use subagents for data gathering.
