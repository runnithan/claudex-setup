---
id: omit-session-url-from-commits-with-attribution-setting
created: 2026-06-27
status: active
supersedes: null
category: configuration
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Set attribution.sessionUrl to Keep claude.ai Session Links Out of Commits and PRs

## TL;DR

The `attribution.sessionUrl` setting omits the claude.ai session link that web and Remote Control sessions otherwise stamp into commit messages and PR bodies.

## Why it matters

Web and Remote Control sessions inject a claude.ai session URL into commit/PR text; in public, shared, or publicly-mirrored repos that leaks an internal link and clutters an otherwise clean commit history.

## How to apply

Set `attribution.sessionUrl` (to omit) in settings for repos where you want clean, link-free commit and PR text. Per changelog 2.1.183: 'Added attribution.sessionUrl setting to omit the claude.ai session link from commits and PRs in web and Remote Control sessions.'

## Related

[[tag-claude-on-prs-to-update-claude-md]]
