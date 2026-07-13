---
id: request-post-tool-summaries-to-learn-from-claude
created: 2026-07-02
status: active
supersedes: null
category: prompting
sources:
  - transcripts/sean-kochel/i-didn-t-know-these-claude-code-rules-big-mistake_ynVfOd_ioDg_20260702.txt
---

# Request Post-Tool Summaries to Turn Claude Into a Teacher

## TL;DR

Newer Claude models are terse and skip explanations; a system-prompt instruction to summarize after tool use restores learnable rationale.

## Why it matters

Efficient models jump action-to-action without explaining decisions or tradeoffs, which starves beginner/intermediate users of the learning that is their real competitive edge. You lose the "why" behind each change unless you ask for it.

## How to apply

Put in CLAUDE.md / system prompt: "After completing a task that involves tool use, give a quick summary of what you did and why." Tune it — "explain like a fifth-grader," "include the tradeoffs you weighed," etc. Newer models honor system prompts strongly, so it applies every turn without re-asking.

## Related

[[directive-not-aggressive-prompting]], [[ask-for-options-before-changes-to-gauge-blast-radius]]
