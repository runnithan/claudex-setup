---
id: nested-subagents-for-layered-analysis
created: 2026-06-11
status: active
supersedes: null
category: agents
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-the-biggest-subagent-upgrade-yet_20260610.txt
---

# Use Nested Subagents (2-3 Layers) for Multi-Order Effect Analysis

## TL;DR

For questions with second- and third-order consequences (a change → its implications → the blast radius of each implication), have layer-1 subagents each spawn layer-2 subagents, so every level of analysis runs in its own isolated context and only clean conclusions roll back up.

## Why it matters

A single agent (or one flat layer of subagents) tends to stop at first-order effects, and stuffing the whole cascade into one context drowns the signal. Nesting keeps each layer's noisy searching and verification isolated, while the main context receives only the collapsed, high-signal result.

## How to apply

Structure the prompt as explicit layers: "For each of these 10 contracts, spawn an agent to determine what breaks if we change term X (layer 1). Each of those agents should spawn agents to find what else must change as a result (layer 2). Report a consolidated impact table." Works for code too: API signature change → affected callers → affected tests/consumers of those callers. Reserve it for genuinely cascading questions, it multiplies token cost like any fan-out.
