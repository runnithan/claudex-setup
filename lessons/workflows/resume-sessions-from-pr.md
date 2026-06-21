---
id: resume-sessions-from-pr
created: 2026-06-21
status: active
supersedes: null
category: workflows
source_type: canonical
sources:
  - https://code.claude.com/docs/en/common-workflows
  - https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
---

# Resume the Exact Session Behind a PR with `claude --from-pr`

## TL;DR

Creating a PR via `gh pr create` auto-links the session to it; reopen that full context later with `claude --from-pr <number-or-url>` (or paste the PR URL into `/resume`) instead of starting cold on review feedback.

## Why it matters

The docs state that a session created via `gh pr create` is automatically linked to the PR and can be reopened with `--from-pr`. It also accepts GitLab MR, Bitbucket, and GitHub Enterprise URLs. Re-explaining a change in a fresh session loses the original implementation context.

## How to apply

Let Claude open PRs with `gh pr create` so the link is recorded. When review comments land, run `claude --from-pr 1234` to resume with the original context intact.

## Related

[[session-resume-keyboard-shortcuts]]
