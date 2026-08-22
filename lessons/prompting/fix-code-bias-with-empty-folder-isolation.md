---
id: fix-code-bias-with-empty-folder-isolation
created: 2026-04-25
status: active
supersedes: null
category: prompting
sources:
  - transcripts/ray-amjad/the-top-0-01-user-s-guide-to-claude-code_20260307.txt
---

# Fix Design Bias by Starting in an Empty Folder

## TL;DR

When existing code anchors Claude to poor patterns, start Claude in an empty folder to generate clean solutions, then port back.

## Why it matters

Claude's outputs are heavily influenced by what it reads in your existing codebase. If your current code has a poor architecture or a mediocre design pattern, Claude will tend to extend it rather than introduce something better. Starting in an empty folder eliminates this anchoring bias completely.

## How to apply

Create a new empty directory: `mkdir /tmp/fresh && cd /tmp/fresh`. Start a new Claude session. Give it only the relevant spec, reference files, and context, no existing code. Let it generate the clean implementation. Review the output, then bring just the relevant parts back into your main project. This is especially useful for: new feature architectures, UI redesigns, and fixing technical debt patterns.
