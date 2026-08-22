---
id: slow-down-instruction-one-step-at-a-time
created: 2026-06-07
status: active
supersedes: null
category: prompting
sources:
  - transcripts/simon-scrapes/how-anthropic-teams-actually-use-claude-code-day-to-day-for-non-engineers_20260607.txt
---

# Explicitly Tell Claude to Slow Down and Work Step-by-Step

## TL;DR

Add "Go one step at a time, don't expect everything to work first try" to your context file or initial prompt.

## Why it matters

Anthropic's legal and design teams use this phrase to set expectations: Claude shouldn't try to solve the full problem in one burst; it should work iteratively with the human. Without it, Claude defaults to delivering a complete (often overreaching) solution in one shot.

## How to apply

In your CLAUDE.md context file or opening prompt, add: "Take one step at a time. Do not expect everything to work out of the box from a single instruction. I'll guide you through corrections." This shifts the interaction from "give me the perfect solution" to "let's build it together", pairs well with `treat-ai-junior-dev-specific-tight-context`.
