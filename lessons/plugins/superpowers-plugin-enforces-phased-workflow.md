---
id: superpowers-plugin-enforces-phased-workflow
created: 2026-06-27
status: active
supersedes: null
category: plugins
sources:
  - transcripts/nate-herk-ai-automation/this-one-plugin-just-10x-d-claude-code_4XqVR6xI6Kw_20260624.txt
---

# Install a Workflow-Enforcing Plugin (e.g. Superpowers) to Force Plan → Build → Verify

## TL;DR

Install a workflow-enforcing plugin such as Jesse Vincent's Superpowers, which chains skills that push Claude through brainstorming, design, planning, test-driven coding, and verification before it considers a task done.

## Why it matters

Left to itself, Claude jumps to coding and skips discovery, which produces expensive rework. A plugin that auto-fires a phased workflow imposes structure you'd otherwise have to remember to prompt for every time, improving output quality on non-trivial work.

## How to apply

Install the plugin via /plugin (browse the marketplace for the current package name — verify it rather than copying a command blindly) so it loads globally and fires at task start. Pair it with a brainstorming/alignment step before coding. You don't memorize the constituent skills; they invoke automatically.

## Related

[[plugin-system-install-from-marketplace]], [[skill-systems-over-monolithic-skills]]
