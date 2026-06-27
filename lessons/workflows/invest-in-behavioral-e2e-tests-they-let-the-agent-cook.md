---
id: invest-in-behavioral-e2e-tests-they-let-the-agent-cook
created: 2026-06-27
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://www.dbreunig.com/2026/06/22/the-problem-is-prompt-debt.html
  - https://www.dbreunig.com/2026/05/04/10-lessons-for-agentic-coding.html
---

# Invest More in Behavioral End-to-End Tests — They're What Let the Agent Cook

## TL;DR

Treat tests as the thing that frees an agent to rewrite implementation freely: spend more bandwidth on behavior-level end-to-end tests that pin what the product does, not how it does it.

## Why it matters

Drew Breunig: 'The best engineers now spend more of their bandwidth on tests than ever, as they are no longer a safety net but the thing that lets the model cook.' Behavior-level tests let an agent refactor or rewrite internals without breaking the product, which is exactly what autonomous work needs.

## How to apply

'Write tests that measure our product's functions, not how it performs them' — favor end-to-end behavioral contracts over implementation-coupled tests, and treat the suite as the signal the agent optimizes against during autonomous runs.

## Related

[[shift-verification-to-the-cheapest-rung]], [[separate-evaluator-agent-exercises-the-running-app]]
