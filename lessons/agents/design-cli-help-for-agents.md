---
id: design-cli-help-for-agents
created: 2026-06-21
status: active
supersedes: null
category: agents
source_type: post
sources:
  - https://simonwillison.net/2026/Feb/16/rodney-claude-code/
---

# Write `--help` output that tells a coding agent everything it needs

## TL;DR

When building CLI tools that Claude Code will drive, design the `--help` text to be self-contained so the agent can learn the whole tool from running it.

## Why it matters

Agents discover and learn unfamiliar tools by reading their help output. If `--help` is comprehensive, the agent can use a brand-new tool correctly with no extra documentation, training data, or hand-holding in the prompt.

## How to apply

Treat `--help` as the agent's onboarding doc: include the full usage, options, and examples needed to operate the tool from scratch, so an agent that runs `your-tool --help` has everything required.

> "I designed Rodney to have --help output that provides everything a coding agent needs to know in order to use the tool.", Simon Willison
