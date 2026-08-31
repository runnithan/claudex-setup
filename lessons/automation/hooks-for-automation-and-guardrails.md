---
id: hooks-for-automation-and-guardrails
created: 2026-04-25
status: active
supersedes: null
category: automation
sources:
  - transcripts/ray-amjad/claude-code-s-biggest-update-in-months_20260307.txt
  - transcripts/ray-amjad/anthropic-just-added-these-features-to-claude-code_20260307.txt
  - transcripts/ray-amjad/anthropic-just-dropped-their-internal-skills-strategy_20260424.txt
  - transcripts/simon-scrapes/every-claude-code-memory-system-compared-so-you-don-t-have-to_20260424.txt
  - transcripts/john-kim/claude-code-s-new-agent-teams-are-insane-opus-4-6_20260424.txt
---

# Use Hooks for Automated Formatting, Notifications, and Security Guardrails

## TL;DR

PreToolUse, PostToolUse, and Stop hooks run shell commands at key lifecycle points, use them for linting, Slack pings, or skill-scoped permissions.

## Why it matters

Hooks let you run arbitrary scripts triggered by Claude's lifecycle events without user prompts. PostToolUse hooks for ExitPlanMode can automatically archive or review plans before execution. PreToolUse hooks can pass additional context back to the model (e.g., inject memory index). Skill-scoped hooks restrict what the skill can do, making automated skills more secure. `once: true` prevents duplicate hook runs.

## How to apply

Define hooks in settings.json (global) or in skill/agent YAML frontmatter (scoped). Example PostToolUse hook for plan archiving: `{"event": "PostToolUse", "tool": "ExitPlanMode", "command": "./archive-plan.sh", "once": true}`. For skill security: use the Claude Code Guide subagent to write hooks that block web access, env file reads, and non-script tool calls for that skill. PreToolUse hooks can return additional context strings that the model reads before proceeding. Use `--maintenance` flag to trigger maintenance hooks on demand.

## Related

[[set-once-true-to-prevent-duplicate-hook-runs]], [[pretooluse-hook-context-strings-brief-the-model]]
