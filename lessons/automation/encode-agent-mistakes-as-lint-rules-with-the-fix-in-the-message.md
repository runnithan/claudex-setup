---
id: encode-agent-mistakes-as-lint-rules-with-the-fix-in-the-message
created: 2026-06-27
status: active
supersedes: null
category: automation
source_type: post
sources:
  - https://www.latent.space/p/cognition
  - https://openai.com/index/harness-engineering/
  - https://milvus.io/blog/harness-engineering-ai-agents.md
---

# Encode the Patterns Agents Get Wrong as Lint Rules That Fail the PR — With the Fix in the Error Message

## TL;DR

Turn the shortcuts and architectural rules agents repeatedly violate into deterministic lint/CI rules that fail the PR, and write each rule's error message to contain the exact corrective action so the agent fixes it without another round-trip.

## Why it matters

Agents reliably reach for loose-typed escape hatches and ignore prose conventions. Cognition's Walden Yan: 'If you do getattr, your pull request is going to fail.' OpenAI's Codex team enforced layering 'mechanically, with error messages that included the fix instruction inline' — a bare 'violation' makes the agent guess and burn a turn; a message that names the fix lets it self-correct immediately.

## How to apply

Add Semgrep (or equivalent) rules to CI targeting the anti-patterns and architecture constraints your agents break (dynamic attribute access, untyped dicts, backwards-compat shims, layering violations); make them required PR checks; and author each error message to state the remedy, not just the rule. The failing check plus inline fix becomes a self-correcting loop.

## Related

[[make-bad-state-impossible-not-tolerant]], [[shift-verification-to-the-cheapest-rung]]
