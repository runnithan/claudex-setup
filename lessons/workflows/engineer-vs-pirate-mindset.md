---
id: engineer-vs-pirate-mindset
created: 2026-07-01
status: active
supersedes: null
category: workflows
sources:
  - transcripts/austin-marchese/how-i-used-claude-code-to-build-a-481k-app_8Z6p-61NH4E_20260628.txt
---

# Split Work Into Engineer-Mode and Pirate-Mode by Blast Radius

## TL;DR

Give business-critical paths (auth, payments, data integrity) slow, reviewed "engineer-mode" treatment; give low-risk work (UI tweaks, content, non-critical features) fast "pirate-mode" screenshot-and-iterate. Applying the same rigor to both wastes time on safe work and under-tests dangerous work.

## Why it matters

The cost of a bug is wildly uneven: a broken auth or payment flow means lost revenue and lost trust, while a wrong button color is one screenshot and one fix. Treating every change with the same caution burns your review attention on things that don't matter and, worse, spreads it too thin to properly guard the things that do.

## How to apply

In CLAUDE.md, explicitly label your critical workflows (login, payment, schema migrations, anything touching user data) as "engineer-side" and require a gate for them — plan mode, `/code-review`, and a verification step before merge. Mark everything else "pirate-side" and let Claude iterate fast: build, run/screenshot, fix, repeat, in one loop. Reserve `/verify` and multi-agent review for engineer-side changes. Re-tier a feature the moment its blast radius changes (a cosmetic component that starts writing to the database moves to engineer-side).
