---
id: usage-and-stats-for-cost-awareness
created: 2026-04-25
status: superseded
superseded_by: usage-command-has-stats-and-cost-aliases-and-reads-local-history
supersedes: null
category: workflows
sources:
  - transcripts/simon-scrapes/you-re-using-claude-code-wrong-these-10-tips-will-change-everything_20260307.txt
  - transcripts/ray-amjad/anthropic-just-added-these-features-to-claude-code_20260424.txt
---

# Use /usage and /stats to Track Consumption and Identify Cost Drivers

## TL;DR

/stats shows model breakdown, streak, token totals, and per-day usage graphs. /usage is per-session. Share-ready with Ctrl+S.

## Why it matters

Without visibility into what's consuming tokens, you can't optimize. /stats reveals your favorite models (often Sonnet via subagents even if you think you're on Opus), identifies which days had expensive sessions, and lets you benchmark against teammates to establish norms for normal vs. runaway usage.

## How to apply

Type `/stats` to see favorite model, usage graph, usage streak, longest session, and total tokens used. Press Tab to switch to the Models tab for per-model per-day breakdown. Press Ctrl+S to copy stats to clipboard for sharing. Use this data to: identify which sessions are token-expensive (correlate with what you were doing), decide if your subagent model choices are right, and track whether /compact usage is paying off in reduced total tokens.
