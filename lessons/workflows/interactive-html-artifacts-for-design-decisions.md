---
id: interactive-html-artifacts-for-design-decisions
created: 2026-04-25
status: active
supersedes: null
category: workflows
sources:
  - transcripts/ray-amjad/even-anthropic-engineers-use-this-claude-code-workflow_20260424.txt
  - transcripts/ray-amjad/anthropic-reveal-how-to-make-claude-code-a-better-designer_20260307.txt
---

# Generate Interactive HTML Artifacts for Design Variations and Data Exploration

## TL;DR

Ask Claude to make 10 design variations in one HTML file; use Bun for a hot-reloading interactive artifact with comment export.

## Why it matters

When you don't know what you want but will know it when you see it (especially for UI design), having Claude generate 10 distinct variations in a single HTML file is dramatically faster than iterating one design at a time. Interactive artifacts let you leave comments on specific elements, export them as JSON, and paste back into Claude for targeted updates, all without polluting the main conversation.

## How to apply

Ask: 'For the Retrieval Settings card, give me 10 variations in one HTML file, each fairly distinct, following the same light theme.' Browse variations, identify what you like. For interactive feedback: 'Make this a Bun interactive artifact with hot reload on localhost, clickable comment bubbles, and an export-to-JSON button in the top right.' Leave comments on elements, export JSON, paste into Claude: 'Apply these comments as changes.' For skill outputs: build HTML artifact generation into the final step of any skill where you're choosing between multiple options.
