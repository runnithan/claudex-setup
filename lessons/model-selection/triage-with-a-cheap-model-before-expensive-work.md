---
id: triage-with-a-cheap-model-before-expensive-work
created: 2026-06-27
status: active
supersedes: null
category: model-selection
sources:
  - transcripts/ray-amjad/anthropic-will-bring-back-fable-5-differently_r4_KLZvHoaA_20260626.txt
---

# Triage With a Cheap Model to Rank Targets Before Spending an Expensive One

## TL;DR

Before pointing an expensive model at a codebase, run a cheap model over everything to score each file on impact × opportunity, discard the low scores, and send only the top few targets to the expensive model.

## Why it matters

Expensive models cost many times more per token, and aiming them at the wrong files burns budget and context for little return. A fast cheap model is plenty to evaluate where the value is, so the expensive model only does the deep work that actually matters — roughly halving cost per unit of quality on discovery-heavy work.

## How to apply

Define impact (reach/importance) and opportunity (bugginess/complexity) as separate 1-5 scores; run cheap parallel subagents to score files, multiply, drop the 1s and 2s, and pass the top 3-5 to the strong model with meta-level context (not just 'fix this file'). Scales to very large codebases.

## Related

[[model-selection-opus-sonnet-haiku-use-cases]], [[add-code-retrieval-before-reaching-for-a-pricier-model]]
