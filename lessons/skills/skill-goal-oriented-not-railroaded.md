---
id: skill-goal-oriented-not-railroaded
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-their-internal-skills-strategy_20260424.txt
  - transcripts/simon-scrapes/how-smart-people-are-using-claude-code-skills-to-automate-anything_20260424.txt
---

# Write Skills Goal-First, Not as Rigid Recipes

## TL;DR

Specifying every step collapses Claude's distribution to one narrow path; goal + context + gotchas lets Claude adapt.

## Why it matters

A skill that says 'write 3 behavioral questions, 3 technical questions, 1 culture fit question' forces identical output regardless of context, a senior architect gets the same interview as a junior intern. Anthropic's internal research shows that rigid step-by-step recipes eliminate all optionality and prevent Claude from making better judgment calls.

## How to apply

Structure skills around goals and constraints, not rigid sequences. Instead of 'do A then B then C', write 'prepare interview questions for this role. Test for what actually predicts success here. Here are the traits our best hires had: [list].' Add gotcha rules for specific failure modes you've observed. Reserve rigid sequencing only for compliance or safety-critical workflows where there is genuinely only one right way.
