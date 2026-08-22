---
id: skill-systems-over-monolithic-skills
created: 2026-06-03
status: active
supersedes: null
category: skills
sources:
  - transcripts/simon-scrapes/this-gives-claude-skills-a-massive-upgrade-it-s-easy_20260603.txt
  - transcripts/simon-scrapes/skill-chaining-in-claude-os-is-insane-don-t-fall-behind_20260603.txt
  - transcripts/simon-scrapes/i-rebuilt-hermes-in-claude-code-it-s-ridiculously-good_20260603.txt
---

# Compose Small Skills Into a Skill System, Not One Monolith

## TL;DR

Chain small single-purpose skills through an orchestrator skill (defining order, per-step inputs, and output→input handoffs) instead of baking everything into one monolithic process skill.

## Why it matters

A monolith that bakes in voice + audience + format duplicates the same context across many near-identical skills, so any change means editing all of them. Modular skills (one responsibility each) that pull from a shared context update in one place and recompose across uses, Anthropic calls this sequential workflow orchestration. Extends `skills-complementary-not-overlapping` and `shared-brand-context-folder-for-all-skills` with the composition/chaining pattern.

## How to apply

Split skills by responsibility (e.g. a voice-profile skill, an ICP/positioning skill, a format-template skill), then write an orchestrator skill that defines the step order, per-step inputs, output→input handoffs, human-in-the-loop checkpoints, and how results are displayed. Have each step read a shared brand/context folder so one edit propagates everywhere. For deterministic, code-driven chaining at scale, drive the steps from a `/workflows` JS file instead of an orchestrator skill (see `workflows-js-deterministic-orchestration`).
