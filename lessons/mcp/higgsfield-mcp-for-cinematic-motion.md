---
id: higgsfield-mcp-for-cinematic-motion
created: 2026-06-11
status: active
supersedes: null
category: mcp
sources:
  - transcripts/tristen-o-brien/claude-higgsfield-insane-cinematic-websites-master-in-7-minutes_20260610.txt
---

# Connect Higgsfield via MCP for Generated Video/Imagery in Web Projects

## TL;DR

Claude Code can't generate video itself; connecting Higgsfield as a custom MCP server lets it request cinematic video/image renders that land directly in the project folder, then wire them into the site (e.g., scroll-synced hero video via WebGL/Three.js).

## Why it matters

This closes the asset gap in design work: instead of stock footage or manual tooling, the same session that builds the page also generates its motion assets and integrates them, including effects like mapping scroll position to video frame index, which would otherwise require manual video editing.

## How to apply

Add Higgsfield as a custom MCP connector (settings → connectors → custom MCP → paste its URL → authorize). Then prompt inside the project: "Generate a hero video with Higgsfield: [description]", the render is written into the project folder. For scroll-sync, ask Claude to map scroll depth to playback frame with Three.js/WebGL. Per `mcp-servers-as-usb-ports-choose-selectively`, enable it only in projects that need generated motion assets.
