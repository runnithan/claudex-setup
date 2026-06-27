---
id: separate-evaluator-agent-exercises-the-running-app
created: 2026-06-27
status: active
supersedes: null
category: agents
source_type: canonical
sources:
  - https://openai.com/index/harness-engineering/
  - https://milvus.io/blog/harness-engineering-ai-agents.md
---

# Use a Separate Evaluator Agent That Exercises the Running App, Not Self-Review

## TL;DR

Split generation from verification across two agents: give the evaluator browser automation to click through the live app like a user and concrete runtime pass-thresholds, rather than letting the agent that wrote the code grade itself.

## Why it matters

An agent that produced a change self-evaluates generously. OpenAI's Codex harness used 'independent verification agents rather than self-validation,' with an Evaluator using Playwright to 'click through the application like a real user' across UI/API/DB, and concrete done-criteria such as 'a service had to start in under 800 milliseconds before a task was considered complete.'

## How to apply

Run a fresh evaluator agent in a separate context that drives the running app (Playwright/CDP) and checks measurable thresholds — latency, real user-flow behavior — not 'looks done.' Layer it on top of self-validation screenshot loops to remove the conflict of interest.

## Related

[[visual-self-validation-screenshot-grading]], [[ultrareview-multi-agent-verification-pattern]]
