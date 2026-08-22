---
id: team-agentic-os-shared-context-folders
created: 2026-06-07
status: active
supersedes: null
category: configuration
sources:
  - transcripts/simon-scrapes/how-to-build-an-agentic-os-your-whole-team-can-actually-use_20260607.txt
---

# Use Shared External Context Folders for a Team OS to Decouple Knowledge From Interface

## TL;DR

Store editable team knowledge (procedures, templates, brand guidelines) in Notion or Google Drive, not Claude Code's native storage, resilient to tool changes and editable by non-technical teammates.

## Why it matters

Building a team agentic OS purely inside Claude Code creates lock-in: institutional knowledge ends up trapped in one tool's config format, and only technical teammates can maintain it. Teams that use external tools as the source of truth can switch AI tools without losing knowledge, and anyone can update a procedure.

## How to apply

Create a shared Notion workspace or Google Drive folder with: `procedures/` (step-by-step workflows), `brand-context/` (voice profiles, guidelines), `templates/`, and an `index.md`. Point Claude Code to these sources (via MCP or a fetch script). When the team updates procedures externally, Claude picks them up next session without code changes. Builds on `shared-brand-context-folder-for-all-skills`, same single-source-of-truth idea, extended to team scale and external storage.
