---
id: portable-setup-via-open-standards
created: 2026-06-18
status: active
supersedes: null
category: configuration
sources:
  - transcripts/simon-scrapes/14-genius-ways-to-give-claude-code-superpowers_20260612.txt
---

# Build a Portable Setup on Open Standards to Avoid Vendor Lock-In

## TL;DR
Lean on cross-tool standards, `AGENTS.md`, the skills format, and MCP/CLI integrations, so your configuration survives a pricing change or a switch away from Claude Code.

## Why it matters
If Anthropic changes pricing or Claude Code becomes unavailable, a setup built on portable primitives keeps working in other agentic tools that read the same standards. The more your value lives in proprietary, tool-specific config, the higher the switching cost. Keeping context in [[team-agentic-os-shared-context-folders]] (external folders) is the same principle applied to team knowledge.

## How to apply
- Prefer `AGENTS.md` as the canonical instruction file where supported; Claude Code reads `CLAUDE.md`, but `AGENTS.md` is the emerging cross-tool standard (symlink or mirror if you want both).
- Keep skills in the open `skill.md` format so they can be imported elsewhere.
- Use MCP servers or plain CLI tools for integrations, both are platform-agnostic, rather than features unique to one client.
- Periodically sanity-check: "if I had to move tools tomorrow, what would I lose?" Push that surface toward zero.
