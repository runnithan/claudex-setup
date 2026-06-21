---
id: agent-view-native-orchestration-ui
created: 2026-06-03
status: active
supersedes: manage-goals-not-terminals
category: workflows
sources:
  - transcripts/john-kim/claude-code-just-got-better-agent-view_20260603.txt
  - transcripts/simon-scrapes/claude-code-has-a-new-ui-pair-it-with-claude-os_20260603.txt
  - transcripts/simon-scrapes/stop-using-claude-code-in-terminal-it-s-holding-you-back_20260424.txt
  - transcripts/simon-scrapes/the-claude-code-setup-nobody-shows-you-replaces-openclaw-hermes_20260424.txt
---

# Use `claude agents` (Agent View) Instead of Juggling Terminals

## TL;DR

`claude agents` opens a native multi-session dashboard (persists across terminal restarts, git-worktree-backed) — the built-in answer to managing 5+ parallel sessions, replacing tmux/window juggling and the older build-your-own-Kanban command centers.

## Why it matters

Running many parallel sessions previously meant babysitting terminal windows and losing sessions when a terminal closed. The real bottleneck at 5+ sessions is managing goals and reviewing outputs, not navigating terminal state. Agent View gives one persistent dashboard with status at a glance, sessions that survive terminal close, and per-project scoping (git worktrees under the hood for collision-free parallel work) — delivering that goal-level view natively. It is the native replacement for the "build your own Kanban" advice (Vibe Kanban, Paperclip, custom HTML/JS command centers), which now remain optional only if you need goal-level features Agent View lacks (e.g. deadlines, a non-terminal/web surface).

## How to apply

Run `claude agents` (v2.1.139+); `/bg` backgrounds the current session into it. Keys: Right = attach, Left = detach, Space = peek / quick reply, `Ctrl+S` = sort by repo, `Ctrl+R` = rename working dir, `Ctrl+T` = pin, `Ctrl+X` twice = delete. Status colours: gray = working, yellow = waiting/checking, purple = merging (e.g. a worktree), green = done/merged. Caveats (research preview): terminal-only, sorts to parent-folder level (not subfolders), and approving from the summary view was unreliable — attach to approve.
