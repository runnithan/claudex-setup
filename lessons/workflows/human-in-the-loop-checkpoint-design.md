---
id: human-in-the-loop-checkpoint-design
created: 2026-06-07
status: active
supersedes: null
category: workflows
sources:
  - transcripts/simon-scrapes/how-anthropic-teams-actually-use-claude-code-day-to-day-for-non-engineers_20260607.txt
---

# Design Workflows With Human Decision Points, Not Full Automation

## TL;DR

Keep the human at the output checkpoint: Claude handles the repetitive grind (generating, finding, drafting), then stops for human review before anything ships.

## Why it matters

Every high-value workflow at Anthropic (marketing, legal, design) has the same shape: input → AI transforms data → human reviews output. The review checkpoint is where judgment lives, it prevents AI slop and is the actual value-add of the system, not a bottleneck to automate away.

## How to apply

When building a workflow, map it explicitly: input (e.g., existing ads) → transformation (e.g., generate 100 variations) → output checkpoint with human review (pick which to ship). Never ask Claude to "run the ad account autonomously", ask it to "generate 100 headline variations for me to choose from." Place the checkpoint at the point where judgment matters, and automate everything before it.
