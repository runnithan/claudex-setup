---
id: claude-design-draw-to-code
created: 2026-06-11
status: active
supersedes: null
category: workflows
tool: claude-design
sources:
  - transcripts/tristen-o-brien/claude-design-basics-master-95-in-10-minutes_20260610.txt
---

# Sketch UI Directly on the Claude Design Canvas Instead of Describing Layout in Words

## TL;DR

In Claude Design, use the draw tool to sketch boxes and wireframes on the canvas — Claude interprets the shapes as UI components (sidebar, hero image, button) and builds them, and the tweaks panel swaps themes/palettes without re-prompting.

## Why it matters

Spatial layout is painful to specify in prose ("a sidebar on the left, about 20% width, with…"). A rough sketch communicates the same intent in seconds and removes a whole class of layout misunderstandings. Tweaks (dark/light mode, palette swaps) avoid burning a prompt round-trip on cosmetic changes.

## How to apply

When a design needs specific layout, click draw on the Claude Design canvas and sketch the regions: a tall box for a sidebar, a wide rectangle for the hero, small shapes for buttons. Annotate sparingly, then let Claude generate. Use the tweaks controls for theme and palette variations instead of prompting for them.
