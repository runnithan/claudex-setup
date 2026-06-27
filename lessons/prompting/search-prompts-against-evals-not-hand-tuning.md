---
id: search-prompts-against-evals-not-hand-tuning
created: 2026-06-27
status: active
supersedes: null
category: prompting
source_type: post
sources:
  - https://www.dbreunig.com/2026/06/22/the-problem-is-prompt-debt.html
---

# Stop Hand-Tuning Prompts — Search for Them Against an Eval Metric

## TL;DR

Once you can score prompt candidates with an eval, stop hand-crafting the prompt and instead search for it with an optimizer (DSPy, GEPA) — the prompt becomes a thing you measure your way to, not a wall of stern instructions.

## Why it matters

Drew Breunig: hand-tuned prompts full of 'repeating instructions, stern warnings, and all-caps demands' are brittle and locked to one model. He argues to 'specify your system's behavior with measurements, not prose,' after which 'the prompt is no longer something to craft but something for which to search' — which also lets you migrate models without rewriting prose.

## How to apply

Build an eval that scores candidate prompts on your task, then run a prompt-optimization system (DSPy/GEPA) to search for the best one; define behavior with metrics, and swap models once behavior is metric-defined rather than prose-defined.

## Related

[[error-analysis-before-llm-judge-no-blanket-score]], [[directive-not-aggressive-prompting]]
