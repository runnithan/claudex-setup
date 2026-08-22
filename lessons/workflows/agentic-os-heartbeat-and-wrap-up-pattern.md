---
id: agentic-os-heartbeat-and-wrap-up-pattern
created: 2026-04-25
status: active
supersedes: null
category: workflows
sources:
  - transcripts/simon-scrapes/how-smart-people-are-using-claude-code-skills-to-automate-anything_20260424.txt
  - transcripts/simon-scrapes/the-easiest-way-to-get-ahead-with-claude-code_20260424.txt
  - transcripts/simon-scrapes/the-claude-code-setup-nobody-shows-you-replaces-openclaw-hermes_20260424.txt
---

# Implement a Heartbeat and Wrap-Up Pattern for Self-Maintaining Systems

## TL;DR

At session start, a heartbeat scans skills vs CLAUDE.md and auto-registers new additions. At session end, a wrap-up skill collects feedback and commits learnings.

## Why it matters

As your skills folder grows, CLAUDE.md and README fall out of sync. Skills get added but never documented; learnings get made but never recorded. The heartbeat ensures the system always reflects what's actually installed. The wrap-up ensures every session's learnings become next session's rules, without manual bookkeeping.

## How to apply

Heartbeat skill: triggered on session start, it scans the skills folder and compares against CLAUDE.md's skill registry. New skills found are automatically registered with their name, description, and dependencies noted. Existing skills that no longer exist are pruned. Wrap-up skill: trigger it with 'close session' or 'wrap up'. It reviews all deliverables produced, collects any feedback you give ('the research was useful, the newsletter was too long'), updates learnings.md on a per-skill basis, and commits all changes. Install these as the first two skills in any skill-based system.
