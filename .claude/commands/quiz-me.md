---
description: "Review an agent-written change by being examined on it: quizzes you on the diff, diagrams what moved, and turns the questions you cannot answer into the review findings. Use after a large agent-produced change instead of reading every line."
argument-hint: "[git-range|commit|pr-number] [--n 6] [--diagram-only]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git diff:*), Bash(git log:*), Bash(git show:*), Bash(git status:*), Bash(gh pr diff:*), Bash(gh pr view:*)
---

# /quiz-me: examine me on this change

You are reviewing by examination, not by summary. Reading an agent-written diff line by line
does not scale with the rate agents produce code, and a summary tells me what the author thinks
happened. A quiz inverts it: the gaps in *my* understanding surface actively, and the questions
I cannot answer are the review findings. You are strictly **read-only**: never edit, fix, commit,
or run anything that changes state.

Arguments: `$ARGUMENTS`

## 1. Resolve the change

Interpret the arguments in this order:
- a git range (`main..HEAD`, `abc123..def456`) or a single commit/ref: use `git diff` / `git show`;
- a PR number or URL: `gh pr diff <n>` for the diff and `gh pr view <n> --json title,body,files`
  for the framing;
- nothing: the working tree diff (`git diff` plus `git diff --cached`); if that is empty, the last
  commit (`git show HEAD`).
- `--n N` sets the number of questions (default 6). `--diagram-only` stops after step 3.

State what you resolved in one line ("Quizzing on `main..HEAD`, 14 files, +612/-88") before going on.

## 2. Read it properly

Read the whole diff, then enough of the surrounding code to know: which callers are affected,
which invariants or data shapes changed, where the error paths go, what the changed tests
actually prove, and what the diff looks like it touches but does not. Do not quiz from the diff
alone; a question about a caller you never opened is a guess.

## 3. Orient me

One paragraph: what moved and why, in plain language. Then a compact diagram (mermaid, or ASCII
if mermaid would not render here) of the touched components and the edges that are new or
changed. Mark removed edges too. Keep it to what the diff changed; this is a map of the change,
not of the system.

## 4. Quiz

Ask `N` questions, all at once, numbered, ordered from structural to edge cases. Every question
must be one a reviewer has to be able to answer before approving, and prefer questions whose
wrong answer would be a merge mistake:
- why this was changed, not just what;
- what happens when a specific input, state, or failure occurs on the new path;
- which callers or consumers are affected, and which one is easy to miss;
- what a changed or added test actually proves, and what it does not;
- what was deliberately left alone, and why that is safe;
- plus **one trap**: something the diff looks like it does but does not (or the reverse).

Do not hint at answers. Tell me to answer inline by number, and that "reveal N" gives me the
answer to one question without grading it.

## 5. Grade

For each answer: **right**, **partial**, or **wrong**, followed by the evidence, a quoted diff
line or file:line reference. Produce every quoted snippet from an executed command (`git diff`,
`git show`, `sed -n`), never retyped. Then the findings: each wrong or unsure answer becomes one
entry stating exactly what I should read (file and lines) and whether it is a knowledge gap on my
side or a real problem in the code. Do not soften a wrong answer, and do not pad the list with
things I got right.

## 6. Verdict

One line: **ready to approve**, or **read these N spots first**, or **this diff has a real
problem at ...** (name it). If the verdict is the third kind, say whether a test would have caught
it and which one.

## Rules

- Read-only. Do not edit, fix, format, commit, push, or open anything.
- Never invent. Every claim about the change cites a diff line or a file:line you opened.
- Keep your own narration short; the output that matters is the diagram, the questions, and the
  findings.
