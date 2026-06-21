---
id: feed-posttooluse-block-back-with-continueonblock
created: 2026-06-21
status: active
supersedes: null
category: automation
source_type: canonical
sources:
  - https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
---

# Use PostToolUse `continueOnBlock` to Coach Claude Instead of Killing the Turn

## TL;DR

Set `continueOnBlock: true` on a PostToolUse hook to feed the hook's rejection reason back to Claude and continue the turn, instead of just hard-blocking — turning a guardrail into a self-correcting nudge.

## Why it matters

The changelog adds `continueOnBlock` for PostToolUse: set true to feed the rejection reason back to Claude and continue. A plain block ends the action with no guidance; with this, Claude reads why it was blocked and fixes the input in the same turn.

## How to apply

On a PostToolUse hook that validates output (lint, schema, forbidden-path check), set `continueOnBlock: true` and write a clear rejection reason. Claude re-attempts correctly rather than stalling.

## Related

[[hooks-for-automation-and-guardrails]]
