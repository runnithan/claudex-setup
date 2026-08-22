---
id: skill-self-improvement-loop-binary-assertions
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/simon-scrapes/build-self-improving-claude-code-skills-the-results-are-crazy_20260424.txt
  - transcripts/simon-scrapes/every-level-of-claude-code-skills-in-27-mins_20260424.txt
---

# Run an Overnight Self-Improvement Loop on Your Skills

## TL;DR

Give Claude an evals.json with 25 binary assertions; it loops autonomously, improve, commit, retest, until you stop it or it hits 100%.

## Why it matters

Karpathy's auto-research pattern (try a change, run a test, check score, keep or revert, never stop) directly applies to Claude Code skills. Getting a skill from version 1 to reliable output normally takes weeks of manual tweaking. An autonomous loop runs all night and returns a structurally sounder skill by morning.

## How to apply

Create `skills/<skill-name>/evals/evals.json` with 25 binary true/false assertions per test case. Tell Claude: 'Use the skill creator skill. Run a self-improvement loop on my [skill] skill. Point to the evals file to evaluate each iteration. If any assertion fails, make one change to skill.md. Rerun and recalculate. If score improved, git commit. If dropped, git reset. Log everything. Do not ask for permissions. Keep looping until interrupted or perfect score.' The binary loop handles structure and format; qualitative improvements still need human review via the eval dashboard.
