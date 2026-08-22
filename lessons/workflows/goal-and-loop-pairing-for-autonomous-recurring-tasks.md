---
id: goal-and-loop-pairing-for-autonomous-recurring-tasks
created: 2026-06-18
status: active
supersedes: null
category: workflows
sources:
  - transcripts/simon-scrapes/14-genius-ways-to-give-claude-code-superpowers_20260612.txt
  - transcripts/simon-scrapes/you-re-only-using-10-of-claude-code-i-m-being-serious_20260617.txt
---

# Pair /goal With /loop (or Routines) for Autonomous Recurring Tasks

## TL;DR
`/loop` sets the cadence (daily, weekly); `/goal` sets the completion condition. Used together, a task runs on schedule and keeps working each run until its goal is met.

## Why it matters
Each command alone is incomplete: `/loop` reruns a prompt but doesn't know when "done" is reached within a run, and `/goal` defines done but doesn't recur. Combined, they replace a standing manual chore, "clear the inbox daily until empty," "scrape competitors weekly until all captured." This composes [[goal-verifiable-finish-lines-with-safety-caps]] with [[loop-command-for-recurring-in-session-tasks]].

## How to apply
1. Write the prompt with a `/goal`-style completion condition baked in (e.g. "file every email, stop when the inbox is empty"), and give it a safety cap so it can't run forever.
2. Schedule it: `/loop` for cadences under ~3 days (runs in-session), or a scheduled routine for longer intervals (weekly+, persists in the desktop app).
3. Approve once, then let it run on its own.
