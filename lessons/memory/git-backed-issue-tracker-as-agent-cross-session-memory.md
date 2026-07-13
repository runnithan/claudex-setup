---
id: git-backed-issue-tracker-as-agent-cross-session-memory
created: 2026-07-02
status: active
supersedes: null
category: memory
source_type: post
sources:
  - https://steve-yegge.medium.com/beads-best-practices-2db636b9760c
  - https://github.com/steveyegge/beads
---

# Give Your Coding Agent a Git-Backed Issue Tracker as Cross-Session Memory

## TL;DR

Agents wake up with no memory of yesterday's work; a git-backed, dependency-graph issue tracker (e.g. Steve Yegge's Beads/`bd`) gives them persistent, mergeable memory across sessions and parallel agents.

## Why it matters

Yegge built Beads to fix the "50 First Dates" problem — agents start each session with no memory of prior work. It stores issues as JSONL in `.beads/` committed to git, makes dependencies first-class (blocks / depends_on / parent-child), and adds multi-agent claim semantics (`bd update --claim` atomically sets assignee+status) so concurrent sessions don't grab the same task or clobber each other in git. It's tool-agnostic, so it complements Claude Code's in-session tasks ([[task-system-replaces-todo-list]]) by adding durable cross-session state.

## How to apply

Add a git-backed tracker to the repo and instruct the agent: file an issue for any work longer than ~2 minutes; plan first, then file epics/issues with explicit dependencies before implementing; file issues as it reviews code. Run one task per agent — kill the process and start fresh between tasks. Maintain it: run `bd doctor`/`bd cleanup` regularly and keep the DB small (roughly under 200–500 issues).
