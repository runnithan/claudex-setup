---
id: trigger-an-agent-on-pipeline-failure-to-self-heal
created: 2026-06-27
status: active
supersedes: null
category: automation
sources:
  - transcripts/nate-herk-ai-automation/i-will-never-fix-another-n8n-workflow-claude-code_20260620.txt
---

# Trigger an Agent on Pipeline Failure to Read the Error, Fix, and Redeploy

## TL;DR

Wire a production pipeline's error path to fire a Claude Code session with the failure details, so it reads the error, fixes the offending code, and redeploys without you.

## Why it matters

Most production failures are small (a typo, a missing null check, a changed schema) and the fix loop is mechanical — exactly what an agent can do in seconds given the error message and code access. Automating the failure-to-fix handoff turns 2am breakages into self-resolving events.

## How to apply

In your orchestrator (n8n, CI, a queue), set the failure handler to POST the error context (job id, failing step, message, stack) to a tunnel/webhook that launches a headless Claude run with repo access; have it diagnose, patch, and redeploy. Keep it scoped and log every auto-fix so you can review what changed.

## Related

[[headless-mode-for-batch-automation]], [[feed-posttooluse-block-back-with-continueonblock]]
