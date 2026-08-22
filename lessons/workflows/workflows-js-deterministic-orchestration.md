---
id: workflows-js-deterministic-orchestration
created: 2026-06-03
status: active
supersedes: null
category: workflows
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-the-update-everyone-s-obsessed-with-dynamic-workflows_20260603.txt
---

# Use the /workflows JS Tool for Deterministic Multi-Agent Orchestration

## TL;DR

Define a JavaScript workflow in `.claude/workflows/` to orchestrate sub-agents in code, results pass directly between agents without re-entering the main context, avoiding the orchestrator token tax. (Beta, env-var gated.)

## Why it matters

Skill- or LLM-driven orchestration bounces every sub-agent result back through the main session, taxing tokens and degrading the orchestrator as the window fills. A workflow runs plain JS (loops, conditionals, fan-out) that calls `agent()` and passes structured outputs agent-to-agent in code, so the main context stays lean. Sub-agents auto-retry (up to 3×), runs are resumable, and the whole thing runs in the background while you keep working.

## How to apply

Enable via the gating env var, then add a `.js` file under `.claude/workflows/` with a `meta` block (name, description, phases), input/output schemas, and JS logic. Use the primitives: `agent()` (one fresh sub-agent), parallel batches (fan out N, await all), and `pipeline()` (stream items through stages so a later stage starts as soon as one item finishes). Add a `budget` and gate loops on remaining tokens; set the model per-agent (cheap first, escalate). Inspect runs and per-stage tokens with `/workflows`. Reach for it when work is repeatable, fans out via loops/conditionals, or is long enough to fail midway; skip one-offs. Command names are version-specific, verify before relying.
