---
id: background-agents-auto-open-draft-prs
created: 2026-07-02
status: active
supersedes: null
category: automation
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Expect Background Agents to Commit, Push, and Open a Draft PR on Their Own

## TL;DR

Background agents launched from `claude agents` now finish code work by committing, pushing, and opening a draft PR from their worktree instead of pausing to ask — plan for that side effect.

## Why it matters

Per the 2.1.198 changelog: "Background agents launched from `claude agents` now commit, push, and open a draft PR when they finish code work in a worktree, instead of stopping to ask." If you assume a background agent will halt for review, you'll be surprised by pushed branches and draft PRs appearing unattended.

## How to apply

Launch background code agents on a clean, dedicated branch/worktree so their auto-commit and push don't clobber other work; review the resulting draft PR rather than expecting an in-session prompt; if you don't want a push, do the work in a foreground session instead.
