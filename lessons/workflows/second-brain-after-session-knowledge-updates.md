---
id: second-brain-after-session-knowledge-updates
created: 2026-04-25
status: active
supersedes: null
category: workflows
sources:
  - transcripts/john-kim/claude-code-workflows-that-will-10x-your-productivity_20260307.txt
  - transcripts/john-kim/his-claude-code-workflow-is-insane_20260307.txt
  - transcripts/simon-scrapes/the-easiest-way-to-get-ahead-with-claude-code_20260424.txt
  - transcripts/simon-scrapes/how-smart-people-are-using-claude-code-skills-to-automate-anything_20260424.txt
---

# After Each Session, Ask Claude to Update Your Knowledge Base

## TL;DR

At session end, prompt Claude to update project MD files with decisions made and lessons learned, this is compound engineering.

## Why it matters

If you don't extract knowledge from sessions, it disappears into compaction summaries. Over time, your CLAUDE.md and reference files should grow to reflect the accumulated wisdom of every session. Boris Cherniy's viral workflow from Anthropic: anytime Claude makes a mistake, don't just fix it, add the correction to CLAUDE.md so Claude knows not to do it next time. During code reviews, tag Claude and ask it to update its own instructions.

## How to apply

At the end of sessions: 'Based on what we learned today, can you update the relevant reference files and CLAUDE.md with any new rules, gotchas, or architectural decisions?' Or use a wrap-up skill that runs at `/close session` or `/wrap-up` to: review deliverables, collect feedback, fix skills with learnings, update learnings.md files, and commit all changes. Keep learnings files structured and prune stale rules weekly to avoid context bloat from accumulated notes.
