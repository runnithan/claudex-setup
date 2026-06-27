---
id: guard-unattended-agent-runs-with-a-stall-watchdog-and-bounded-retry
created: 2026-06-27
status: active
supersedes: null
category: automation
source_type: canonical
sources:
  - https://github.com/openai/symphony/blob/main/SPEC.md
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Guard Unattended Agent Runs With a Stall Watchdog and Bounded Retry

## TL;DR

Wrap autonomous or headless agent runs with a stall watchdog (kill-and-retry when no events arrive for N minutes), bounded exponential-backoff retries, and a concurrency cap — so a silently-hung 'zombie' agent doesn't wedge the loop and quietly burn quota.

## Why it matters

Long-running agents hang with no output and keep spending wall-clock/tokens. OpenAI's Symphony enforces a stall_timeout (default 5m): 'if no agent events arrive within that window, the orchestrator terminates the worker and schedules a retry,' with capped exponential backoff and a concurrency limit. Claude Code now caps CLAUDE_CODE_MAX_RETRIES at 15 and provides CLAUDE_CODE_RETRY_WATCHDOG for exactly this.

## How to apply

For any `claude -p` loop or agent fleet, add a watchdog that kills a worker emitting no events within N minutes and reschedules it, retry failures with bounded backoff (not infinitely), and cap concurrent agents. In Claude Code specifically, configure CLAUDE_CODE_RETRY_WATCHDOG for unattended sessions rather than cranking CLAUDE_CODE_MAX_RETRIES (now capped at 15).

## Related

[[goal-verifiable-finish-lines-with-safety-caps]], [[stop-hook-8-block-cap]]
