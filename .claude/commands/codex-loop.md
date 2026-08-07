---
description: Use Codex as a second, differently-trained reviewer of your branch, fix every real finding with regression tests, and loop until two consecutive reviews come back clean. Runs autonomously.
argument-hint: "[base-branch] [--max-rounds N]"
model: opus
---

# /codex-loop — review, fix, repeat until clean

Run `codex review` against a base branch, fix what it finds, and keep looping
until **two consecutive rounds** return no findings. **Run autonomously.** Do
not report back between rounds and do not ask permission to continue; the point
is that the owner starts it and walks away.

**`--base` is the COMPARISON point, not the branch under review.** Run this from
the feature branch you are working on; `--base main` then reviews everything
that branch adds on top of `main`. Do not check out the base branch to run it.
Default base is `main`.

**There is no round cap by default.** Run as many rounds as it takes.
`--max-rounds N` sets an optional ceiling. The stop conditions in §6 are the
real terminators, and they are what keep this from being an infinite loop.

Fixes run on **Opus** (pinned in this file's frontmatter). Triage is the hard
part of this loop, and a cheaper model tends to apply findings literally, which
is the exact failure §2 exists to prevent.

Requires the Codex CLI, authenticated, with `codex review` available
(`codex review --help`).

---

## 0. Before the first round

1. **Start whatever services the test suite needs** (database container, etc.).
   A suite whose dependency is missing often does not fail cleanly — it *hangs*,
   which reads like a slow suite rather than a missing dependency and can burn
   half an hour before you notice. Start dependencies first, and if a suite
   runs far longer than its usual time, suspect a missing service before
   suspecting the tests.
2. Confirm the working tree is clean apart from the work you intend to review.
3. **Create or resume the state file** `.planning/codex-loop/STATE.md` (or the
   project's equivalent scratch location). This loop runs long enough to be
   compacted mid-flight and everything that matters between rounds otherwise
   lives only in context. If the file exists with an unfinished run, RESUME
   from it rather than restarting the count.

```markdown
# codex-loop state
base: main
started: <HEAD sha at round 1>
round: <n>
consecutive_clean: <0..2>
max_rounds: none

## Rounds
- R1: 4 findings -> 4 fixed (sha, sha, ...)
- R2: 3 findings -> 2 fixed, 1 rejected (reason)
- R4: 2 findings, all self-inflicted x2 -> fixed by Codex (escalation) (sha, sha)

## Rejected (do not re-litigate)
- <finding> — <evidence it is not real, or why the suggested fix is wrong>

## Flagged, deliberately not fixed
- <finding> — <why>

## Self-inflicted
- <finding> — caused by <sha> earlier in this loop
```

## 1. Run the review

```bash
codex review --base <base> > /tmp/codex-review-<n>.log 2>&1
```

- **Run it in the background and REDIRECT to a file. Never pipe it through
  `tail`, `head`, or a pager** — the pipe buffers everything until the process
  exits, so a long run shows nothing at all and you cannot tell progress from a
  hang.
- Expect **10–15 minutes** on a multi-commit branch. That is normal.
- It runs as its own child thread and reads the `review_model` config key, **not
  `model`**. If unset it inherits `model`, which means a later change to `model`
  silently moves your reviews too. There is no review-specific effort key;
  reviews inherit `model_reasoning_effort`.
- The CLI prints its summary block **twice**. Cosmetic; parse either copy.
- Findings are the block after the last `^codex$` line.

## 2. Triage every finding before touching code

**Do not apply findings literally.** A reviewer can be right about the symptom
and wrong about the fix. For each finding decide:

- **Real, fix as described** — proceed.
- **Real, but the suggested fix is wrong** — fix it properly and say why in the
  commit message.
- **Not real** — reject it and record the evidence in the state file.

Check these every time. Each has produced a wrong suggestion in practice:

1. **Is it actually new?** Grep for the same pattern elsewhere. If the "new"
   code merely mirrors existing behaviour, fixing only the new site makes the
   codebase inconsistent. Either fix the whole class, or fix the new site and
   **document explicitly** that the older ones still have it. Do not silently
   change legacy behaviour as a side effect.
2. **Does an existing test or comment encode the opposite intent?** A test that
   fails after your fix is evidence, not an obstacle — read it before editing
   it. An assertion that looks pedantic (object identity, a "no copy" contract)
   is often pinning a deliberate decision.
3. **Would the fix add a heuristic to a path that has already caused
   regressions?** If so, prefer flagging over fixing, and say why. Some findings
   are cheaper to accept than to guard against.

## 3. Fix, and prove it

- Trace the real call chain before changing anything. Verify the premise against
  the code, **including what the client actually sends** — a server-side
  assumption about request payloads is a classic source of wrong fixes (a field
  the UI sends as an explicit `null` behaves nothing like one it omits).
- Write a regression test that **fails before the fix**. A test that encodes
  your assumption rather than the system's real behaviour is worse than none: it
  will pass while the bug ships.
- Follow the repo's own conventions (commit format, authorship, prose rules).

## 4. Verify with the project's own checklist

Do not invent verification commands. Read the project's `CLAUDE.md` / `AGENTS.md`
"done when" checklist and run exactly that, for each stack whose **code**
changed. A change touching no code in a stack does not owe that stack's checks.

Redirect long runs to a file. If a test fails intermittently, **re-run the same
code before concluding** — distinguish a real regression from a load-sensitive
flake by evidence, not by assumption.

## 5. Commit

One commit per finding. Explain **why** and name the failure mode in plain
language. If a finding was caused by an earlier fix in this same loop, say so
and reference that commit. **Never push.**

## 6. Loop

Go back to §1.

### Stop when any of these is true

- **TWO CONSECUTIVE rounds return zero findings.** The success condition. One
  clean round is not enough: counts oscillate, and an empty round is often
  followed by a round that finds real problems once the reviewer examines a
  different slice. Increment `consecutive_clean` on an empty round and **reset
  it to 0 the moment a round finds anything**, including a finding you reject.
- **A round returns only findings you would push back on.** Chasing those makes
  the code worse. Stop and report. Does NOT count as a clean round.
- **A round returns only findings already in the Rejected section.** The
  reviewer is re-raising settled ground; more rounds will not converge. Check
  the state file BEFORE fixing, so a re-raise is recognised rather than
  re-litigated into a bad fix.
- **A Codex-authored fix round (§6a) is followed by another round of
  self-inflicted findings in the same area.** Both models are now introducing
  problems there — that is a genuine fix-and-introduce cycle, not convergence.
  Report the area as needing a design change rather than more patches.
- **A finding needs an owner decision** — a product call, a one-way door, or
  anything requiring a push or a deploy. Stop, ask, then resume.
- **`--max-rounds N` reached**, if supplied.

Expect the count to oscillate rather than fall monotonically. Each fix opens new
surface for the next round. A round producing **no new self-inflicted findings**
is a better convergence signal than a low count — which is the other reason the
bar is two clean rounds, not one.

## 6a. Escalation — hand self-inflicted findings to the reviewer

**Trigger: two consecutive rounds where every new finding was self-inflicted**
by fixes made earlier in this loop. That pattern means the fixing model keeps
re-introducing the same class of problem; do not write the next fix yourself.
Instead, let Codex — which keeps spotting the issue — attempt the fix:

```bash
codex exec --full-auto "<prompt>" > /tmp/codex-fix-<n>.log 2>&1
```

- The prompt must contain: the findings verbatim, the relevant file paths, the
  constraint to fix ONLY those findings, and the requirement to add a
  regression test per finding. Same output hygiene as §1: background, redirect
  to a file, never pipe through a pager.
- **You still own triage, verification, and commits.** Diff what Codex changed,
  run the §4 checklist, and commit per §5 — one commit per finding, noting in
  the commit message that the fix was authored by Codex via escalation.
- Record the round in the state file as `fixed by Codex (escalation)` and
  reset the self-inflicted streak. Then resume the loop at §1.
- This escalation fires at most once per area. If the round after a
  Codex-authored fix again returns self-inflicted findings in the same area,
  that is the stop condition in §6 — both models are churning the same ground,
  and the answer is a design change, not another patch.

## 6b. Surviving compaction

This loop reliably outlives a single context window, often several. Treat
compaction as routine, not failure, and never end the loop early to avoid one.

- **Update the state file at the end of EVERY round**, before starting the next
  review. Losing "why I rejected finding X" is what causes a later round to
  re-litigate it into a bad fix.
- **When context runs low, compact and continue.** Do not stop and do not ask.
  After compacting, re-read the state file first, then resume.
- Keep long tool output OUT of context: reviews and test runs redirect to files;
  read only the findings block or the summary line. That alone is most of what
  makes long runs survivable.
- Commits are the other half of durability. A finding that is fixed, tested and
  committed is safe from any context loss; one that is only fixed in the working
  tree is not. Commit per finding rather than batching.

## 7. Final report

One summary at the end, not per round:

- Findings per round, and the trend.
- What was fixed, grouped by area, with commit SHAs.
- **Which findings were caused by fixes earlier in this loop.** Be explicit;
  this is the most useful signal about which areas are genuinely hard.
- What was rejected, and the evidence.
- What was flagged but deliberately not fixed, and why.
- Final suite counts, and confirmation that nothing was pushed.
