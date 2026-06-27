---
id: authenticate-mcp-servers-from-the-cli
created: 2026-06-27
status: active
supersedes: null
category: mcp
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Authenticate MCP Servers From the CLI With claude mcp login/logout

## TL;DR

`claude mcp login <name>` and `claude mcp logout <name>` authenticate an MCP server from the CLI without opening the interactive /mcp menu, with `--no-browser` stdin-redirect support for completing OAuth over SSH.

## Why it matters

Re-authenticating an MCP server used to require the interactive /mcp menu, which is awkward in headless, scripted, or SSH sessions. CLI auth makes it automatable and remote-friendly.

## How to apply

Run `claude mcp login <name>` to (re)auth a server; add `--no-browser` to complete the OAuth flow over SSH; `claude mcp logout <name>` clears it. Per changelog 2.1.186.

## Related

[[mcp-servers-as-usb-ports-choose-selectively]]
