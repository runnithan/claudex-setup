---
id: classify-skills-into-four-types
created: 2026-07-01
status: active
supersedes: null
category: skills
sources:
  - transcripts/austin-marchese/how-anthropic-employees-actually-use-claude-skills_3UWxMPUko1k_20260628.txt
---

# Classify Each Skill as Utility, Verification, Data-Enrichment, or Orchestration

## TL;DR

Bucket every skill into one of four types — utility (does a reusable task), verification (a quality gate), data-enrichment (pulls external data), or orchestration (chains other skills). Keep each skill to one type; a skill that both drafts and grades its own work confuses Claude about when to invoke it and what "done" looks like.

## Why it matters

A skill that straddles categories loses activation clarity — Claude can't tell if it's a tool to run, a check to apply, a fetch to perform, or a coordinator to kick off, so it underuses all of those functions. Naming the type forces single responsibility and makes the skill's trigger and success criteria obvious.

## How to apply

Before writing a skill, decide which of the four it is, and split it if it's more than one (e.g. separate "draft email" as a utility from "grade email quality" as a verification). Encode the type in the description's trigger language: a verification skill's description says when it runs ("after code changes, before deploy"), an enrichment skill's names the data it fetches, an orchestration skill's lists the skills it chains. Pairs with "write skill descriptions as routing logic" — the type tells you what routing language to use.
