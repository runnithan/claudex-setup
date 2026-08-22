---
id: readme-driven-development-into-claude-code
created: 2026-06-21
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://simonwillison.net/2026/Apr/5/scan-for-secrets-3/
---

# Write the README first, then hand it to Claude Code to build the tool

**TL;DR:** Specify a tool by writing its complete README describing exactly how it should work, then dump that README into Claude Code as the build spec and have it implement with red/green TDD.

## Why it matters

README-driven development front-loads the design decisions into a precise, human-readable spec, so the agent builds to a clear target, and you get the docs for free. Pairing it with red/green TDD keeps the implementation honest against that spec.

## How to apply

Carefully write the README covering the exact intended behaviour, paste it into Claude Code and tell it to build the tool from that spec, instructing it to use red/green test-driven development as it goes.

> "I built this tool using README-driven-development: I carefully constructed the README describing exactly how the tool should work, then dumped it into Claude Code and told it to build the actual tool (using red/green TDD, naturally.)", Simon Willison
