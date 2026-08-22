---
id: task-system-replaces-todo-list
created: 2026-04-25
status: superseded
supersedes: null
superseded_by: todo-and-task-tools-removed-on-modern-models
category: workflows
sources:
  - transcripts/ray-amjad/claude-code-s-new-task-system-explained_20260307.txt
  - transcripts/ray-amjad/claude-code-s-biggest-update-in-months_20260307.txt
  - transcripts/john-kim/claude-code-s-new-agent-teams-are-insane-opus-4-6_20260424.txt
---

# Use the Task System for Multi-Session Dependency Tracking

## TL;DR

Tasks live in `.claude/tasks/`, support `blocks`/`blocked_by` dependencies, and notify sibling sessions in real time via the same CLAUDE_CODE_TASK_LIST_ID.

## Why it matters

The old ad-hoc todo list approach breaks down across sessions and agents. The task system gives tasks a persistent identity, dependency graph, and cross-session notification. Two Claude sessions pointing to the same task list ID will see each other's task updates in real time, enabling genuine multi-session coordination without agent teams.

## How to apply

Set `CLAUDE_CODE_TASK_LIST_ID` in the `env` section of settings.json for auto-sharing across sessions. Tasks are created with TaskCreate, updated with TaskUpdate (set to `in_progress` when starting, `completed` when done), queried with TaskGet/TaskList. Set dependencies: `{"blocks": ["task-id-2"], "blocked_by": ["task-id-1"]}`. Tasks are stored as JSON in `.claude/tasks/`. Use Ctrl+T to view the task list inline while agent teams are running.
