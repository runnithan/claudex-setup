---
id: design-tool-mcp-for-design-as-code-builds
created: 2026-07-02
status: active
supersedes: null
category: mcp
sources:
  - transcripts/sean-kochel/google-stitch-antigravity-never-hire-a-designer_NprG-SGd4-A_20260702.txt
  - transcripts/sean-kochel/how-i-design-pro-app-uis-full-workflow_IFlxdcyCPz4_20260702.txt
---

# Connect a Design-Tool MCP So Claude Builds From Design-As-Code

## TL;DR

Instead of screenshotting or scraping HTML, wire a design tool's MCP server and skills into your project so Claude reads the structured design JSON and builds pixel-perfect.

## Why it matters

Downloading images or raw HTML and reverse-engineering them into React/Tailwind produces poor, ambiguous output. A design-as-code JSON (tokens, components, sizing, do's/don'ts) leaves no ambiguity for the model to guess at.

## How to apply

Google Stitch: paste its MCP raw config into your IDE's MCP config, add your Stitch API key (Stitch settings → create key), install the Stitch Skills library into the project, then prompt "Use the stitch MCP and stitch skills to build out [project] from our account." Pencil.dev exposes a bidirectional MCP that piggybacks on your existing Claude subscription and serves a `.pen` JSON of every screen/component — run it in plan mode and point Claude at the screens to build.

## Related

[[generate-ui-structure-first-then-inject-copy]], [[hand-off-claude-design-exports-to-claude-code]], [[mcp-servers-as-usb-ports-choose-selectively]]
