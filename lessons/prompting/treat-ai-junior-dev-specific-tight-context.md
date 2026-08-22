---
id: treat-ai-junior-dev-specific-tight-context
created: 2026-04-25
status: active
supersedes: null
category: prompting
sources:
  - transcripts/andrew-codesmith/900-hours-of-learning-claude-code-cursor-in-10-minutes_20260307.txt
  - transcripts/andrew-codesmith/master-95-of-claude-code-in-15-mins-as-a-beginner_20260424.txt
  - transcripts/ray-amjad/anthropic-reveals-how-to-prompt-claude-code-10x-better_20260307.txt
---

# Treat Claude Like a Junior Developer With ADHD: Specific Tasks, Tight Context

## TL;DR

Give one specific task at a time with tight context constraints; Claude will guess confidently and take you to error hell if you don't.

## Why it matters

LLMs are designed to fill in blanks by predicting what comes next, they will never say 'I don't know enough to proceed.' They will confidently proceed in the wrong direction. Your job as the human is to make those blanks smaller and better-defined. This is not a limitation to work around, it is the fundamental model of how to use these tools effectively.

## How to apply

Break work into specific tasks: not 'implement the auth system' but 'implement the JWT token validation middleware for the /api route using our existing AuthService'. Constrain scope explicitly: 'Modify only files in /src/api/middleware. Do not touch the frontend.' Add success criteria: 'The test in /tests/api/auth.test.js should pass when you're done.' Use subagents for any noisy exploration so it doesn't contaminate the main task context. When a task goes sideways, /rewind, never argue.
