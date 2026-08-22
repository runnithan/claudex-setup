---
id: parallel-sessions-with-system-notifications
created: 2026-04-25
status: active
supersedes: null
category: workflows
sources:
  - transcripts/john-kim/how-i-use-claude-code-meta-staff-engineer-tips_20260307.txt
  - transcripts/john-kim/his-claude-code-workflow-is-insane_20260307.txt
  - transcripts/ray-amjad/claude-code-s-biggest-update-in-months_20260307.txt
  - transcripts/simon-scrapes/stop-using-claude-code-in-terminal-it-s-holding-you-back_20260424.txt
---

# Run Multiple Parallel Claude Sessions With System Notification Hooks

## TL;DR

Open 5+ terminal tabs each running a separate task; use a Stop hook to notify you when each finishes so you can check in without babysitting.

## Why it matters

The biggest productivity gain from agentic AI is parallelism, running multiple agents on independent tasks simultaneously. But without notifications, you end up constantly polling each window. A Stop hook that sends a system notification (or Slack ping, or Telegram message) lets you context switch freely and return only when a session needs attention.

## How to apply

Open multiple iTerm/terminal tabs, each starting `claude` in a different worktree or context. Configure a Stop hook: `{"event": "Stop", "command": "osascript -e 'display notification \"Claude session finished\" with title \"Claude Code\"'"}`. For team setups: send a Slack or Telegram message via curl in the Stop hook command. Navigate between sessions with keyboard shortcuts. Manage at scale using a Kanban-style command center or Tmux with split panes. Boris Cherniy reports using 5 local + 5-10 web sessions simultaneously.
