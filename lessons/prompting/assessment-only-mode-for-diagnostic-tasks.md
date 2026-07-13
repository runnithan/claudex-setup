---
id: assessment-only-mode-for-diagnostic-tasks
created: 2026-07-02
status: active
supersedes: null
category: prompting
sources:
  - transcripts/nate-herk-ai-automation/how-anthropic-engineers-actually-prompt-fable-5_vcU85OrwuV0_20260702.txt
---

# Constrain Side Effects With an Explicit Assessment-Only Rule

## TL;DR

For diagnostic or question tasks, spell out what the model must NOT do so it reports findings instead of silently fixing, sending, editing, or deleting things.

## Why it matters

Models try to be helpful and take unrequested actions. Naming the forbidden actions — like briefing an intern on what not to touch — reliably prevents premature edits or sends; explicit negative constraints work well on current models.

## How to apply

Use a reusable snippet: "When I'm describing a problem or asking a question, the deliverable is your assessment. Report what you find and stop. Don't fix, send, edit, or delete anything until I say go." Keep it in config once rather than appending to every prompt. Complements act-when-ready by governing autonomous side effects specifically.

## Related

[[instruct-model-to-act-once-context-is-sufficient]], [[ask-for-options-before-changes-to-gauge-blast-radius]], [[directive-not-aggressive-prompting]]
