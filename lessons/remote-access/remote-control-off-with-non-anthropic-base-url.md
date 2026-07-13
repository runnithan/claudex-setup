---
id: remote-control-off-with-non-anthropic-base-url
created: 2026-07-02
status: active
supersedes: null
category: remote-access
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Routing to a Non-Anthropic Base URL Disables Remote Control

## TL;DR

If you point `ANTHROPIC_BASE_URL` at a non-Anthropic host (OpenRouter, local Ollama, a proxy), Remote Control is switched off — so you can't drive that session from your phone/browser.

## Why it matters

The 2.1.196 changelog: "Remote Control is now disabled when `ANTHROPIC_BASE_URL` points at a non-Anthropic host, matching the existing behavior under `CLAUDE_CODE_USE_BEDROCK`/`_VERTEX`/`_FOUNDRY`." This is a direct trade-off against [[route-claude-code-to-cheaper-or-local-models]]: you lose remote/phone access on those sessions.

## How to apply

Reserve cheaper/local base-URL routing for sessions you'll only drive from the terminal; keep the default Anthropic endpoint (and Bedrock/Vertex/Foundry off) on any session you need to control remotely via `claude rc`. Don't burn time debugging "Remote Control unavailable" — check your base URL first. See [[remote-control-channels-for-phone-access]].
