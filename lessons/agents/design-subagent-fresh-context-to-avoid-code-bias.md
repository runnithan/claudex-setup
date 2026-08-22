---
id: design-subagent-fresh-context-to-avoid-code-bias
created: 2026-04-25
status: active
supersedes: null
category: agents
sources:
  - transcripts/ray-amjad/anthropic-reveal-how-to-make-claude-code-a-better-designer_20260307.txt
  - transcripts/ray-amjad/anthropic-just-dropped-the-biggest-subagent-upgrade-yet_20260424.txt
---

# Use a Fresh-Context Subagent for Design Work to Avoid Code Bias

## TL;DR

A subagent that hasn't seen your existing code generates more distinct designs; the main session's code context biases toward what already exists.

## Why it matters

When Claude has seen your existing code in the main session, it tends to design variations that are constrained by what it knows. A subagent with a clean context approaches the design problem with no anchoring to existing patterns. This is exactly why forked subagents are poor for code review (they saw the code they wrote) but regular subagents are better.

## How to apply

For design variations: spawn a regular (non-forked) subagent with only a description of the goal, your design reference files (fonts.md, colors.md, animations.md), and a clear prompt—without passing it the existing codebase context. Collect multiple variations from the subagent, compare them, pick the one you like, then tell the main session to implement the chosen design. Apply the same principle for any creative or exploratory task where prior context would be anchoring.
