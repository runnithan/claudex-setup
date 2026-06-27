---
id: spawn-teammates-via-the-agent-name-param-no-teamcreate
created: 2026-06-27
status: active
supersedes: null
category: agents
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Spawn Agent-Team Teammates via the Agent name Param — No TeamCreate Step

## TL;DR

The TeamCreate/TeamDelete tools have been removed; with CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 every session has one implicit team and you spawn teammates simply by passing a `name` to the Agent tool.

## Why it matters

The old flow required an explicit team-creation call before spawning teammates; that setup step is gone, and any guidance to 'create a team first' is now obsolete.

## How to apply

Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, then spawn a teammate by calling the Agent tool with a `name` parameter — no setup. The `team_name` parameter is accepted but ignored. Per changelog 2.1.178.

## Related

[[agent-teams-for-cross-domain-collaboration]], [[shut-down-agent-teams-gracefully]]
