---
id: rewind-can-recover-a-cleared-conversation
created: 2026-06-27
status: active
supersedes: null
category: context-management
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Use /rewind to Recover a Conversation You Accidentally Cleared

## TL;DR

/rewind can now resume a conversation from before /clear was run, so an accidental /clear is no longer an irreversible wipe.

## Why it matters

/clear used to be a one-way reset — an accidental clear meant rebuilding context from scratch. Knowing /rewind reaches past it turns a painful mistake into a quick recovery.

## How to apply

After an unwanted /clear, run /rewind (or Esc Esc) and pick a checkpoint from before the clear to resume the prior conversation. Per changelog 2.1.191: 'Added /rewind support for resuming a conversation from before /clear was run.'

## Related

[[rewind-instead-of-arguing-with-stale-context]], [[directional-summarize-rewind-menu]]
