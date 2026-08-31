---
id: skills-add-scripts-to-avoid-repeated-api-scaffolding
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-their-internal-skills-strategy_20260424.txt
---

# Add Pre-Built API Scripts to Skills to Save Tokens on Repeated Data Fetching

## TL;DR

Build Python/Node scripts once for each API your skill uses; subsequent runs call the scripts rather than re-deriving the API pattern from scratch.

## Why it matters

Every time a skill needs to fetch data from an API it hasn't seen before, it spends tokens figuring out the API, reading documentation, and testing requests. If the skill runs daily, this scaffolding cost repeats every time. Pre-built scripts in the skill's scripts folder let Claude simply call the function and focus on analyzing the result.

## How to apply

When building a new skill that calls an API: first run, let Claude figure out the API and generate working scripts. Say: 'Once you've figured out how to use this API, turn the working fetch functions into a set of scripts in the skills/[skill-name]/scripts folder that can be called reliably in future runs.' Add a read-only API key to the skill's .env. Use skill-scoped hooks to prevent Claude from reading the .env directly or making unapproved web requests. Next runs: Claude calls the pre-built scripts instead of re-deriving the API.

## Related

[[guard-skill-env-secrets-with-skill-scoped-hooks]]
