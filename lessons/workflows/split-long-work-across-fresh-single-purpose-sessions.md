---
id: split-long-work-across-fresh-single-purpose-sessions
created: 2026-06-27
status: active
supersedes: null
category: workflows
sources:
  - transcripts/nate-herk-ai-automation/how-to-never-hit-your-claude-session-limit-again__qZvORxGqI0_20260624.txt
---

# Split Long Work Across Fresh, Single-Purpose Sessions With File Handoffs

## TL;DR

Instead of letting one session degrade and auto-compacting at its worst moment, run a handoff while the model is still sharp — summarize decisions, key files, and open questions to a file, /clear, and start a fresh single-purpose session that reads it.

## Why it matters

Auto-compaction fires when context is already polluted, so it compresses at the model's least intelligent point and loses nuance. Splitting a project into short, specialized sessions (discovery, planning, execution), each handing the next a written summary, keeps every phase running on a fresh, focused context.

## How to apply

Build or invoke a handoff step that captures decisions, the files that matter, and what's left to do; write it to a file in the repo; /clear; then open the next session and have it read that file first. Keep each session scoped to one purpose and well under the model's effective window.

## Related

[[three-compact-rule-and-new-session-for-complex-plans]], [[plan-file-persistence-in-project-folders]], [[save-checkpoint-reset-on-drift]]
