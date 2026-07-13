---
id: force-explore-and-read-before-implementing
created: 2026-07-02
status: active
supersedes: null
category: workflows
sources:
  - transcripts/sean-kochel/i-didn-t-know-these-claude-code-rules-big-mistake_ynVfOd_ioDg_20260702.txt
---

# Force Explore-and-Read Before Implementing (Opus Under-Explores by Default)

## TL;DR

Opus is conservative about scanning the codebase before acting and will sometimes infer a file's contents from conventions instead of reading it — add a standing rule that makes it explore and read first.

## Why it matters

Solutions that look thorough fall apart on implementation because the model didn't read enough surrounding code, or guessed a file's structure/parameters/functions and built against a wrong mental model. This causes subtle breakage that's hard to trace back.

## How to apply

Add an explore-first instruction (or a custom `/explore-first` command) that runs a defined sequence before coding: list the directory structure, find related files, read them deeply, summarize the patterns, then decide the implementation. Include a hard rule: "Never assume or speculate about what's inside a file; read and investigate it fully before implementing anything based on it." Especially valuable for multi-file changes and debugging.

## Related

[[verify-touched-symbols-after-agent-says-done]], [[steer-agent-to-vertical-slice-and-root-cause]], [[treat-ai-junior-dev-specific-tight-context]]
