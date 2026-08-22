---
id: sandbox-mode-for-safe-exploration
created: 2026-04-25
status: active
supersedes: null
category: permissions
sources:
  - transcripts/ray-amjad/big-claude-code-update-web-mobile-sandbox_20260307.txt
  - transcripts/ray-amjad/claude-code-s-new-default-subagents-this-week-s-news_20260307.txt
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-that-kills-openclaw_20260307.txt
---

# Use Sandbox Mode for Safe Experimentation and Automated Skill Runs

## TL;DR

`/sandbox` enables file/network isolation; configure excludedCommands, allowLocalBinding, and allowUnixSockets for your use case.

## Why it matters

Running skills that have API key access and file write permissions without sandboxing is risky, especially for automated scheduled tasks. Sandbox mode limits what Claude can access, preventing accidental database deletions, credential exfiltration, or runaway file operations in untested skills.

## How to apply

Type `/sandbox` to enable. Configure in settings.json: `{"sandbox": {"excludedCommands": ["rm", "curl"], "allowLocalBinding": true, "allowUnixSockets": true, "allowUnsandboxedCommands": false}}`. For skill-level sandboxing, use PreToolUse hooks to block specific tools. For remote/mobile sessions, always use sandbox or run on a VPS. `allowLocalBinding: true` is needed if your skill starts a local server for testing.
