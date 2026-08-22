---
name: session-handoff
description: Write a handoff file so a stuck session can resume in the other tool without losing context. Use when asked to "hand this off", "switch to Codex", "switch to Claude Code", "write a handoff", "I'm stuck, try the other tool", or when a session has burned several attempts on the same problem.
argument-hint: "[target-tool]"
model: inherit
---

# Session Handoff

Capture everything the *other* tool needs to continue this task, and write it to `HANDOFF.md` in the repo root.

The receiving tool starts cold. It has none of the conversation, none of the reasoning, and no memory of what has already been ruled out. Without a handoff it re-explores ground this session already closed, and its first suggestion is usually something tried an hour ago.

Use this when switching Claude Code to Codex or back, typically because a session is stuck. A different model is genuinely useful on a stuck problem, but only if it starts from where you got to.

## When to use it

- Two or more failed attempts at the same problem, where a differently-trained model is worth trying.
- A long session about to be abandoned, whose reasoning is worth keeping.
- Work that must continue on another machine or after a restart.

Not for routine context trimming. `/compact` or a fresh session with a plan file covers that. This is specifically for crossing a tool boundary.

## What to write

Write `HANDOFF.md` with these sections. Be concrete and name real paths, commands and errors. Vagueness is what makes a handoff useless.

### 1. Task and definition of done

One paragraph on what is being attempted, then the finish line stated so it can be objectively checked. If the goal was fuzzy in this session, say so, because the receiving tool will otherwise invent a sharper one and solve the wrong problem.

### 2. Files in play

List each file touched or read closely, with one line on **why it matters**, not just that it was opened. A bare file list is close to worthless; the reason is the context.

### 3. Decisions made, and options rejected

Both halves. The rejected options matter more than the accepted ones: they are what a cold session re-litigates first, and re-arriving at a discarded approach wastes the entire benefit of the switch. For each rejection, record the reason, not just the verdict.

### 4. Current blocker

The precise failure. Paste the actual error text, the failing command, or the observed-versus-expected behaviour. Do not summarise an error message; the wording is often the clue.

### 5. Next things to try

Ordered, most promising first. Include anything this session suspected but did not get to.

### 6. Reproduce the state

The exact commands to get from a clean checkout to the current position: branch, services to start, migrations, environment variables that must be set. If a service must be running for the failure to appear, say so. Test suites that hang because a dependency is missing look like slowness rather than failure, and cost the receiving session real time.

## After writing it

Tell the user the file is written and give them the command to open the other tool on it, for example `codex "read HANDOFF.md and continue"`. Do not switch tools yourself.

Leave `HANDOFF.md` in place rather than deleting it at the end of the task; it is a useful record of why an approach was abandoned. Add it to `.gitignore` if the repo does not want it tracked.

## Notes

- Write the file even if the session feels short. The cost is a minute; the cost of the other tool re-deriving context is much larger.
- If the user names a target tool as an argument, tailor the reproduce section to it. Codex needs `AGENTS.md` conventions called out; Claude Code needs `CLAUDE.md` ones.
- Never include secrets, tokens or `.env` contents in the handoff. Reference the variable name and where it comes from instead.
