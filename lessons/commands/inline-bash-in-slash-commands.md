---
id: inline-bash-in-slash-commands
created: 2026-06-21
status: active
supersedes: null
category: commands
source_type: post
sources:
  - https://www.infoq.com/news/2026/01/claude-code-creator-workflow/
  - https://x.com/bcherny/status/2007179832300581177
---

# Pre-compute context with inline bash inside slash commands

## TL;DR

Embed bash in a slash command to pre-compute state (e.g. `git status`) so the model gets the context for free instead of round-tripping for it.

## Why it matters

A high-frequency command that makes the model gather routine context itself burns tool calls and turns every time. Pre-computing that context with inline bash makes the command fast and deterministic, Boris Cherny (who created Claude Code) runs a `/commit-push-pr` command this way dozens of times a day.

## How to apply

In a checked-in `.claude/commands/*.md` command, use inline bash to compute things like git status, diff stats, or the branch name up front, then have the model act on the pre-filled result rather than fetching it.

> "Claude and I use a /commit-push-pr slash command dozens of times every day. The command uses inline bash to pre-compute git status and a few other pieces of info to make the command run quickly and avoid back-and-forth with the model.", Boris Cherny
