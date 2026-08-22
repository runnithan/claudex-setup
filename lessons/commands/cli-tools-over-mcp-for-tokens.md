---
id: cli-tools-over-mcp-for-tokens
created: 2026-06-03
status: active
supersedes: null
category: commands
sources:
  - transcripts/john-kim/the-insane-story-of-openclaw_20260603.txt
  - transcripts/john-kim/what-is-agentic-ai-engineering-meta-staff-engineer-explains_20260603.txt
  - transcripts/john-kim/how-to-save-90-of-claude-code-token-usage_20260603.txt
---

# When an Agent Hits Friction, Build a CLI Tool: Not an MCP

## TL;DR

Prefer giving agents small CLI tools over MCPs: a CLI is read once then driven by command, is deterministic, self-documents via `--help`, and costs far less context than an MCP's loaded tool schemas.

## Why it matters

MCPs load tool schemas into context and negotiate opaquely; a CLI Claude can discover via `--help`/subcommands, drive predictably, and reuse across projects for a fraction of the tokens. This is the core move of harness/agentic engineering: remove a friction point by building a tool for it rather than doing it by hand or bolting on a heavy server. It complements `mcp-servers-as-usb-ports-choose-selectively`, still choose MCPs selectively, but reach for a CLI first when you control the integration.

## How to apply

At each manual or agent-blocked step, write a small CLI (Python/Node/Go) that exposes the action with semantic subcommands and a real `--help`, put it on `PATH`, and reference it in a skill or `CLAUDE.md` so Claude discovers it. Keep outputs predictable and machine-readable. Reuse the same CLIs across projects; over time your friction points become a personal tool belt the agent drives itself.
