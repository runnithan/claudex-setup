---
id: directional-summarize-rewind-menu
created: 2026-06-21
status: active
supersedes: null
category: context-management
source_type: canonical
sources:
  - https://code.claude.com/docs/en/best-practices
---

# Compact Only Part of the Conversation with Summarize-From-Here / Up-To-Here

## TL;DR

`Esc Esc` (or `/rewind`) → pick a message → 'Summarize from here' condenses everything after that point; 'Summarize up to here' condenses earlier messages while keeping recent ones full. A surgical alternative to `/compact`.

## Why it matters

Docs document directional summarization from the `/rewind` checkpoint menu. Blanket `/compact` loses nuance everywhere; directional summarize lets you keep the half that still matters verbatim.

## How to apply

When early exploration is done but recent debugging is load-bearing, `/rewind` → select the boundary message → 'Summarize up to here' to shrink the stale front while keeping recent turns full (or 'from here' for the opposite).

## Related

[[context-rot-prevention-compact-proactively]], [[three-compact-rule-and-new-session-for-complex-plans]]
