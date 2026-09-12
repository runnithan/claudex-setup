---
id: visual-self-validation-screenshot-grading
created: 2026-06-03
status: active
supersedes: null
category: workflows
sources:
  - transcripts/john-kim/how-to-build-an-app-with-claude-code-no-experience-required_20260603.txt
  - transcripts/john-kim/what-is-agentic-ai-engineering-meta-staff-engineer-explains_20260603.txt
---

# Give Visual Work a Self-Validation Loop (Screenshot + Grade + Iterate)

## TL;DR

Have Claude drive the running app via `/chrome`, screenshot it, grade the result against explicit criteria, and iterate until it passes, backed by real screenshot/E2E tests and observable runtime state.

## Why it matters

Models can't see their own output by default and lack visual taste, so layout/spacing/colour drift goes uncaught. An explicit grade-and-iterate harness with concrete pass criteria lets the agent self-correct before a human looks. Screenshots alone aren't fully reliable, so back them with tests and readable app/store state that confirm the code path actually fired. Builds on `chrome-extension-for-browser-testing`.

## How to apply

Add a validation step to the skill or plan: "use `/chrome` to open the running app, screenshot it, and grade against explicit rules (alignment, spacing, no overlaps, design-system/token match); re-iterate until the score passes." Then confirm with screenshot/E2E tests and observable runtime state (readable store/app state, structured logs) proving the behaviour fired, not just that a test passed. When the agent repeatedly can't verify something, build a CLI/tool to expose that signal.

## Related

[[build-a-cli-to-expose-a-signal-the-agent-keeps-failing-to-verify]]
