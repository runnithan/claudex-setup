---
id: skills-complementary-not-overlapping
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-their-internal-skills-strategy_20260424.txt
  - transcripts/simon-scrapes/how-smart-people-are-using-claude-code-skills-to-automate-anything_20260424.txt
  - transcripts/simon-scrapes/the-claude-code-skills-trap-most-people-fall-for-this_20260307.txt
---

# Skills Should Be Complementary, Not Overlapping, One Skill Per Specific Goal

## TL;DR

Before creating a new skill, read all existing skill frontmatter for overlaps; a bug-hunting skill should call the DataDog skill rather than duplicating data fetching.

## Why it matters

Overlapping skills create confusion about which to use, split the Claude distribution toward two mediocre skills rather than one excellent one, and waste context with redundant instructions. The best skills are narrow, specialized, and designed to be composed, a DataDog skill providing data that a debugging skill consumes.

## How to apply

Rule: before creating a skill, list all existing skills with their trigger descriptions. Ask: 'Is there any overlap between what I want to build and what already exists?' If overlap is found: either extend the existing skill's reference files or modify its description to handle the new use case. If genuinely new: design the skill to interoperate, have it explicitly call other skills when it needs capabilities they provide. Build skills that chain: trending-research → content-repurposing → humanizer → publish (each is narrow; together they form a workflow).
