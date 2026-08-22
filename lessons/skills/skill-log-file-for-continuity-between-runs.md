---
id: skill-log-file-for-continuity-between-runs
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-their-internal-skills-strategy_20260424.txt
---

# Add a Log File to Skills So They Remember Previous Runs

## TL;DR

A skills/[name]/data/log.json or learnings.md file lets the skill track what it wrote last time, avoiding duplicate content and maintaining continuity.

## Why it matters

Without persistent state, a content skill might write about the same topic twice, a research skill might recheck already-analyzed sources, and an outreach skill might contact the same people repeatedly. A simple JSON or text log between runs gives the skill the context it needs to continue where it left off.

## How to apply

Add to skill.md: 'Before starting, read skills/[name]/data/log.json. Record [what was produced] and [what failed] in the log after each run.' Store: published topics (don't repeat), contacts already messaged, files already processed, errors from last run. Use `git ignore` if each user should have their own log; commit it if the team should share. Store in the `.claude` plugin data directory if you want the log to survive plugin updates. Commit the log structure as part of the skill so new installs start with the right schema.
