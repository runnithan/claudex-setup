---
id: error-analysis-before-llm-judge-no-blanket-score
created: 2026-06-21
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://hamel.dev/blog/posts/evals-skills/
  - https://hamel.dev/blog/posts/claude-auto-evals/
---

# Do Error Analysis and Split Failure Types Before Building an LLM Judge

## TL;DR

When having Claude build evals for an AI feature, first sort real failures into distinct error types, then give each type its own evaluator (a code assertion where string or tool-call inspection can check it, an LLM judge only for the rest) instead of one blended score.

## Why it matters

Hamel Husain: lump failures into a generic 'hallucination score' and you'll miss errors. Different failures (confusing facts vs fabricating user actions) need different checks, so a single blended score hides the ones that matter. Reviewing an auto-eval tool, they found it produced one call-transfer evaluator that mixed one LLM-judge check with three code checks under a single "protocol_ok" headline, which hides which failure moved, and they read the generated judge prompt or code directly because the tool's prose summary of it was hard to follow. They also note that infrastructure around the agent, telemetry and evals it can query, mattered more than improving the model.

## How to apply

Point Claude at your traces to do error analysis first: have it cluster real failures into named error types, then build one evaluator per type rather than one blanket judge. Use plain code assertions for anything checkable by string or tool-call inspection and reserve an LLM judge for the rest. When an agent drafts an evaluator, reject one that bundles several failures behind a single pass/fail score, and ask it to show the judge prompt or code, not a summary of it. If inheriting an eval pipeline, start with an eval audit before adding new judges.

Verified (second source): https://hamel.dev/blog/posts/claude-auto-evals/ was fetched with curl on 2026-10-02 and the quote below matched verbatim. Practice, not a mechanism: no flag or command involved. That article's claude-api plugin commands (build_eval, hill-climb) are NOT verified: 0 hits in the Claude Code 2.1.288 binary, not in the claude-plugins-official marketplace listing, no official doc found. Do not cite those names.

> "I would prefer to scope the eval to focus on one error at a time, or at the very least separate the evals into those that needed a code-based eval vs a LLM as a Judge.", Hamel Husain

## Related

[[skill-creator-ab-testing-and-evals]], [[skill-self-improvement-loop-binary-assertions]]
