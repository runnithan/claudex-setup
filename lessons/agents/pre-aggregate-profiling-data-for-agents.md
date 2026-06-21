---
id: pre-aggregate-profiling-data-for-agents
created: 2026-06-21
status: active
supersedes: null
category: agents
source_type: post
sources:
  - https://www.indragie.com/blog/i-shipped-a-tool-to-help-agents-fix-slow-code
---

# Pre-Aggregate Profiling/Runtime Data Before Handing It to an Agent

## TL;DR

When you want a coding agent to fix slow code, don't dump raw profiler output — give it a single tool that aggregates samples (frequencies, percentiles) into an analyzed view, because LLMs are bad at doing those computations themselves.

## Why it matters

Agents see the caller code but not the runtime characteristics of callees, so they guess and pick the wrong hotspot. Raw flamegraph output forces the model to do statistical aggregation it's poorly suited for; a pre-analyzed view (e.g. '~22% CPU in this function') lets it correctly localize the bottleneck.

## How to apply

When wiring performance/observability tooling for an agent: expose at most a handful of tools (ideally one); have the tool itself compute frequencies and percentile durations and present a consumable summary, not raw samples; supply runtime data alongside the source; and be specific about which path is slow.

## Related

[[cli-tools-over-mcp-for-tokens]], [[design-cli-help-for-agents]]
