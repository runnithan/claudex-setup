---
id: validation-loop-in-claude-md-is-critical
created: 2026-04-25
status: active
supersedes: null
category: configuration
sources:
  - transcripts/john-kim/how-i-use-claude-code-meta-staff-engineer-tips_20260307.txt
  - transcripts/john-kim/claude-code-workflows-that-will-10x-your-productivity_20260307.txt
---

# Include a Validation Loop in CLAUDE.md: Tell Claude How to Know It's Done

## TL;DR

Without a success criterion in CLAUDE.md, Claude either stops too early or never stops. Include test commands and acceptance criteria.

## Why it matters

Claude's default stopping behavior is to stop when the code looks right. This is different from stopping when tests pass, when the feature works end-to-end, or when the acceptance criteria are met. The validation loop, explicitly telling Claude how to verify its own work, is what enables autonomous runs that reliably produce correct output.

## How to apply

In CLAUDE.md, add a section: 'Validation: Before marking any task complete: 1. Run `npm test` and confirm all tests pass. 2. Run `npm run type-check` and confirm zero TypeScript errors. 3. If UI change: use /chrome to verify the affected page renders correctly. 4. If API change: test the endpoint with the sample requests in /tests/fixtures.' The goal is to encode your definition of done so Claude can self-verify without asking you.
