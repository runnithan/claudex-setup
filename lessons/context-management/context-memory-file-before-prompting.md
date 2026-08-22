---
id: context-memory-file-before-prompting
created: 2026-06-07
status: active
supersedes: null
category: context-management
sources:
  - transcripts/simon-scrapes/how-anthropic-teams-actually-use-claude-code-day-to-day-for-non-engineers_20260607.txt
---

# Load a Context Memory File Before Sending Work Prompts

## TL;DR

Create a memory/context file that tells Claude who you are and how you work before executing task prompts; this context matters more than prompt quality.

## Why it matters

Anthropic's non-engineering teams (legal, design, marketing, finance) consistently outperform by injecting context first rather than crafting perfect prompts. Context determines output quality more than prompt engineering does, the same prompt produces materially better output when Claude knows the operator's role and working style.

## How to apply

Create a CLAUDE.md or memory file that describes your role, working style, and preferences (e.g., "I'm a designer with little coding experience; give me smaller, incremental changes"). Load this as shared context before every task. Test by comparing outputs with and without the memory file on the same prompt, Anthropic teams report a 30–50% quality improvement. Complements `claude-md-hierarchy-keep-it-under-200-lines`: the persona/working-style block belongs in the curated top-level file, not in every prompt.
