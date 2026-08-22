---
id: directive-not-aggressive-prompting
created: 2026-04-25
status: active
supersedes: null
category: prompting
sources:
  - transcripts/ray-amjad/anthropic-reveals-how-to-prompt-claude-code-10x-better_20260307.txt
  - transcripts/ray-amjad/the-top-0-01-user-s-guide-to-claude-code_20260307.txt
---

# Use Directive Prompts, Not Aggressive Ones, Include Your Reasoning

## TL;DR

Anthropic's internal guide: be explicit about scope, include the 'why' behind rules, avoid aggressive tone, and never use 'think' when thinking mode is off.

## Why it matters

Anthropic tested prompting strategies internally and found that aggressive tone degrades output. The model responds better to clear directives with reasoning. Including the 'why' behind rules (not just 'always use React 19' but 'always use React 19 because our CI pipeline only supports this version') helps Claude generalize the rule to edge cases. The word 'think' in a prompt when extended thinking is disabled wastes tokens as the model may attempt a think-style response that doesn't work.

## How to apply

Structure prompts as: [what to do] + [scope constraint] + [why]. Example: 'Modify the auth function in place, no new files, we need to keep the test suite passing without adding new test coverage. Our build pipeline doesn't support new file additions at this stage.' For rules in CLAUDE.md: include rationale after each rule. Replace aggressive language ('you must', 'never') with clear directives ('modify in place'). When extended thinking is off, use 'consider' or 'evaluate' instead of 'think'.
