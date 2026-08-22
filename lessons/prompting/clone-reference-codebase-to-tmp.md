---
id: clone-reference-codebase-to-tmp
created: 2026-06-21
status: active
supersedes: null
category: prompting
source_type: post
sources:
  - https://simonwillison.net/guides/agentic-engineering-patterns/adding-a-new-content-type/
---

# Point the agent at a reference codebase by cloning it to /tmp

**TL;DR:** Instead of explaining a complex pattern in prose, tell Claude Code to `git clone` an existing repo into `/tmp` and study it as the reference for the new code.

## Why it matters

Coding agents can clone from GitHub, and pointing them at real code communicates complex conventions (an existing ORM layer, project style, a feature's shape) with a tiny prompt. The agent reads the actual implementation instead of relying on your lossy written description.

## How to apply

Add a one-line instruction like *"Clone `owner/repo` from GitHub to /tmp for reference"* before the task, then describe the new feature briefly and let the agent extract the patterns it needs from the cloned source.

> "Telling agents to use another codebase as reference is a powerful shortcut for communicating complex concepts with minimal additional information needed in the prompt.", Simon Willison
