---
id: plan-mode-before-every-nontrivial-change
created: 2026-04-25
status: active
supersedes: null
category: workflows
sources:
  - transcripts/ray-amjad/my-claude-code-workflow-for-2026_20260307.txt
  - transcripts/ray-amjad/anthropic-reveals-how-to-prompt-claude-code-10x-better_20260307.txt
  - transcripts/john-kim/how-i-use-claude-code-meta-staff-engineer-tips_20260307.txt
  - transcripts/john-kim/his-claude-code-workflow-is-insane_20260307.txt
  - transcripts/simon-scrapes/every-claude-code-concept-explained-for-normal-people_20260307.txt
  - transcripts/andrew-codesmith/900-hours-of-learning-claude-code-cursor-in-10-minutes_20260307.txt
  - transcripts/andrew-codesmith/how-i-code-profitable-apps-solo-beginner-step-by-step-best-tools_20260307.txt
  - transcripts/john-kim/complete-beginner-s-guide-to-openai-s-codex-app_20260424.txt
  - transcripts/andrew-codesmith/master-95-of-claude-code-in-15-mins-as-a-beginner_20260424.txt
---

# Use Plan Mode Before Every Non-Trivial Change

## TL;DR

Enter plan mode for any change >10-15 lines; the AI drafts a detailed plan you review before a single line is written.

## Why it matters

Without a plan, Claude moves like a fast train on the wrong track, generating code rapidly in the wrong direction, wasting tokens, and requiring painful rollbacks. Plan mode catches edge cases, surfaces design decisions, and forces the model to break work into verifiable steps before irreversible edits happen.

## How to apply

Type `/plan` or press Shift+Tab twice to enter plan mode. Describe your goal, answer Claude's clarifying questions, review the resulting plan, then approve it. For large features, use Ultrathink in the plan prompt (`ultrathink: implement this plan`). For cross-session continuity, store the approved plan in a file via `planDirectory` in settings.json.
