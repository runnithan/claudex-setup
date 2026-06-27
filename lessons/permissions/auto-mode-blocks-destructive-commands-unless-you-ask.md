---
id: auto-mode-blocks-destructive-commands-unless-you-ask
created: 2026-06-27
status: active
supersedes: null
category: permissions
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# In Auto Mode, Explicitly Ask for Destructive git/terraform Commands or They're Blocked

## TL;DR

Auto mode now blocks destructive git commands (reset --hard, checkout -- ., clean -fd, stash drop, unrequested --amend) and terraform/pulumi/cdk destroy unless you explicitly asked for that specific action.

## Why it matters

Autonomous runs could previously nuke local work or tear down infrastructure on their own. The guard means an unsupervised task will silently NOT run these unless your prompt requested it — so you have to phrase destructive intent clearly.

## How to apply

When you genuinely want a destructive op during an unattended run, state it explicitly ('discard my local changes with git reset --hard', 'destroy the staging stack'); otherwise expect auto mode to block it. Per changelog 2.1.183.

## Related

[[auto-mode-permissions-for-unsupervised-runs]]
