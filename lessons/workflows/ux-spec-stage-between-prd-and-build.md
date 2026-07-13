---
id: ux-spec-stage-between-prd-and-build
created: 2026-07-02
status: active
supersedes: null
category: workflows
sources:
  - transcripts/sean-kochel/my-3-step-claude-skill-for-perfect-ux-design_nDHXLnwlIaY_20260702.txt
---

# Insert a UX-Spec Stage Between the PRD and the Build

## TL;DR

Add a dedicated UX-specification step between the PRD and implementation that pins down mental-model alignment, information architecture, affordances, and every UI state.

## Why it matters

A PRD says *what* works, not *how it should feel*. If affordances and states (empty / loading / error / incomplete) aren't specified up front, the model decides them "at game time" and cuts corners, producing generic vanilla UIs.

## How to apply

Chain three skills: PRD skill → UX-spec skill (mental model → information architecture → affordance/action → states, each stage building on the prior) → build-order skill that splits the spec into small sequential prompts (layout shell first, then details) because design tools handle large context poorly. Paste the build-order prompts one at a time rather than dumping the whole spec at once.

## Related

[[generate-ui-structure-first-then-inject-copy]], [[step-by-step-workflow-planning-before-session]], [[skill-systems-over-monolithic-skills]]
