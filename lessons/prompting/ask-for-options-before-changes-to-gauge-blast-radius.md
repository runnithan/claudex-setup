---
id: ask-for-options-before-changes-to-gauge-blast-radius
created: 2026-06-21
status: active
supersedes: null
category: prompting
source_type: post
sources:
  - https://steipete.me/posts/just-talk-to-it
---

# When Unsure of Impact, Ask for a Few Options Before Any Edits

## TL;DR

For a change whose scope you can't predict, prompt 'give me a few options before making changes' — a lightweight, read-only probe that surfaces the blast radius before the agent touches files.

## Why it matters

Letting an uncertain agent edit straight away risks a sprawling, hard-to-review commit. A read-only options pass shows how many files and which approaches are in play, so you can pick the contained one cheaply — a faster, in-band alternative to full plan mode for medium-uncertainty tasks.

## How to apply

Prompt 'give me a few options before making changes,' read the options, choose the contained one, then let it execute. Works the same in Claude Code as the Codex post describes.

## Related

[[plan-mode-before-every-nontrivial-change]]
