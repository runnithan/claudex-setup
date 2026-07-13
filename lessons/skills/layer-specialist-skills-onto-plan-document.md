---
id: layer-specialist-skills-onto-plan-document
created: 2026-07-02
status: active
supersedes: null
category: skills
sources:
  - transcripts/sean-kochel/7-claude-code-skills-every-beginner-needs-to-master_m3jiIowIi5I_20260702.txt
---

# Harden a Plan Document by Running Specialist Skills Against It

## TL;DR

Point domain skills at your `plan.md` (not just at code) to progressively revise the plan before any implementation begins.

## Why it matters

Chaining specialist skills against a planning artifact catches best-practice gaps while changes are still cheap (editing prose, not rewriting shipped code). In the demo an API-design skill produced a REST migration plan, then a Postgres table-design skill rewrote that same plan to conform to database best practices — all before a single line was built.

## How to apply

Generate a plan with one specialist skill, clear context, then invoke the next specialist skill referencing the plan file so it updates the document in place: e.g. "use the Postgres table-design skill to update our REST API migration plan." Repeat per relevant domain (API → DB → security → …) before executing. Pairs with writing the plan to a durable file so each skill re-reads the latest version.

## Related

[[plan-file-persistence-in-project-folders]], [[skill-systems-over-monolithic-skills]], [[plan-mode-before-every-nontrivial-change]]
