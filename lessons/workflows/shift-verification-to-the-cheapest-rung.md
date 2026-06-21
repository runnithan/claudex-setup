---
id: shift-verification-to-the-cheapest-rung
created: 2026-06-21
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://eugeneyan.com/writing/working-with-ai/
---

# Shift Verification to the Cheapest Rung and Let Claude Run the Eval

## TL;DR

Catch issues with the cheapest deterministic check that can catch them (lint/type/test) rather than expensive human review, and when a metric exists, hand Claude the eval so it can optimize against it itself.

## Why it matters

Eugene Yan frames verification as a ladder — the bottom is cheap and deterministic, the top expensive and judgement-bound; address issues at the lowest possible rung. Without a self-checkable loop, Claude can't tell whether its output is good, so problems escalate to your review.

## How to apply

Make the cheap, deterministic checks runnable by Claude in-session (lint, types, unit tests, an eval script) and tell it to run them and iterate until green before handing back. Reserve your judgement for what only judgement can catch. Check for execution drift often and direction drift occasionally.

## Related

[[validation-loop-in-claude-md-is-critical]]
