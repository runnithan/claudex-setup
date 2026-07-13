---
id: hook-matchers-exact-match-not-substring
created: 2026-07-02
status: active
supersedes: null
category: automation
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Write Hook Matchers as Exact Names or Regexes — They No Longer Substring-Match

## TL;DR

Hook matchers now exact-match the tool name instead of substring-matching, so a matcher like `mcp__brave-search` silently stops firing — use a regex such as `mcp__brave-search__.*` to catch a family of tools.

## Why it matters

The 2.1.195 changelog fixed hyphenated matchers (e.g. `code-reviewer`, `mcp__brave-search`) that were "accidentally substring-matching — they now exact-match." Any hook you wrote expecting a partial match will quietly never run, and a matcher for one MCP server won't cover its individual tools. Comma-separated matchers (e.g. `"Bash,PowerShell"`) also used to silently never fire and were fixed in 2.1.191.

## How to apply

Audit every hook matcher in settings.json: to match all tools of a hyphenated MCP server use a regex like `mcp__brave-search__.*`, not the bare server name; give exact tool names (`Bash`, `Edit`) where you want one tool; re-verify comma-separated matchers still fire after upgrading. See [[hooks-for-automation-and-guardrails]].
