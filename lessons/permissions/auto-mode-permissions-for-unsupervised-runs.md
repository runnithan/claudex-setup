---
id: auto-mode-permissions-for-unsupervised-runs
created: 2026-04-25
status: active
supersedes: null
category: permissions
sources:
  - transcripts/simon-scrapes/the-only-claude-code-updates-you-need-to-know-apr-2026_20260424.txt
  - transcripts/simon-scrapes/every-claude-code-concept-explained-for-normal-people_20260307.txt
  - transcripts/ray-amjad/big-claude-code-update-web-mobile-sandbox_20260307.txt
---

# Enable Auto Mode or Set Allow/Deny Rules to Run Without Constant Permission Prompts

## TL;DR

Developers approve 93% of Claude's permission requests anyway. Auto mode uses a classifier to auto-approve safe actions and block risky ones.

## Why it matters

The default permissions model requires approving every file write, package install, and test run, babysitting that defeats the purpose of agentic AI. Anthropic research found 93% of prompts are approved anyway. Auto mode automates the safe 93% and flags only the risky actions (delete files, push to main, send data externally).

## How to apply

Auto mode (team plans only for now): start with `claude --enable-auto-mode` or press Shift+Tab to cycle to auto mode. For pro/max plans: configure settings.json with explicit allow/deny lists. Allow: read files and folders, run dev server, run tests, format and lint, edit and write files. Deny: install packages, delete files, API calls to external services, read sensitive files/secrets. This covers ~80% of the benefit without the classifier. For fully autonomous overnight runs: combine with the `-p` headless flag and `--disallowedTools` for specific safety boundaries.
