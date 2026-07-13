---
id: multi-hypothesis-prompt-for-diagnosis
created: 2026-07-02
status: active
supersedes: null
category: prompting
sources:
  - transcripts/sean-kochel/most-people-use-ai-the-wrong-way_4dK49YpL1Hw_20260702.txt
---

# Use a Cautious Multi-Hypothesis Prompt for Diagnosis and Debugging

## TL;DR

For "why did X happen" questions, force multiple hypotheses and evidence-needed reasoning so Claude doesn't fabricate one confident false cause.

## Why it matters

LLMs optimize for plausible-sounding tokens, are penalized for "I don't know," and lock onto a single narrative that doubles down when challenged — dangerous for debugging and root-cause work where the confident wrong answer costs you hours.

## How to apply

Prepend a rule-set: act as a cautious reasoning assistant that minimizes false confidence; evaluate multiple hypotheses; avoid stating a definite cause; use conditional (if/then) reasoning; for each claim state what evidence would confirm or falsify it; and list the critical uncertainties. Treat the model as a hypothesis generator, not an oracle.

## Related

[[steer-agent-to-vertical-slice-and-root-cause]], [[fact-verification-table-for-claude-claims]], [[assessment-only-mode-for-diagnostic-tasks]]
