---
id: agents-wizard-removed-edit-agents-dir
created: 2026-07-02
status: active
supersedes: null
category: agents
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# The /agents Wizard Is Gone — Edit .claude/agents/ or Ask Claude to Manage Subagents

## TL;DR

Claude Code removed the interactive `/agents` wizard; create or edit subagents by writing files in `.claude/agents/` directly or by asking Claude to do it.

## Why it matters

The 2.1.198 changelog states: "Removed the `/agents` wizard; ask Claude to create or manage subagents, or edit `.claude/agents/` directly." Guidance or muscle memory that says to run `/agents` to scaffold a subagent is now dead and will just fail.

## How to apply

Define subagents as markdown files under `.claude/agents/<name>.md` with frontmatter (name, description, tools, model), or prompt Claude "create a subagent that does X" and let it write the file. Don't look for the wizard. Related: [[spawn-teammates-via-the-agent-name-param-no-teamcreate]].
