---
id: state-change-breadth-explicitly-maximal-or-minimal
created: 2026-07-02
status: active
supersedes: null
category: prompting
sources:
  - transcripts/sean-kochel/i-didn-t-know-these-claude-code-rules-big-mistake_ynVfOd_ioDg_20260702.txt
---

# State the Breadth of a Change Explicitly to Control Scope Creep

## TL;DR

Newer Claude models follow explicit scope instructions precisely, so say whether you want a maximal build-out or a minimal surgical change.

## Why it matters

Left unspecified, Claude either under-delivers a basic version or over-engineers — breaking working code with unrequested edits and extra files. The model can't infer your risk tolerance; you have to state it.

## How to apply

For greenfield richness: "include as many relevant features and interactions as possible, go beyond the basics." For tight edits: "only make changes that are directly requested; keep the solution simple and focused" — to stop it touching unrelated code or adding janky workarounds. Match the phrasing to the blast radius of the file you're in.

## Related

[[engineer-vs-pirate-mindset]], [[yagni-cost-persists-when-agents-generate-code]], [[ask-for-options-before-changes-to-gauge-blast-radius]]
