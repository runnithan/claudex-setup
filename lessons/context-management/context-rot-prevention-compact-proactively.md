---
id: context-rot-prevention-compact-proactively
created: 2026-04-25
status: active
supersedes: null
category: context-management
sources:
  - transcripts/simon-scrapes/every-claude-code-concept-explained-for-normal-people_20260307.txt
  - transcripts/simon-scrapes/the-easiest-way-to-get-ahead-with-claude-code_20260424.txt
  - transcripts/simon-scrapes/200-hours-of-claude-code-lessons-in-14-minutes-for-business-owners_20260424.txt
  - transcripts/ray-amjad/the-top-0-01-user-s-guide-to-claude-code_20260307.txt
  - transcripts/andrew-codesmith/master-95-of-claude-code-in-15-mins-as-a-beginner_20260424.txt
---

# Compact Proactively, Don't Wait for Auto-Compact

## TL;DR

By the time Claude auto-compacts, you've already been operating in degraded mode. Compact or clear before context quality drops.

## Why it matters

Context rot (progressively worse output as context window fills with stale info, failed attempts, and off-topic Q&A) happens faster than most users realize. Auto-compact triggers late; the model has already been working with a polluted context for a while before it fires. One task per conversation, then start fresh.

## How to apply

Use `/compact [optional instructions]` to compress the conversation with a custom summary prompt (e.g., '/compact keep the architectural decisions and current task state'). Use `/clear` between completely unrelated tasks. For complex multi-phase projects, use the GSD pattern: plan in one session, execute in another, review in a third, each starts fresh with only the context it needs. As a power user tip: Mermaid diagrams convey what thousands of tokens of text would, so use them to compress complex state descriptions.
