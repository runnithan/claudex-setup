---
id: autonomous-ui-loop-acceptance-must-exercise-rendered-ui
created: 2026-07-02
status: active
supersedes: null
category: workflows
sources:
  - transcripts/sean-kochel/how-to-run-a-ralph-loop-step-by-step_7TwIrPQnFfg_20260702.txt
---

# Make Autonomous-Loop Acceptance Criteria Exercise the Rendered UI

## TL;DR

In autonomous loops that build UI, require browser/UI testing and a git commit per task — file existence is not verification.

## Why it matters

A Ralph loop marked UI tasks complete because it saw the components created in the codebase, but never tested the running app — so a right-click "branch" submenu silently didn't work. Loops trust code-presence over behavior unless you force otherwise.

## How to apply

Before starting the loop, edit the task list so each task's acceptance criteria run lint + type-check + tests, and — for user-facing UI — create passing test files or use a browser-automation MCP to actually exercise the interaction. Also require a git commit per completed task so every iteration is a reviewable checkpoint the loop can inspect later (not on by default).

## Related

[[match-autonomous-loops-to-disposable-or-verifiable-work]], [[visual-self-validation-screenshot-grading]], [[official-ralph-plugin-does-not-reset-context]]
