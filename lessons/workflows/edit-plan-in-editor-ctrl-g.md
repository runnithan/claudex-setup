---
id: edit-plan-in-editor-ctrl-g
created: 2026-06-21
status: active
supersedes: null
category: workflows
source_type: canonical
sources:
  - https://code.claude.com/docs/en/best-practices
---

# Edit the Plan Directly with `Ctrl+G` Before Approving It

## TL;DR

In plan mode, press `Ctrl+G` to open the generated plan in your text editor and edit it in place before Claude executes — faster and more precise than negotiating changes turn-by-turn in chat.

## Why it matters

The best-practices guide documents `Ctrl+G` to open the plan in your editor for direct editing before Claude proceeds. Correcting the plan as text is more exact than describing edits conversationally, and the corrected plan becomes the spec Claude implements against.

## How to apply

Enter plan mode, let Claude draft the plan, hit `Ctrl+G`, tighten scope/ordering/out-of-scope notes in your editor, save, then approve. Combine with persisting the plan to a repo file so it survives compaction.

## Related

[[plan-mode-before-every-nontrivial-change]], [[plan-file-persistence-in-project-folders]]
