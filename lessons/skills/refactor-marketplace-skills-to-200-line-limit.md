---
id: refactor-marketplace-skills-to-200-line-limit
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/simon-scrapes/every-level-of-claude-code-skills-in-27-mins_20260424.txt
  - transcripts/simon-scrapes/the-claude-code-skills-trap-most-people-fall-for-this_20260307.txt
---

# Refactor Any Marketplace Skill With >200 Lines Using the Skill Creator

## TL;DR

Run 'take this skill and refactor it to max 200 lines, move all reference info to references/' using the Skill Creator, 60% reduction is typical.

## Why it matters

Most marketplace skills are built to be comprehensive, not context-efficient. A 400-line skill.md will load all 400 lines into context every time it activates. Refactoring to 200 lines with proper references reduces context consumption by 60%+ and improves performance, without losing any of the domain knowledge, which moves to reference files.

## How to apply

Install the skill locally first: `claude install --local <github-url>`. Trigger the Skill Creator: 'Take the [skill-name] skill and use the Skill Creator skill to refactor it. I want the skill.md to be max 200 lines and all reference information should go into the references folder.' Review what changed, the Skill Creator will report the line count reduction and what new reference files were created. Verify the skill still activates properly by checking the description was improved as part of the refactor.
