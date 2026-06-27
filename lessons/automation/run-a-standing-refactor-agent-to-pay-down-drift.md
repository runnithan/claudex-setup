---
id: run-a-standing-refactor-agent-to-pay-down-drift
created: 2026-06-27
status: active
supersedes: null
category: automation
source_type: canonical
sources:
  - https://openai.com/index/harness-engineering/
  - https://milvus.io/blog/harness-engineering-ai-agents.md
---

# Run a Standing Background Agent That Submits Small Refactor PRs Continuously

## TL;DR

Schedule a background agent that scans for deviations from your conventions and opens small, auto-mergeable refactoring PRs — paying drift down continuously rather than letting it accumulate into a painful migration.

## Why it matters

Drift compounds, and a half-consistent codebase feeds agents contradictory signals about 'the right way.' OpenAI's harness had agents 'scan for deviations and submit refactoring PRs. Most merged automatically within a minute — small continuous payments rather than periodic reckoning,' keeping the repo coherent for future agent work.

## How to apply

Set up a cron/background agent that diffs the codebase against your conventions, opens narrowly-scoped refactor PRs, and auto-merges them when CI passes. Keep each PR tiny so review/auto-merge stays cheap and the codebase never drifts far from its intended shape.

## Related

[[finish-every-migration-you-start]], [[encode-agent-mistakes-as-lint-rules-with-the-fix-in-the-message]]
