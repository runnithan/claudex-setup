---
id: tag-claude-on-prs-to-update-claude-md
created: 2026-06-21
status: active
supersedes: null
category: configuration
source_type: post
sources:
  - https://x.com/bcherny/status/2007179832300581177
---

# Tag `@claude` on Coworkers' PRs to Fold Review Feedback Into CLAUDE.md

## TL;DR

During code review, tag `@claude` on a PR (via the Claude Code GitHub Action, installed with `/install-github-action`) to add the lesson from your review comment to CLAUDE.md as part of that PR.

## Why it matters

This turns code review — where conventions and mistakes surface naturally — into the moment knowledge is captured, and captures learnings from coworkers' PRs, not just your own session. It automates the 'update CLAUDE.md after a correction' habit at team-review time.

## How to apply

Install the GitHub Action once with `/install-github-action`. When reviewing a PR and you spot something Claude should learn, tag `@claude` with the instruction; the action edits CLAUDE.md as part of the PR so the rule is checked in with the change that motivated it.

## Related

[[second-brain-after-session-knowledge-updates]], [[never-manually-maintain-config-let-claude-do-it]]
