---
id: finish-every-migration-you-start
created: 2026-06-21
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny
---

# Always finish a migration you start

## TL;DR

Never leave a codebase half-migrated, partial migrations confuse both humans and the model and degrade Claude's output.

## Why it matters

A codebase with two competing patterns gives the model contradictory signals about "the right way," so it produces inconsistent code that drifts between the old and new style. Completing the migration removes the ambiguity and keeps the model's output coherent.

## How to apply

Treat a migration as atomic: scope it so it can be driven to completion (fan out with parallel agents/worktrees if it's large), and don't land it in a state where old and new patterns coexist long-term.

> "Always make sure that when you start a migration, you finish the migration.", Boris Cherny
