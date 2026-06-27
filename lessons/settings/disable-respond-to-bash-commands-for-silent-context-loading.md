---
id: disable-respond-to-bash-commands-for-silent-context-loading
created: 2026-06-27
status: active
supersedes: null
category: settings
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Disable respondToBashCommands if You Use ! Just to Load Context Silently

## TL;DR

`!` bash commands now trigger Claude to respond to their output automatically; set `respondToBashCommands: false` in settings.json to keep the old context-only behavior.

## Why it matters

If you run `!cmd` purely to drop its output into context (not to trigger a model turn), the new auto-response wastes a turn and tokens reacting to it. The toggle preserves `!` as a silent context loader.

## How to apply

To restore silent behavior, set `"respondToBashCommands": false` in settings.json. Per changelog 2.1.186.

## Related

[[inline-bash-in-slash-commands]]
