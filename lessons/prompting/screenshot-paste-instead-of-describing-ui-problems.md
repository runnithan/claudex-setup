---
id: screenshot-paste-instead-of-describing-ui-problems
created: 2026-06-18
status: active
supersedes: null
category: prompting
sources:
  - transcripts/simon-scrapes/every-claude-code-concept-explained-for-non-coders_20260615.txt
---

# Paste a Screenshot Instead of Describing a UI Problem

## TL;DR
When a layout or visual bug is hard to put into words, screenshot it and paste the image into Claude Code rather than describing it, Claude reads the image and locates the exact problem.

## Why it matters
Prose description of a visual defect is lossy: "the header overlaps the nav" forces Claude to reconstruct a picture you already have. A pasted screenshot is precise, Claude sees the overlap, the spacing, the broken alignment directly, and fixes the right thing on the first try. This is the input-side complement to [[visual-self-validation-screenshot-grading]] (where Claude screenshots its own output).

## How to apply
1. Capture the broken UI (OS screenshot tool, or the browser).
2. Paste the image straight into the Claude Code prompt.
3. Say "fix this" or "the layout is broken here", no lengthy description needed.

Claude analyzes the image, identifies the cause (e.g. a CSS overlap or wrong flex direction), and implements the fix.
