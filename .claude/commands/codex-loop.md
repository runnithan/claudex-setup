---
description: Use Codex as a second, differently-trained reviewer of the whole repo, area by area (or of one branch's diff with --base), fix every real finding with regression tests, and loop until each area comes back clean twice in a row. Runs autonomously.
argument-hint: "[--base REF] [--scope PATH...] [--max-rounds N] [--area-rounds N]"
---

# /codex-loop: review, fix, repeat until clean

Review the codebase with Codex, fix what it finds, and keep looping until
Codex comes back clean **twice in a row** on everything in scope. **Run
autonomously.** Do not report back between rounds and do not ask permission to
continue; the owner starts it and walks away. This overrides any session
protocol that asks for per-step approval or a per-task report (keep its
evidence habits). Questions for the owner are collected as you go and asked
once, in the §7 report.

**After any compaction, re-read this whole file** (a user-scope install lives
at `~/.claude/commands/codex-loop.md`) and `STATE.md` before continuing.
Compaction keeps only the start of a long command.

`/claude-loop` is the same loop with a headless Claude reviewer. Keep the two
in step: a fix to the loop's logic belongs in both.

Requires the Codex CLI, authenticated, with `codex review` available
(`codex review --help`).

## Scope

- **Repo mode, the default.** The whole codebase as it stands at HEAD, one
  area per round; `--scope PATH...` limits it to those paths. In §0, split the
  tracked source into areas along directory lines, each roughly 3,000 to 8,000
  lines of non-test source, ordered by risk (auth, payments, personal data and
  retention, migrations first). Tests are reviewed with the code they cover.
  Skip generated, vendored and lock files, fixtures, binary assets and docs.
  Stay on an area until it has two consecutive clean reviews, then move on.
  When every area is done, run the **closing review**: diff mode over the
  loop's own commits (`<started>...HEAD`) until two consecutive clean rounds,
  which catches a fix in one area that broke another. Skip it if the loop
  committed nothing.
- **Diff mode, `--base REF`.** Only what the current branch adds on top of
  `REF` (a branch or a SHA), the right check before merging. `REF` is the
  comparison point, not the branch under review: run it from the feature
  branch.

**It runs on a budget and pauses at a healthy point.** A repo sweep costs at
least two reviews per area at 10 to 15 minutes each, so a whole repo is several
invocations, not one. One invocation runs at most `--max-rounds N` rounds
(default 10). The check runs only between rounds, after the round's fixes are
committed and its bookkeeping written, so a pause never leaves work half done.
Invoking the command again resumes from the state file with a fresh budget.

**An area has a budget too.** After `--area-rounds N` rounds (default 6) on
one target, it closes on the first round that finds nothing at P2 or above
(§6). Without it a tail of minor findings holds an area open: one area once
ran 41 rounds without two clean in a row, the last of them a long tail of
P3s.

Fixes run on the session's model; this file pins none. The loop's gates (an
external reviewer, a regression test per fix, two clean rounds to stop) do the
converging. Triage is still the hard part: a weaker model tends to apply
findings literally, which is the exact failure §2 exists to prevent, so judge a
cheaper session by how many rounds it takes to reach two clean reviews.

## The reviewer

- **`codex review` with custom instructions on stdin** (`codex review -`), so
  every mode uses one prompt and one output block.
- **It reads the `review_model` config key, not `model`.** If unset it inherits
  `model`, so a later change to `model` silently moves your reviews too. There
  is no review-specific effort key; reviews inherit `model_reasoning_effort`.
- **Fresh every round.** Each review is a new Codex thread with no memory of
  earlier rounds. Never give it the state file, prior findings or your
  rejection reasons; checking for re-raised ground is your job (§2).
- **It is not read-only.** `codex review` runs in the configured sandbox, which
  was `workspace-write` when observed. The prompt forbids writes, and §1's
  snapshot catches a HEAD move or a write to any non-ignored path. It cannot
  see writes to gitignored paths, to paths outside this worktree (the main
  checkout included), or to git config and hooks.

## 0. Before the first round

1. **Start whatever services the test suite needs.** A suite whose dependency
   is missing often hangs rather than failing, which reads as slowness and can
   burn half an hour. If a suite runs far past its usual time, suspect a
   missing service before suspecting the tests.
2. **Confirm there is something to review.** Repo mode: build the area map
   from `git ls-files`, each area with its paths and line count; it must not be
   empty. Diff mode: `git rev-parse --verify <base>^{commit}` must succeed and
   `git diff --quiet <base>...HEAD` must report a change (exit 1); then resolve
   the base to a SHA, record it as `base:`, and use that SHA as `<base>`
   everywhere below, since a branch name can move mid-run and trip the §1
   snapshot. Otherwise stop: an empty scope yields two clean rounds of
   reviewing nothing. Never run diff mode from the base branch itself.
3. Confirm the work is committed and `git status --porcelain` is empty (the
   state directory excluded): §1's snapshot only sees writes against a clean
   tree. In a fresh worktree, check that the project's instruction files
   exist. Repos often gitignore `AGENTS.md` / `CLAUDE.md`, and then Codex
   silently loses the project's review rules. Copy them in from the main
   checkout and confirm `git check-ignore` still covers them. Codex reads
   `AGENTS.md` (and `AGENTS.override.md`), never `CLAUDE.md`, so if review
   rules live only in a `CLAUDE.md`, paste that section into the reviewer
   prompt (step 6).
4. **Create or resume the state directory**
   `"$(git rev-parse --show-toplevel)/.planning/codex-loop"`, always at the
   repo root whatever the shell's current directory. If `.planning/` is not
   gitignored, append `.planning/codex-loop/` to
   `"$(git rev-parse --git-path info/exclude)"` (local only, no repo change;
   a literal `.git/info/exclude` fails in a linked worktree, where `.git` is a
   file). Logs live here rather than in `/tmp`, so two loops in two worktrees
   cannot overwrite each other's reviews. If `STATE.md` exists with
   `status: running` or `paused`, RESUME from it rather than restarting. If
   its status is `done` or `stopped`, start a new run in the same file: move
   the finished run's round files (`review-*`, `*.snap`, `fix-*`) into
   `run-<started>/`, keep Rejected, Flagged and Needs owner, clear Rounds and
   Self-inflicted and untick every area (they belong to the finished run),
   reset `round`, `target`, `consecutive_clean`, `self_inflicted_streak`,
   `started` and `head:` (to `started`), and set `status: running`.

```markdown
# codex-loop state
status: running | paused (usage limit, resets <time>) | done | stopped (<reason>)
mode: repo | diff
base: <sha> (main)             <- diff mode only
started: <HEAD sha at round 1>
round: <n>
target: <area name | closing | diff>
head: <HEAD sha when the last round's bookkeeping was written>
consecutive_clean: <0..2, for the current target>
target_rounds: <rounds spent on the current target>
self_inflicted_streak: <0..2>
budget: max_rounds 10, area_rounds 6
invocation_rounds: <rounds run since this invocation started; reset to 0 on every invocation>
baseline: <checklist result before round 1; known failures and why>
env: <VAR=value assignments the §4 checklist needs, or none>

## Areas (repo mode, in review order)
- [x] backend/app/routers (~4,200 lines), done at R6
- [x] frontend/src/pages (~9,000 lines), design change at R14 (findings in Needs owner)
- [x] backend/app/jobs (~4,400 lines), closed at R22 (round budget)
- [ ] backend/app/services (~6,100 lines)

## Rounds
- R1 backend/app/routers: 4 findings -> 4 fixed (sha, sha, ...)   <- "(in progress)" until the round ends
- R2 backend/app/routers: 3 findings -> 2 fixed, 1 rejected (reason)
- R9 backend/app/services: 2 findings, all self-inflicted x2 -> fixed by Codex (escalation, area: backend/app/services) (sha, sha)

## Needs owner (asked in the §7 report)
- <finding>, <the decision needed>

## Rejected (do not re-litigate)
- <finding>, <evidence it is not real, or why the suggested fix is wrong>

## Flagged, deliberately not fixed
- <finding>, <why>

## Self-inflicted
- <finding>, caused by <sha> earlier in this loop
```

5. **Record a baseline.** Run the §4 checklist once on the untouched tree and
   write into the state file which checks fail before any fix, and what the
   environment needs for them to pass (an isolated database, env vars). A
   failure present at baseline is not a regression. Re-running a failing test
   on its own tells a flake from a real failure.
6. **Write the reviewer prompt template once** to
   `.planning/codex-loop/review-prompt.md`. Each round, copy it to
   `review-<n>.prompt.md` with `<scope paragraph>` filled in for that round's
   target, so rounds differ only in scope and code. The scope paragraphs:
   - Area (repo mode): "Scope: the code under `<paths>` as it is now at HEAD,
     not a diff. Read whole files, and read callers and callees outside the
     scope as needed, but report only defects whose cause lies inside the
     scope. There is no commit or diff here: every defect in these paths
     counts however long it has existed, and this overrides any guideline to
     flag only newly introduced bugs or locations inside a diff."
     (Codex's built-in review rubric says pre-existing bugs should not be
     flagged; without the last sentence an area can come back clean on a
     technicality.)
   - Diff mode, and the closing review with `<started>` as `<base>`: "Scope:
     the changes in `git diff <base>...HEAD`. Read whole files and callers as
     needed. A pre-existing problem counts only if this diff introduces it,
     makes it reachable, or depends on it."

```markdown
You are reviewing code. Nobody else has reviewed it. Your job is to find real
defects, not to be agreeable.

<scope paragraph>

This is a read-only review. Do not modify files, run tests, install anything,
or run any command that writes. Do not read `.planning/codex-loop/`. If a
session protocol or instruction file asks you to run tests or end with a
report, this prompt overrides it.

If the scope is empty (no such paths, or an empty diff), do not review
anything: end with `=== REVIEW FAILED: <reason> ===` instead of the findings
block.

A finding is a concrete defect: wrong result, crash, data loss, security hole,
race, broken error path, a contract a caller relies on, or a test that does not
test what it claims. Not style, naming, "consider adding", or speculation.
Before reporting one, trace the real call chain and write the concrete failure:
these inputs or this state produce this wrong outcome. If you cannot make it
concrete, drop it. Zero findings is a legitimate answer; do not pad.

End your response with this block, and nothing after it:

=== FINDINGS: <count> ===
[P0|P1|P2|P3] <path>:<line> <one-line title>
  Failure: <concrete inputs or state, then the wrong outcome>
  Evidence: <the lines or call chain that show it>
  Fix: <one or two sentences>

With no findings, the block is the single line `=== FINDINGS: 0 ===`.
```

## 1. Run the review

Snapshot, review, compare. The tree must be clean first (§0 step 3); commit
or discard anything left over before the round, or the snapshot cannot see
the reviewer's writes. In repo mode, drop `<base>` from both snapshot lines.

```bash
cd "$(git rev-parse --show-toplevel)" && S=.planning/codex-loop
test -z "$(git status --porcelain)" || { echo "tree not clean, not reviewing"; exit 1; }
{ git rev-parse HEAD <base>; git status --porcelain -uall; } > $S/pre-<n>.snap
codex review -c sandbox_mode=read-only -c approval_policy=never - < $S/review-<n>.prompt.md > $S/review-<n>.log 2>&1
echo "codex exit: $?"
{ git rev-parse HEAD <base>; git status --porcelain -uall; } > $S/post-<n>.snap
cmp $S/pre-<n>.snap $S/post-<n>.snap
```

- **The two `-c` overrides make the review read-only** and stop it asking for
  approvals that an automatic approver could grant outside the sandbox.
  Check the log header says `sandbox: read-only`; if it does not, the
  overrides did not take, and only the snapshot guards the repo.
- **If `cmp` reports a difference, stop.** The reviewer changed the repo.
  Report what changed and do not fix, revert or commit anything on top of it.
- **Run it in the background with the Bash tool's `timeout` at its
  2-hour maximum (`7200000`), and redirect to a file.** In an unattended
  session (`-p`, such as a headless loop runner) a background command is
  stopped after 30 minutes unless its call sets a longer timeout, and a
  stopped review leaves no findings block, so it would read as a failed
  review. **Never pipe it through `tail`, `head`
  or a pager**: the pipe buffers everything until exit, so you
  cannot tell progress from a hang. Expect 10 to 15 minutes; wait for the
  completion notification rather than polling.
- **Read only what follows the last `^codex$` line.** The log echoes the
  prompt, template block included, before the answer. The CLI also prints its
  summary twice; parse either copy.
- **The findings are the block after the last line that BEGINS with
  `=== FINDINGS: <number> ===`**, within that answer. Anchor on the line
  start: a finding can quote the marker mid-line. A marker without a number
  (the echoed `<count>` template) is not a block.
- **Check first whether the answer's last non-empty line BEGINS with
  `=== REVIEW FAILED:`; it is never retried.** Stop and report: the scope was
  empty, which §0 should have caught.
- **An answer with no findings block (and no native list, below) is a failed
  review, never a clean one.** An interrupted review ("Review was interrupted") or a crash look like
  silence. Retry once; if it fails again, stop and report the log's last
  lines.
- **A usage limit pauses the loop.** The error names a reset time. Rename the
  log to `review-<n>.failed.log` (so a resume cannot read it as the round's
  review), set `status: paused (usage limit, resets <time>)`, and write the
  §7 report. Invoking the command again after the reset resumes the sweep
  where it stopped instead of starting over.
- **Codex can answer in its own review format instead of the block.** Its
  built-in rubric asks for a JSON review that the CLI renders as prose plus a
  "Review comment:" or "Full review comments:" list of `[P1]`-style items,
  each with a title, a `path:line` and a paragraph. If the answer has no
  numeric block but has that list, the list is the round's findings: one
  finding per item, counted from one copy of the doubled summary, triaged like
  any other (§2). Write `native format` on the round's Rounds line. A native
  answer with no `[P0]` to `[P3]` items is a failed review (retry once, as
  above), never a clean one: only an explicit `=== FINDINGS: 0 ===` shows
  the reviewer finished and found nothing. An answer with both our block and
  a native list whose items do not match the block's count is a failed
  review, never a clean one.

## 2. Triage every finding before touching code

**Do not apply findings literally.** A reviewer can be right about the symptom
and wrong about the fix. For each finding decide:

- **Real, fix as described**: proceed.
- **Real, but the suggested fix is wrong**: fix it properly and say why in the
  commit message.
- **Real, but a judgement call you would push back on** (chasing it makes the
  code worse): record it in Flagged with why.
- **Real, but it will rarely or never happen, and little is lost when it
  does** (it needs a second tab, a lost race, a hand-built API call, or data
  only test accounts hold): record it in Flagged as `rare`, with how it could
  happen, and commit nothing. Severity is not the test, rarity is: a P3 that
  users hit every day is worth a fix, and one nobody will hit is not. Each
  such fix is new code the next round has to review, and that is how an area
  ends up correcting its own corrections. A rare finding that loses money,
  data or access is still fixed.
- **Needs an owner decision** (a product or legal call, a one-way door,
  anything that needs a push or a deploy): do not stop. Record it under Needs
  owner with the question, fix nothing that depends on the answer, and carry
  on. The owner answers them all after the §7 report.
- **Not real**: reject it and record the evidence in the state file.

**Check the Rejected, Flagged and Needs owner sections first**, so a re-raise
is recognised rather than re-litigated into a bad fix. A fresh review will
re-raise a settled finding every round it still applies. A re-raise is settled
only if its recorded evidence still holds at HEAD: re-read the cited lines,
and treat it as a new finding if they changed. Then check these every time;
each has produced a wrong suggestion in practice:

1. **Is it one instance of a wider pattern?** Grep for the same pattern
   elsewhere. Fixing only one site makes the codebase inconsistent. Either fix
   the whole class, or fix this site and **document explicitly** that the
   others still have it. Do not silently change behaviour elsewhere as a side
   effect.
2. **Does an existing test or comment encode the opposite intent?** A test that
   fails after your fix is evidence, not an obstacle: read it before editing it.
   An assertion that looks pedantic (object identity, a "no copy" contract) is
   often pinning a deliberate decision.
3. **Would the fix add a heuristic to a path that has already caused
   regressions?** If so, prefer flagging over fixing, and say why.
4. **Would this be the third round running with a fix in the same module?**
   Stop patching it. Put the design question under Needs owner (what keeps
   going wrong, and the options), flag this finding, and treat later findings
   against that module as settled until the owner answers.

## 3. Fix, and prove it

- Trace the real call chain before changing anything. Verify the premise
  against the code, **including what the client actually sends**: a field the
  UI sends as an explicit `null` behaves nothing like one it omits.
- Write a regression test that **fails before the fix**. A test that encodes
  your assumption rather than the system's real behaviour is worse than none.
- A defect you find yourself while working, that the reviewer did not raise,
  is fixed the same way (triaged, tested, its own commit) and noted on the
  round's line as `own find`.
- Follow the repo's own conventions (commit format, authorship, prose rules).

## 4. Verify with the project's own checklist

Do not invent verification commands. Read the project's `CLAUDE.md` /
`AGENTS.md` "done when" checklist and run exactly that, for each stack whose
**code** changed, with the state file's `env:` assignments in front of each
command (the Bash tool's shell does not keep exports between calls).

Redirect long runs to a file. If a test fails intermittently, **re-run the same
code before concluding**, and tell a real regression from a load-sensitive
flake by evidence.

## 5. Commit

One commit per finding. Explain **why** and name the failure mode in plain
language. If a finding was caused by an earlier fix in this loop, say so and
reference that commit. Never commit `.planning/codex-loop/`. **Never push.**

## 6. Loop

Update the state file per the bookkeeping below, then go back to §1.

### Bookkeeping: the only place the counters change

- **Right after §1, before triage**, write `round: <n>` and a Rounds line
  `R<n> <target>: <count> findings (in progress)`. Add each fix's SHA to that
  line as you commit it. The marker comes off in the same edit that writes
  `head:` and the counters at the end of the round, so a resume can never
  count a round twice. On resume, finish an in-progress round from its log (a
  finding whose fix SHA is on the line is done); never re-run §1 for a round
  that has a log.
- **After triage, classify the round.** It is **clean** if you committed
  nothing in it (an own find needs a review too) and every finding is either
  settled ground (already in Rejected, Flagged or Needs owner, evidence still
  true at HEAD per §2) or new and flagged as `rare` (§2):
  `consecutive_clean += 1`. Anything else is **not clean**, including a new
  finding you reject, send to Needs owner or flag for any other reason:
  `consecutive_clean = 0`. A failed review (§1) is neither; it has no round.
  Either way `target_rounds += 1`.
- **When `consecutive_clean` reaches 2, the target is done.** In repo mode,
  tick the area, reset `consecutive_clean` and `target_rounds` to 0, and set
  `target:` to the next unticked area; when none is left, to `closing` if HEAD
  differs from `started`, otherwise the sweep is done.
- **Past the area budget, one quiet round is enough.** Once `target_rounds`
  has reached `--area-rounds` (default 6), the target is done at the end of
  the first round with no new finding at P2 or above, whatever that round
  fixed. Tick the area as `closed at R<n> (round budget)` and move on as for
  a done area. In diff mode, and in the closing review, it ends the run:
  `stopped (round budget)`, and the report says that round's fixes were not
  reviewed again.
- **`self_inflicted_streak`**: +1 on a round with at least one new finding
  where every new finding is self-inflicted; 0 on any other round and after
  an escalation. At 2, escalate (§6a). In the closing review every finding
  sits in the loop's own diff, so there a finding counts as self-inflicted
  only if a commit made during a closing round caused it; a defect in an area
  fix that the closing review is the first to see is an ordinary finding. The
  escalation area for a closing round is `closing`.
- **At the end of the round**, set `head:` to the current HEAD. On resume, if
  HEAD has commits since `head:` that the current Rounds line does not list,
  someone committed outside the loop: set `consecutive_clean = 0`.

Two consecutive clean rounds, not one: counts oscillate, and an empty round is
often followed by one that finds real problems in a different slice. A round
with **no new self-inflicted findings** is a better convergence signal than a
low count.

### Stop when any of these is true

- **Everything in scope is done.** Diff mode: the diff target is done. Repo
  mode: every area is ticked and the closing review is done (or the loop
  committed nothing). The success condition: `status: done`.
- **A Codex-authored fix (§6a) is followed by another self-inflicted round in
  the same area.** Both models are churning the same ground. This does not
  end a repo sweep: tick the area as `design change at R<n>`, move that
  round's open findings to Needs owner marked `design change`, reset
  `self_inflicted_streak` to 0, and set `target:` as for a done area. In diff
  mode, and in the closing review, it ends the run: `stopped (design change)`.
- **Codex is out of usage** (§1): `status: paused`.
- **The reviewer changed the repo** (§1 snapshot mismatch).
- **A run failed**: §0's precondition check; REVIEW FAILED; a review with no
  findings block after its retry (§1); an escalation that moved HEAD or failed
  twice (§6a).
- **The budget is spent** (checked only here, after the round's bookkeeping):
  this invocation has run `--max-rounds` rounds (default 10).
  `status: paused (budget)`.

At every stop, set `status:` (`done`, `paused (...)`, or `stopped (<reason>)`)
before writing the §7 report.

## 6a. Escalation: hand self-inflicted findings to Codex

**Trigger: `self_inflicted_streak` reaches 2**: two consecutive rounds where
every new finding was self-inflicted by fixes made earlier in this loop. The
fixing model keeps re-introducing the same class of problem, so do not write
the next fix yourself. Let Codex, which keeps spotting it, attempt the fix:

```bash
cd "$(git rev-parse --show-toplevel)" && S=.planning/codex-loop
git rev-parse HEAD > $S/pre-fix-<n>.head
<env assignments from the state file> codex exec --sandbox workspace-write --approve-for-me \
  < $S/fix-prompt-<n>.md > $S/fix-<n>.log 2>&1
echo "codex exit: $?"
git rev-parse HEAD | cmp - $S/pre-fix-<n>.head
```

(`--full-auto` was removed in Codex 0.147.0; the workspace-write sandbox plus
automatically reviewed approvals is its replacement for an unattended fix run.
With no prompt argument, `codex exec` reads the prompt from stdin.)

- The state file's `env:` assignments go in front of `codex` (omit the prefix
  when it is `none`), since the Bash tool's shell does not keep exports
  between calls; without them its tests run against the wrong environment.
- The prompt must contain: the findings verbatim, the relevant file paths, the
  constraint to fix ONLY those findings, a regression test per finding, the
  project's test command, and "do not stage or commit anything, and do not
  edit gitignored files". Same output hygiene as §1.
- **If HEAD moved, stop and report.** Otherwise inspect everything it changed
  with `git status --porcelain -uall` and `git diff HEAD`.
- **The escalation failed** if it exits non-zero, changes nothing, or its
  changes fail §4 or your triage. Discard its changes (the tree was clean
  before it ran), retry once, otherwise stop and report. A failed run does not
  use up the area's one escalation.
- **You still own triage, verification and commits.** Run the §4 checklist and
  commit per §5, noting in each commit message that the fix was authored by
  Codex via escalation. The tree must be clean again before §1.
- Record the round as `fixed by Codex (escalation, area: <area>)` and reset
  the self-inflicted streak, then resume at §1. The area is what makes "once
  per area" survive compaction.
- This fires at most once per area (the closing review counts as one area). A
  second self-inflicted round in the same area after it is the §6
  design-change condition.

## 6b. Surviving compaction

This loop reliably outlives a single context window. Treat compaction as
routine and never end the loop early to avoid one.

- **Update the state file at the end of EVERY round**, before the next review.
  Losing "why I rejected finding X" is what lets a later round re-litigate it
  into a bad fix.
- **When context runs low, compact and continue.** Do not stop and do not ask.
  Then re-read this file and the state file (see the top of this file).
- Keep long output out of context: reviews and test runs go to files; read only
  the findings block or the summary line.
- Commit per finding. A committed fix survives any context loss; one sitting in
  the working tree does not.

## 7. Final report

One summary at the end, not per round, after `status:` is set:

- How it ended: `done`, `paused` with the reset time, or `stopped` and why.
- Mode and scope; in repo mode, every area with its rounds to done.
- Findings per round, and the trend.
- What was fixed, grouped by area, with commit SHAs, own finds marked.
- **Which findings were caused by fixes earlier in this loop.** This is the
  most useful signal about which areas are genuinely hard.
- Areas recorded as needing a design change, and areas closed on the round
  budget with what their last round fixed.
- What was rejected, and the evidence.
- What was flagged but deliberately not fixed, and why.
- **The Needs owner questions**, each with its finding, asked together.
- Findings still open at a stop, verbatim, with your triage of each.
- Final suite counts, and confirmation that nothing was pushed.
