---
id: context-fork-for-isolated-skill-execution
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/ray-amjad/claude-code-s-biggest-update-in-months_20260307.txt
  - transcripts/ray-amjad/better-than-mcps-claude-code-s-new-skills-feature_20260307.txt
  - transcripts/ray-amjad/the-top-0-01-user-s-guide-to-claude-code_20260307.txt
---

# Use context_fork: true in Skill Frontmatter for Isolated Skill Execution

## TL;DR

Skills with context_fork run in a separate context window; the agent field and disable_model_invocation save tokens on cheap tasks.

## Why it matters

Some skills do noisy work (scanning files, calling APIs) that would pollute the main session if run inline. Context_fork ensures that work happens in its own context and only the result comes back. Combined with `disable_model_invocation: true` for skills that just run scripts and return, and a `model: haiku` field for simple skills, you can dramatically reduce the cost of running skills at scale.

## How to apply

In skill.md YAML frontmatter: `context_fork: true` to run in isolated context. `agent: [agent-name]` to run the skill as a specific subagent. `disable_model_invocation: true` for skills that just invoke scripts without needing model reasoning. `model: haiku-3` for skills that are simple enough to run on the cheapest model. These are composable: a data-fetch skill might have `context_fork: true`, `model: haiku-3`, and pre-built scripts, nearly free to run at high frequency.
