---
id: goal-verifiable-finish-lines-with-safety-caps
created: 2026-06-11
status: active
supersedes: null
category: workflows
sources:
  - transcripts/tristen-o-brien/claude-code-just-dropped-goal-master-it-in-8-minutes_20260610.txt
---

# Give /goal a Verifiable Finish Line and a Safety Cap

## TL;DR

Use `/goal` with a measurable, observable finish line (e.g., "every transaction categorized and summed in a spreadsheet") plus an explicit safety cap ("stop after 25 turns") so the verifier knows when to stop and a vague condition can't burn tokens forever.

## Why it matters

`/goal` runs a boss/worker loop until a condition is met. A vague condition ("make it good", "no mistakes") is unverifiable, so the loop never converges and token spend runs away. A concrete finish line lets the checking agent test "done or not" objectively each turn; the cap bounds the worst case.

## How to apply

Phrase the goal as something an agent can verify by inspection: `/goal Every transaction from my bank PDFs is categorized in the spreadsheet with monthly totals. Stop after 25 turns.` Include the turn/time limit in the same prompt every time. If you can't state an observable completion test, the task isn't ready for `/goal`, use a normal session or plan mode first.
