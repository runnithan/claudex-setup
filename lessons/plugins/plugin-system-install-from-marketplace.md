---
id: plugin-system-install-from-marketplace
created: 2026-04-25
status: active
supersedes: null
category: plugins
sources:
  - transcripts/ray-amjad/big-claude-code-update-plugins_20260307.txt
  - transcripts/ray-amjad/anthropic-just-connected-claude-code-to-your-browser_20260307.txt
  - transcripts/simon-scrapes/how-to-use-claude-code-skills-like-the-1-it-s-easy-actually_20260307.txt
  - transcripts/ray-amjad/anthropic-just-added-these-features-to-claude-code_20260424.txt
---

# Browse and Install Plugins from the Official Marketplace

## TL;DR

`/plugin` opens the official marketplace; plugins bundle skills + commands + hooks + MCP servers into one installable package.

## Why it matters

Plugins are the unit of sharing for complete workflows, not just individual skills. A plugin can include a skill, a custom slash command, lifecycle hooks, and MCP server configuration all at once. The official marketplace ensures plugins are discoverable and maintained; unofficial GitHub installs require `--local` flag to inspect before installing globally.

## How to apply

Type `/plugin` to open the marketplace browser. Select a plugin, press Enter to install, Claude Code restarts to activate it. To install from GitHub: `claude install --local <github-url>` (local flag lets you inspect before committing). Plugin structure lives in `.claude-plugin/marketplace.json`. To build your own plugin for sharing: bundle a skills folder, commands, hooks, and MCP configs together with a marketplace.json manifest. Use the `--agent` CLI flag to run Claude Code as a specific subagent: `claude --agent macOS-log-analyzer` to debug that agent's behavior directly.
