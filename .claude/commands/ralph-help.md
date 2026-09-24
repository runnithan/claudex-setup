---
description: "Explain Ralph Loop plugin and available commands"
---

# Ralph Loop Help

Explain the following to the user:

## What is Ralph Loop?

Ralph Loop implements the Ralph Wiggum technique, an iterative development methodology based on continuous AI loops, pioneered by Geoffrey Huntley.

**Core concept**: The same prompt is fed to Claude repeatedly. Claude sees its own previous work in files and git history, building incrementally toward the goal.

**Each iteration:**
1. Claude receives the SAME prompt
2. Works on the task, modifying files
3. Tries to exit
4. Stop hook intercepts and feeds the same prompt again
5. Claude sees its previous work in the files
6. Iteratively improves until completion

## Available Commands

### /ralph-loop PROMPT [OPTIONS]

Start a Ralph loop in your current session.

**Options:**
- `--max-iterations <n>`, Max iterations before auto-stop
- `--completion-promise <text>`, Promise phrase to signal completion

**Examples:**
```
/ralph-loop Refactor the cache layer --max-iterations 20
/ralph-loop Add tests --completion-promise "TESTS COMPLETE"
/ralph-loop Fix the auth bug --completion-promise "FIXED" --max-iterations 10
```

### /cancel-ralph

Cancel an active Ralph loop (removes the loop state file).

## When to Use

**Good for:** Well-defined tasks with clear success criteria, tasks requiring iteration, greenfield projects.

**Not good for:** Tasks requiring human judgment, one-shot operations, unclear success criteria.

## Limitation: no fresh context per iteration

This loop runs inside your current session. The Stop hook feeds the same prompt back, but the
context window is never cleared between iterations, so a long loop accumulates context and
degrades the way one long session does. A true Ralph loop gives every pass a fresh context that
reads only the task files.

For fresh-context iterations, relaunch a new headless session per pass from a shell loop with an
iteration cap, for example `for i in $(seq 20); do claude -p "$(cat PROMPT.md)"; done`. A headless
run cannot answer permission prompts, so pre-approve the tools the task needs.
