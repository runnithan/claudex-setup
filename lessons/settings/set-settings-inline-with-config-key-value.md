---
id: set-settings-inline-with-config-key-value
created: 2026-06-27
status: active
supersedes: null
category: settings
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Set Any Setting Inline With /config key=value (Works in -p and Remote Control)

## TL;DR

Use `/config key=value` to change any setting straight from the prompt instead of opening the interactive menu — and it works in headless (-p) and Remote Control sessions, where the menu doesn't.

## Why it matters

Toggling a setting mid-task used to require navigating the interactive /config UI, which isn't available in -p or remote contexts at all. Inline syntax is scriptable and remote-safe.

## How to apply

Type e.g. `/config thinking=false` to flip a setting in place; run `/config --help` to list the shorthand keys. Per changelog 2.1.181: '/config key=value syntax ... works in interactive, -p, and Remote Control.'

## Related

[[never-manually-maintain-config-let-claude-do-it]]
