---
id: make-bad-state-impossible-not-tolerant
created: 2026-06-21
status: active
supersedes: null
category: agents
source_type: post
sources:
  - https://lucumr.pocoo.org/2026/5/24/pi-oss/
---

# Reject Agent Fixes That Add Tolerant Readers and Fallbacks — Make the Bad State Impossible

## TL;DR

When an agent hits a malformed state, its default is to pile on a tolerant parser, then a fallback, then a migration, then debug output. The correct fix is usually to enforce an invariant upstream so the bad state can never occur.

## Why it matters

Defensive accretion bloats the codebase, hides the real bug, and lets broken state propagate. Agents over-engineer in exactly this direction by default, so a reviewer must redirect them to the invariant-level fix.

## How to apply

When reviewing an agent's bug fix, watch for added tolerant parsing, fallbacks, or migrations around malformed input. Stop it and ask which invariant was violated, then enforce it upstream. Prompt with 'make this state impossible,' not 'handle this state.'
