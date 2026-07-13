---
id: learn-technical-vocabulary-for-precise-prompts
created: 2026-07-01
status: active
supersedes: null
category: prompting
sources:
  - transcripts/austin-marchese/how-i-used-claude-code-to-build-a-481k-app_8Z6p-61NH4E_20260628.txt
---

# Learn the ~40 Technical Terms, Not the Code — One Right Word Fixes Claude's Output

## TL;DR

Non-technical (or cross-stack) builders don't need to learn the language; they need its vocabulary. Claude is trained on precise technical terms, so "debounce the search input" or "use a websocket for real-time sync" moves the output from wrong to right far faster than describing the behavior in prose.

## Why it matters

Vague intent ("I want edits to show up instantly") leaves Claude guessing between very different implementations (polling vs websockets), and you pay for the wrong guess in extra iterations. The right term collapses that ambiguity in one shot — and there are only a few dozen terms that cover most of what you'll ask for.

## How to apply

Build a working vocabulary of ~40 core terms and reach for them in prompts: component, modal, toast, debounce, throttle, memoize, lazy-load, pagination, infinite scroll, optimistic update, websocket vs polling, responsive breakpoint, happy path vs edge case, race condition, idempotent, migration, listener/subscription. When a result is off, suspect an imprecise word before rewriting the whole prompt. Keep the list in a reference file so it's easy to extend as you hit new concepts.
