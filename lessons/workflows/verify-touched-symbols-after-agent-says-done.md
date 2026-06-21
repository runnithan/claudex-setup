---
id: verify-touched-symbols-after-agent-says-done
created: 2026-06-21
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://sourcegraph.com/blog/agentic-coding
---

# After an Agent Says 'Done,' Grep Every Usage of the Symbols It Touched

## TL;DR

On an established codebase, when Claude reports a task complete, search the repo for all other usages of the symbols it changed; if a callsite turns up that Claude never opened, the task isn't actually done.

## Why it matters

Claude plans from the files it happened to find locally. As Yegge puts it: if the agent finds three relevant files it plans on three; if the real change affects 17 files across 9 repos, it doesn't know and won't ask. Approximate retrieval misses cross-cutting impact, so incomplete edits slip through as false completions.

## How to apply

Make 'verify the invisible 20%' a finishing step: search the codebase for any other usage of the symbols the agent touched with exact/deterministic Grep (not fuzzy recall), surface every callsite and interface implementer, then point Claude at the ones it missed. Gate the result on the same CI as human commits.

## Related

[[finish-every-migration-you-start]]
