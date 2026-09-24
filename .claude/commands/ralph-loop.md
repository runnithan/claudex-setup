---
description: "Start a Ralph Loop, iterative self-referential development loop"
argument-hint: "PROMPT [--max-iterations N] [--completion-promise TEXT]"
allowed-tools: ["Bash(.claude/scripts/setup-ralph-loop.sh:*)"]
---

# Ralph Loop Command

Execute the setup script to initialize the Ralph loop:

```!
.claude/scripts/setup-ralph-loop.sh $ARGUMENTS
```

Please work on the task. When you try to exit, the Ralph loop will feed the SAME PROMPT back to you for the next iteration. You'll see your previous work in files and git history, allowing you to iterate and improve.

Keep a running implementation-notes.md recording decisions and tradeoffs you had to make and anything else the reviewer should know; it gets read before the diff.

CRITICAL RULE: If a completion promise is set, you may ONLY output it when the statement is completely and unequivocally TRUE. Do not output false promises to escape the loop, even if you think you're stuck or should exit for other reasons.

SAFE EXIT: If the task turns out to be infeasible or blocked on something outside this loop's control, say so and stop: reporting infeasibility, with the evidence, is a valid completion, not a failure (it is NOT the completion promise; never output that falsely). Do not retry the same failing approach more than twice.

EVIDENCE: do not stop at a plausible implementation or the first successful build. Before claiming an iteration's work is done, audit each claim against a tool result from this run and say plainly which claims are not yet verified. Where the task has an objective check (a test, a command, a rendered output), run it and quote the result; where it has none, write down what good looks like and how it would be tested. "The tasks I listed are done" is satisfied by code that exists and was never exercised, which is why it is not the stopping condition.
