---
id: plan-file-persistence-in-project-folders
created: 2026-06-18
status: active
supersedes: null
category: workflows
sources:
  - transcripts/simon-scrapes/14-genius-ways-to-give-claude-code-superpowers_20260612.txt
  - transcripts/simon-scrapes/you-re-only-using-10-of-claude-code-i-m-being-serious_20260617.txt
---

# Store Plans Inside Project Folders, Not Throwaway Directories

## TL;DR
Write `/plan` output (and PRDs) to a file inside the project repo so Claude can re-read it across context compactions, instead of losing it when the conversation summarizes.

## Why it matters
A plan that lives only in the conversation gets thinned out after one or two compactions, the nuance that guided the work is exactly what compaction drops. A plan written to a file in the project folder survives the whole session and beyond; Claude can re-read it to rebuild understanding after any context reset. This complements [[step-by-step-workflow-planning-before-session]] (plan first) and [[three-compact-rule-and-new-session-for-complex-plans]] (the file is what you carry forward).

## How to apply
- When using plan mode or drafting a PRD, save it to a project-specific path (e.g. `PLAN.md` or `docs/plan-<feature>.md` in the repo), not a global scratch directory.
- Reference that file in `CLAUDE.md` or mention it when context needs a refresh ("re-read PLAN.md before continuing").
- After a compaction or `/rewind`, point Claude back at the file rather than re-explaining the plan inline.
