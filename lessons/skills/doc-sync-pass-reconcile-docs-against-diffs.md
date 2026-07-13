---
id: doc-sync-pass-reconcile-docs-against-diffs
created: 2026-07-02
status: active
supersedes: null
category: skills
sources:
  - transcripts/sean-kochel/this-tech-ceo-s-claude-code-toolkit-will-blow-you-away_MM320sAhFoY_20260702.txt
---

# Run a Doc-Sync Skill That Reconciles Docs Against Your Diffs Before Committing

## TL;DR

After a batch of changes, run a skill that diffs the changed files, cross-references every doc, resolves contradictions, prunes dangling TODOs, and only then commits.

## Why it matters

Fast AI-assisted coding leaves README / architecture / changelog / TODOs stale, and later work reads those out-of-date docs and breaks in ways that are hard to trace. A structured doc-release pass keeps documentation honest against what the code actually does.

## How to apply

Keep a structured docs folder (README, architecture, contribution guidelines, changelog, TODOs, design artifacts). Build a "doc release" skill that: finds the diffs, cross-checks each doc for conflicts with what changed, updates stale docs, quizzes you on risky changes, verifies docs don't contradict each other, prunes dangling TODOs, then commits and bumps the version. Run it as the last step before every commit batch.

## Related

[[second-brain-after-session-knowledge-updates]], [[verify-touched-symbols-after-agent-says-done]], [[classify-skills-into-four-types]]
