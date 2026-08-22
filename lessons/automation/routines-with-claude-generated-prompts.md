---
id: routines-with-claude-generated-prompts
created: 2026-06-11
status: active
supersedes: null
category: automation
sources:
  - transcripts/tristen-o-brien/top-6-claude-code-features-to-get-you-ahead-of-99-of-users-in-under-10-minutes_20260610.txt
---

# Have Claude Write the Routine's Prompt Before You Schedule It

## TL;DR

Before creating a scheduled routine, ask Claude in a normal session to "write a detailed routine prompt for [task]" and paste that into the routine config, instead of hand-writing the prompt yourself.

## Why it matters

A routine runs unattended, so an under-specified prompt fails silently or drifts. Claude writes a more complete prompt than you would by hand, it has the project context in-session and thinks through inputs, edge cases, and output format that you'd forget. The session where you draft it can also test the prompt once before you schedule it.

## How to apply

In a working session: "Write a detailed routine prompt that pulls my calendar, checks my to-do list, generates a morning briefing, and emails it to me, include error handling for missing data." Review/test it once interactively, then create the routine and paste the generated prompt with a schedule. Apply the same trick to any headless automation (cron + `claude -p`, scheduled cloud agents).
