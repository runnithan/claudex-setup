---
id: forked-subagents-when-nuance-matters
created: 2026-04-25
status: superseded
supersedes: null
category: agents
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-the-biggest-subagent-upgrade-yet_20260424.txt
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-nobody-knew-they-needed_20260424.txt
superseded_by: subagent-forking-is-now-on-by-default
---

# Use Forked Subagents When the Conversation Nuance Is Needed Downstream

## TL;DR

Forked subagents inherit the full conversation history (and share its prompt cache), so they preserve nuance that normal subagents compress away.

## Why it matters

Normal subagents receive a 2,000-token compressed summary of a 50,000-token conversation. When the full nuance of design decisions, code context, or accumulated back-and-forth is required, this compression loses too much. Forked subagents inherit the entire prior history and use the same prompt cache as the main session, making them cost-efficient for history-heavy tasks.

## How to apply

Enable with `CLAUDE_CODE_FORK_SUBAGENTS=1` env var in settings.json. Use `/fork` to spawn a forked subagent interactively. Rule of thumb: if the subagent needs the accumulated nuance (design variations, code verification with full context), use a fork. If the subagent benefits from a blank slate (code review, so it doesn't see the code it wrote and self-confirm), use a normal subagent. You can mix both: spawn one fork and one non-fork for the same task to compare perspectives.

## Related

[[pair-one-fork-and-one-fresh-subagent-for-decision-convergence]]
