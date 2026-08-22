---
id: custom-clarifying-questions-slash-command
created: 2026-06-18
status: active
supersedes: null
category: commands
sources:
  - transcripts/tristen-o-brien/the-6-claude-slash-commands-to-get-you-ahead-of-90-of-people-using-ai_20260615.txt
---

# Build a Custom Slash Command That Asks Clarifying Questions First

## TL;DR
Package the "ask before you build" habit into a reusable custom slash command: it captures the task, asks ~5 clarifying questions, drafts a plan, and waits for approval before executing.

## Why it matters
Tristen O'Brien reports a ~43% output-quality improvement from a custom command that forces clarity up front. The win isn't the questions themselves, it's making the behavior *repeatable* as a one-word command instead of re-typing the spec-developer preamble every session. This turns the existing [[spec-developer-workflow-with-clarifying-questions]] prompt into reusable infrastructure.

## How to apply
Create `.claude/commands/<name>.md` (e.g. `clarify.md`) whose body instructs Claude to:
1. Restate the task in its own words.
2. Ask 5+ clarifying questions covering scope, constraints, edge cases, and the definition of done.
3. Wait for answers, then produce a plan.
4. Pause for explicit approval before writing any code.

Invoke it with `/clarify <task>` at the start of any non-trivial work. Pair with [[plan-mode-before-every-nontrivial-change]] so the plan is reviewable before execution.
