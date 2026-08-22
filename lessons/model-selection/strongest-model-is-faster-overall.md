---
id: strongest-model-is-faster-overall
created: 2026-06-21
status: active
supersedes: null
category: model-selection
source_type: post
sources:
  - https://www.anup.io/35-claude-code-tips-from-the-guy-who-built-it/
  - https://x.com/bcherny/status/2007179832300581177
---

# Default to the strongest model + thinking because prompt-to-done is shorter

**TL;DR:** Use the top model with thinking for all coding work even though it's slower per request, fewer corrections make the total time-to-done shorter.

## Why it matters

The instinct to reach for a faster/cheaper model to "save time" is often wrong. A slower-but-stronger model needs less steering and fewer retries, so end-to-end wall-clock, and your review attention, is lower than with a faster, weaker model. Boris Cherny runs the strongest model with thinking enabled for everything.

## How to apply

Set your default to the strongest available model with thinking on for coding; don't reflexively downshift to a faster model. Reserve cheaper/faster models for genuinely trivial or mechanical work where steering cost is near zero.

> "Opus 4.5 with thinking enabled for everything ... the total time from prompt to done is usually shorter.", Boris Cherny (reported)
