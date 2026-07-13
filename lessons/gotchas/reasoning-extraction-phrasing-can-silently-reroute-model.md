---
id: reasoning-extraction-phrasing-can-silently-reroute-model
created: 2026-07-02
status: active
supersedes: null
category: gotchas
sources:
  - transcripts/nate-herk-ai-automation/how-anthropic-engineers-actually-prompt-fable-5_vcU85OrwuV0_20260702.txt
---

# "Explain Your Reasoning" Phrasing Can Silently Reroute You to a Weaker Model

## TL;DR

A standing "explain / show your reasoning" line — especially in a system prompt — can trip a safety check and silently reroute your request to a different, less-capable fallback model.

## Why it matters

The model runs a safety check and can silently hand requests that look like reasoning-extraction (or hacking, or dangerous-bio) to a fallback model. In the app you won't see the swap happen (only the raw API response reveals it), so you quietly lose capability while thinking you're still on the top model.

## How to apply

Keep "explain your reasoning" / "reveal your chain of thought" out of system prompts, and don't phrase tasks in ways that read as malicious. If output quality suddenly drops for no clear reason, suspect a silent reroute and reword the prompt. (Note the tension with [[request-post-tool-summaries-to-learn-from-claude]] — ask for a plain-English summary of *what it did*, not for its internal reasoning.)

## Related

[[request-post-tool-summaries-to-learn-from-claude]], [[avoid-the-1m-context-model-without-usage-credits]]
