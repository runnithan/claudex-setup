---
id: headless-mode-for-batch-automation
created: 2026-04-25
status: active
supersedes: null
category: automation
sources:
  - transcripts/simon-scrapes/every-claude-code-concept-explained-for-normal-people_20260307.txt
  - transcripts/simon-scrapes/you-re-using-claude-code-wrong-these-10-tips-will-change-everything_20260307.txt
  - transcripts/simon-scrapes/every-claude-code-workflow-explained-u0026-when-to-use-each_20260424.txt
  - transcripts/simon-scrapes/claude-code-just-went-mobile-remote-control-vs-openclaw_20260307.txt
---

# Use Headless Mode (-p Flag) for Batch Processing and Scheduled Automation

## TL;DR

`claude -p 'your prompt'` runs Claude with no interaction, full permissions assumed, pipe it to cron or Mac scheduler for autonomous workflows.

## Why it matters

Headless mode is how Claude Code goes from a tool you sit with to a background agent. Combined with OS-level scheduling (cron, launchctl), it enables fully autonomous workflows that run whether you're present or not. The Ralph Loop pattern extends this: feeding the same prompt back until a completion condition is met.

## How to apply

Basic: `claude -p 'process this prompt and return results' > output.json`. With skills: include skill trigger words in the prompt. In cron: `0 7 * * 1 cd /your/project && claude -p 'check for new YouTube videos and run content repurposing skill' --disallowedTools AskUserQuestion`. For the Ralph Loop: create `prd.json` with user stories and acceptance criteria, then `/ralph-loop` with max iterations. Headless works best for: batch processing, report generation, content pipelines, anything where output is easy to verify before acting on.
