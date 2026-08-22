---
id: skill-description-is-routing-logic-not-marketing
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-their-internal-skills-strategy_20260424.txt
  - transcripts/simon-scrapes/every-level-of-claude-code-skills-in-27-mins_20260424.txt
  - transcripts/simon-scrapes/build-self-improving-claude-code-skills-the-results-are-crazy_20260424.txt
  - transcripts/simon-scrapes/how-to-use-claude-code-skills-like-the-1-it-s-easy-actually_20260307.txt
---

# Write Skill Descriptions as Routing Logic, Not Marketing Copy

## TL;DR

Community testing found skills activate only ~20% of the time with vague descriptions. List exact trigger keywords Claude would hear.

## Why it matters

Claude uses the YAML description to semantically match incoming queries to skills. A description like 'comprehensive tool for monitoring PR status across the deployment lifecycle' doesn't contain any words a user would actually say. Activation rates as low as 20% mean 4 in 5 invocations miss the skill entirely.

## How to apply

Write your description with three elements: (1) trigger keywords, exact phrases the user would say ('triggers on: babysit this PR, watch CI, make sure this lands'); (2) explicit non-triggers ('does not trigger for general web browsing'); (3) expected output ('produces a research brief other skills can consume'). The Skill Creator skill has a built-in loop that tests trigger accuracy across sample queries and iterates the description until activation hits your target threshold.
