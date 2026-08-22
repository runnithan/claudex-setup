---
id: advisor-tool-escalation-pattern
created: 2026-04-25
status: active
supersedes: null
category: model-selection
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-that-makes-sonnet-feel-like-opus_20260424.txt
---

# Configure /advisor So Sonnet Escalates to Opus When Stuck

## TL;DR

/advisor lets Sonnet consult a stronger model mid-session by passing the full conversation history, cheaper than running Opus throughout.

## Why it matters

Anthropic benchmarks show the Sonnet+Opus-advisor pattern consumes fewer usage limits and achieves slightly better performance on complex tasks than running Opus alone throughout. The advisor sees the full conversation history so it has complete context, and any advice it gives is added to the shared context for future advisor calls to also see.

## How to apply

Type `/advisor` to configure the advisor tool. Set your main model to Sonnet (`/model sonnet`), set the advisor to Opus. The advisor is called automatically before substantive work, when stuck, when results don't fit, and when the model believes the task is complete. You can also manually invoke it: 'Can you call the advisor to check this solution?' On short reactive tasks (change some colors), it correctly skips the advisor call. Note: the advisor cannot read files, it only uses the conversation history.
