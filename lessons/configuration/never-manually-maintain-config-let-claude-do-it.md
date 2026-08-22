---
id: never-manually-maintain-config-let-claude-do-it
created: 2026-04-25
status: active
supersedes: null
category: configuration
sources:
  - transcripts/john-kim/how-i-use-claude-code-meta-staff-engineer-tips_20260307.txt
  - transcripts/simon-scrapes/every-claude-code-memory-system-compared-so-you-don-t-have-to_20260424.txt
---

# Never Manually Maintain Config Files, Ask Claude to Update Its Own Configuration

## TL;DR

Paste the desired config behavior into Claude and ask it to find and update the relevant settings file; it knows its own schema.

## Why it matters

Manually editing settings.json, hooks configs, and MCP configurations is error-prone and slow. Claude knows its own configuration schema and can correctly update the right file for any setting. This applies to: enabling features, adding hooks, configuring MCP servers, setting up worktree isolation, and enabling experimental features.

## How to apply

Pattern: 'Can you set up [feature] for me? Here is the relevant documentation I found: [paste]. Please update the appropriate config file.' Claude will locate the correct settings.json (project vs. user level), add the right keys, and verify the structure. For complex setups like the memory management hook: paste the setup prompt, let Claude plan it, review the plan, then let it execute. Example: 'Enable auto memory for this project by updating the project settings.json appropriately.'
