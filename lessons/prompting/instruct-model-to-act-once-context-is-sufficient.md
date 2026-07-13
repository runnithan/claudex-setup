---
id: instruct-model-to-act-once-context-is-sufficient
created: 2026-07-02
status: active
supersedes: null
category: prompting
sources:
  - transcripts/nate-herk-ai-automation/how-anthropic-engineers-actually-prompt-fable-5_vcU85OrwuV0_20260702.txt
---

# Tell the Model to Act Once It Has Enough Context

## TL;DR

Replace "research everything and make a full plan first" with "when you have enough information to act, then act" to stop the model burning minutes over-planning.

## Why it matters

On hard tasks at high reasoning effort, models can run for many minutes gathering context and self-planning before doing anything. An explicit act-when-ready instruction curbs this — the Anthropic-engineer walkthrough dropped default plan-mode in favor of it.

## How to apply

Add a standing instruction for build/execution tasks: "When you have enough information to act, act." Pair it with an explicit stop rule for pure diagnostic tasks (see [[assessment-only-mode-for-diagnostic-tasks]]) so "act when ready" doesn't cause it to take unrequested actions on questions.

## Related

[[assessment-only-mode-for-diagnostic-tasks]], [[plan-mode-before-every-nontrivial-change]], [[directive-not-aggressive-prompting]]
