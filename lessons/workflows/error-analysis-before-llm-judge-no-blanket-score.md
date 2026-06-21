---
id: error-analysis-before-llm-judge-no-blanket-score
created: 2026-06-21
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://hamel.dev/blog/posts/evals-skills/
---

# Do Error Analysis and Split Failure Types Before Building an LLM Judge

## TL;DR

When having Claude build evals for an AI feature, first categorize real failures into distinct error types instead of scoring everything under one generic metric.

## Why it matters

Hamel Husain: lump failures into a generic 'hallucination score' and you'll miss errors. Different failures (confusing facts vs fabricating user actions) need different checks, so a single blended score hides the ones that matter. He notes infrastructure around the agent — telemetry and evals it can query — mattered more than improving the model.

## How to apply

Point Claude at your traces to do error analysis first: have it cluster real failures into named error types, then build a specific check per type rather than one blanket judge. If inheriting an eval pipeline, start with an eval audit before adding new judges.

## Related

[[skill-creator-ab-testing-and-evals]], [[skill-self-improvement-loop-binary-assertions]]
