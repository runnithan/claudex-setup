---
id: prompt-cache-what-breaks-it
created: 2026-06-27
status: active
supersedes: null
category: context-management
sources:
  - transcripts/nate-herk-ai-automation/give-me-10-mins-and-i-ll-save-you-millions-of-claude-tokens_6cEQEba0i2A_20260627.txt
---

# Know What Invalidates the Prompt Cache — Don't Switch Models or Edit CLAUDE.md Mid-Session

## TL;DR

Switching models mid-session, editing CLAUDE.md or other early context, and going idle past the cache TTL all invalidate the prompt cache and force Claude to reprocess the whole conversation from scratch.

## Why it matters

The prompt cache is what makes a long session cheap — each turn re-reads the cached prefix instead of re-billing it. Anything that changes the prefix (a different model, an edited system prompt/CLAUDE.md, or letting the cache expire) busts it, silently inflating cost and latency. The /model opusplan pattern, which swaps Opus and Sonnet between plan and execution, pays this tax on every switch.

## How to apply

Make model switches and CLAUDE.md edits between sessions, not in the middle of one. To change models cleanly, save state to a file, /clear, then start fresh on the new model. Keep working within the cache window rather than leaving a session idle for long stretches.

## Related

[[model-selection-opus-sonnet-haiku-use-cases]], [[context-rot-prevention-compact-proactively]]
