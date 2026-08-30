---
id: mcp-servers-as-usb-ports-choose-selectively
created: 2026-04-25
status: superseded
superseded_by: stop-pruning-mcp-servers-tool-search-loads-schemas-on-demand
supersedes: null
category: configuration
sources:
  - transcripts/ray-amjad/anthropic-just-added-these-features-to-claude-code_20260307.txt
  - transcripts/ray-amjad/huge-claude-code-update-new-model-mobile-u0026-web-app_20260307.txt
  - transcripts/andrew-codesmith/900-hours-of-learning-claude-code-cursor-in-10-minutes_20260307.txt
  - transcripts/simon-scrapes/200-hours-of-claude-code-lessons-in-14-minutes-for-business-owners_20260424.txt
---

# Install MCP Servers Selectively, Each One Costs Context Window Space

## TL;DR

MCPs with many tools trigger auto tool-search (at 10% threshold by default), which adds overhead. Disable selectively with @<server> toggle.

## Why it matters

MCP servers add their tools to the context window, competing with your conversation for space. With many tools, the model uses a tool-search mechanism (auto-enabled at 10% threshold) that adds an extra round trip before each tool call. The Supabase MCP in particular can access and potentially delete your database if given write access, the power requires care.

## How to apply

Toggle individual MCP servers on/off mid-session with `@<server-name>` + Enter (e.g., `@supabase` to toggle). Set the tool-search threshold in settings.json: `MCP_TOOL_SEARCH_THRESHOLD=0.15` to trigger auto-search only when >15% of context is MCP tools. For skills that use an MCP, use skill-scoped hooks to restrict the MCP's access to only the specific operations the skill needs (read-only API key pattern). Give Supabase and similar MCPs read-only API keys unless write access is specifically needed for the task.
