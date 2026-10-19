---
description: "Run the weekly hub pass in one session: mine new lessons (transcripts, an optional course source, social sources), consolidate them, triage both changelogs, audit every tracked project area against one shared trace, rank top tips, then put every decision on one sheet and apply what the owner approves."
argument-hint: "[--skip <stage>[,<stage>...]] [--tips <n>]"
disable-model-invocation: true
---

# /weekly-update: the whole weekly pass, one decision sheet

The hub's weekly routine is eight commands run in a fixed order, and each one stops for its own
approval dialogs. Run by hand, the last pass ran across two days (2026-10-10 and 2026-10-11),
and a stage that gets forgotten leaves a gap the next run has to recover. This command runs every
stage in one session, holds every question back, and asks them all at once on one numbered sheet.
Then it applies what the owner approved, ledgers every outcome, commits, and asks before anything
is pushed. Each stage runs only when this checkout has what it needs (§0), so the same file works
in the private hub and in the public mirror.

**After any compaction, re-read this whole file (`.claude/commands/weekly-update.md`), the state
file, and the command file of the stage you are in.** Compaction keeps only the start of a long
command.

## What a finished run leaves behind

- Every transcript the scheduled job fetched, and every course video missing from disk where the
  hub has a course source, committed under `transcripts/` and ledgered in
  `lessons/.processed.json`.
- New lessons from transcripts and from the social sources, verified, indexed, and consolidated
  until a pass changes nothing.
- Both changelog ledgers advanced to the newest release, with every entry triaged.
- Every tracked area's `current.md` refreshed (design and non-codebase snapshots carried forward
  and labelled as such), its window reconciled from one shared trace saved as
  `projects/top-tips-trace-<date>.md`, and its audit-log row and `last_audit` updated.
- One decision sheet answered, with every outcome ledgered where its source command ledgers it.
  Nothing is applied without a yes, and nothing declined is offered again.
- `python3 scripts/validate-artifacts.py` passing, the publish dry run clean on the final HEAD
  where the hub has `scripts/publish.sh`, the hub committed, and the push question asked.
- A report with exact counts per stage.

Out of scope: `/claude-loop`, `/codex-loop` and other review loops; application code in an
audited project; pushing the hub or publishing the mirror without a yes to the final question;
any paid model eval (no stage calls one).

## Hard rules

- **Never ask mid-run.** Every question a stage command would put in a dialog goes on the sheet
  instead. The only stops before the sheet are the abort conditions at the end.
- **Dispatch subagents wherever a stage says to.** This is an explicit request to delegate, so a
  model told not to volunteer the Agent tool has the instruction it needs. Tracers, verifiers and
  refuters are fresh subagents, never forks, because a fork grades its own reasoning.
- **At most 5 subagents at once.** Where a stage command says to launch every batch in one
  message, launch waves of up to 5. Six or more parallel subagents can exhaust memory and kill
  the session mid-run.
- **Run each stage by reading its command file in full and following it**, with the arguments
  given here. Do not use the Skill tool for them: the two changelog commands set
  `disable-model-invocation`, and reading keeps one method for every stage. This file wins on
  when to ask, when to commit, how lessons are traced, and how many subagents run at once; the
  stage command wins on everything else.
- **Update the state file before and after every stage.** A stage that commits is done only when
  the state file names its SHA. A stage that feeds the sheet is done when its items are in the
  state file.
- Prose this run writes (lessons, ledgers, commit messages, `CHANGELOG.md`, the sheet) follows
  the repo rules: Conventional Commits, no attribution lines, no em dashes, and no private
  project name in `CHANGELOG.md`.

## 0. Preflight

- Hub root: `git rev-parse --show-toplevel`, which must hold `lessons/` and `.claude/commands/`.
  If it does not, stop and say so.
- State directory: `<hub>/.planning/weekly-update/`. If `git check-ignore -q` does not cover it,
  append `.planning/weekly-update/` to `"$(git rev-parse --git-path info/exclude)"` (local only, no
  repo change). If `STATE.md` exists with any status other than `done`, resume at its first
  unfinished stage. If its status is `done` and its date is within the last 6 days, stop: say this
  week's run finished on that date (a re-sent command or a timer can trigger this) and start fresh
  only if the owner says so. An older `done` file is renamed to `STATE-<its date>.md` and the run
  starts fresh.
- The working tree may hold only scheduled-job output under `transcripts/`. If anything else is
  uncommitted, stop and list it, so this run's commits contain only this run's work.
- If the hub has a course source (`transcripts/ray-amjad-agentic-coding-school/` exists, or
  `claude mcp list` names `agentic-coding-school`), prove the server is connected before anything
  runs: call `mcp__agentic-coding-school__list_classes` (load it through tool search first if it
  is deferred). If the tools are missing or the call fails, stop here and tell the owner to run
  `/mcp`, connect `agentic-coding-school`, and start `/weekly-update` again; a newly added server
  only loads in a new session. Go on without the course only if the owner says so. With no
  course source, record `course: none` and carry on.
- Record in the state file: the date, `claude --version`, `codex --version`, the course check's
  result (connected, skipped by the owner, or none), the `--skip` list, and `window_start`, the
  oldest `last_audit:` across every area's `improvements.md` (none when there are no areas).
- When the hub has `transcripts/`, check for transcripts no extraction has run over, and record the result. Compare the newest
  commit that added a transcript (`git log -1 --diff-filter=A --format='%h %ad %s' -- 'transcripts/*/*.txt'`)
  with the last extraction run (`git log -1 --format='%h %ad %s' -- lessons/.processed.json`),
  and count the committed (`git ls-files`) and uncommitted (`git ls-files --others
  --exclude-standard`) `transcripts/*/*.txt` files missing from `lessons/.processed.json`. The
  uncommitted ones are normally the scheduled job's week. A transcript committed after the last
  run, or committed and missing from the ledger, goes on the sheet as a note; the extract stage
  mines it either way, since its work list is every transcript not in the ledger.
- `--skip` takes stage names from the headings in §1. A skipped stage changes no ledger, and the
  report says what it leaves stale.

```markdown
---
status: running | sheet-open | applying | done
date: <YYYY-MM-DD>
window_start: <YYYY-MM-DD>
---
## Stages
- fetch: done, <counts>
- extract: done, <counts>, <sha>, <sha>
- social: running
## Sheet
- <n>: <source stage>, <target file>, <one-line summary>, answer: <y|n|l|none>
## Notes
<anything a resumed session needs: dead ends, a failed check and its output>
```

Each stage runs only when the checkout has what it needs. A missing prerequisite skips the stage,
with the reason in the state file and the report; it is never an abort. The public mirror ships
without `projects/`, `transcripts/` and `scripts/publish.sh`, and most installs have no course
source.

| Stage | Needs |
|---|---|
| fetch | `scripts/run_pipeline.py` and `transcripts/` |
| extract | at least one transcript under `transcripts/`; its course pull also needs a course source |
| social | `references/agentic-coding-voices.md` |
| consolidate | lessons written by this run |
| changelog-claude, changelog-codex | the hub check in each command's §0 to pass; `/changelog-codex` also needs `gh` and `codex` |
| trace, areas, top-tips | at least one area under `projects/` |
| publish dry run (§3) | `scripts/publish.sh` |

## 1. Stages, in order

The order is a requirement: lessons must exist before they are consolidated, be consolidated
before they are traced, and be traced once before any area or the top-tips ranking reads them.
The two changelog stages read no lessons, so a failed lessons stage does not stop them.

The extract and social stages research independent sources, so launch the social scouts while
the extract miners run, keeping both within the 5-subagent cap. Their writes share `lessons/`,
`INDEX.md` and the dedupe, so write them one stage at a time, extract first: the social stage then
dedupes against the lessons extraction just filed. When a social candidate makes the same claim as
a lesson filed earlier in this run, add its URL to that lesson's `sources` (and its `source_type`)
instead of skipping it, so the lesson keeps both the video and the more authoritative source.

### fetch

If the timestamp in `transcripts/.last_run` is more than 48 hours old, or the tail of
`transcripts/.pipeline.log` ends in `BLOCKED` or `Network not ready`, run
`scripts/run_pipeline.py --force` once under the hub's Python (`.venv-linux/bin/python` when that
venv exists, otherwise `uv run python`) and read the new tail.
Nothing is committed here; the course pull in the next stage joins the same commit.

### extract

Follow `.claude/commands/extract-lessons.md` with the argument `new`. Where the hub has a course
source, its §3.3 course reconciliation is the weekly course pull and is not optional. A tool
result too large to return arrives as `<persisted-output>` with a `Full output saved to:` path;
read the JSON from that path. After the pull, rebuild the transcript index with the fetch stage's
Python: `<python> -c "import sys; sys.path.insert(0,'scripts'); import fetch_transcripts as f; f.rebuild_index()"`.

Commit twice: the transcripts (`feat(transcripts): add <n> youtube and <m> course transcripts`,
naming only the sources that added any),
then the lessons with their `CHANGELOG.md` entry (`feat(lessons): add <n> lessons from <k>
transcripts`). The lessons commit carries `lessons/.processed.json`, so it moves the last
extraction run that the next run's preflight check compares against.

If the owner chose at preflight to go on without the course, put "course not reconciled" at the
top of the sheet. Never report the course as current without the diff.

### social

Follow `.claude/commands/extract-social-lessons.md` with the argument `new` and a window that
starts on the date of the newest entry under `## Last social run` in `lessons/INDEX.md`. Commit
with its `CHANGELOG.md` entry.

### consolidate

Follow `.claude/commands/consolidate-lessons.md`, scoped to the lessons this run's two lessons
stages created, checked against each other and against the full active corpus. If a pass changes
anything, re-run it on the changed lessons, up to 3 passes, until one reports 0 merged, 0 split
and 0 pruned. Commit (`refactor(lessons): consolidate the <date> batch`).

### changelog-claude, changelog-codex

Follow `.claude/commands/changelog-claude.md`, then `.claude/commands/changelog-codex.md`, each
through its §3 triage, keeping candidates in its ledger's `## Pending` block as it says. Stop
before its §4 walk. Every Config, Retire and Habit item becomes a sheet item, and an update
proposal (`claude update`, `codex update`, `codex app-server daemon update`) goes first. Risk
items, and any mirrored config file found replaced by a plain copy (with its diff), go on the
sheet as notes.

### trace

One trace serves every area and the top-tips ranking, so each lesson is judged once rather than
once per area. Its scope is every active lesson created after `window_start`, since each
area's last pass already reconciled the lessons created on its `last_audit` day (`/optimise` §4
starts a window the day after).

- Split the scope into batches of about 45, one fresh read-only subagent each, on the cheap or
  fast tier. Each tracer checks its lessons against the corpus `/top-tips` §2 names (`projects/`,
  the global `CLAUDE.md`, `.claude/commands/`) plus each codebase area's real config path from its
  `current.md`, matching by slug and by distinctive phrase. It returns one row per lesson:
  `| # | Slug | Verdict | Fit (areas -> destination) | Evidence |`. The verdict is one of
  ADOPTED, QUEUED, ALREADY DECLINED, NOT-ELIGIBLE, NICHE, LOUD, CONVENIENCE, STALE or SURVIVOR,
  and every verdict except SURVIVOR carries file:line evidence.
- One more fresh subagent tries to refute every SURVIVOR against the tracking files and any
  `decisions.md`. A survivor it kills is reclassified with the evidence that killed it.
- Save the tracer tables and the refutation unedited to `projects/top-tips-trace-<date>.md`, with
  the verdict counts at the top.

Done when every lesson in scope has exactly one verdict, so the verdict count equals the scope
count.

### areas

An area is each `projects/<slug>/` folder, and inside a multi-tool one each tool subfolder
(`claude-code/`, `claude-design/`, `codex/`). Root files (`README.md`, `audit-log.md`,
`habits.md`, ledgers, traces, sheets) are not areas. For each area, follow
`.claude/commands/optimise.md` §0 to §4 with these changes:

- §3a inventories run as Explore subagents, in waves of up to 3 areas.
- §3b and the non-codebase case in §3a: do not ask. Carry the snapshot forward and say so in the
  audit-log note. For a design area whose window holds `claude-design` lessons, also put a
  snapshot refresh question on the sheet.
- §4: reconcile from the trace, not from new miners. The trace verdicts are the tally, and the
  surviving lessons whose Fit names this area are the keepers; refutation already ran.
- Flush the keepers to `AREA_DIR/optimise.md` as §4 step 6 says, each with its exact change worked
  out (§6b forbids asking about a diff nobody has written), then stop. Each keeper becomes a
  sheet item.

Several areas mined from one batch propose the same change: on 2026-09-12 about a quarter of all
keepers were duplicates of this kind. Merge keepers that land in the same destination file with
the same change into one sheet item that names every area it came from.

### top-tips

Follow `.claude/commands/top-tips.md` §1 and §3; the trace stage has already done its §2. The
candidates are the surviving lessons whose Fit names no single area (a general habit or the global
config), plus ledger LATER entries older than 30 days. Rank them and put the top `--tips`
(default 3) on the sheet, each with the exact entry text it would become.

## 2. The sheet

Write the full sheet to `.planning/weekly-update/SHEET.md`, set `status: sheet-open`, send it as
one plain message (not the question picker, which holds four questions), and stop until the owner
answers.

- Notes come first and need no answer: risks, skipped stages, the course not reconciled, a broken
  mirror link, committed transcripts the preflight found unextracted.
- Then the items, numbered continuously and grouped by source: updates, each changelog, areas,
  top tips, habits. Each item says what it is in plain words, why it fits this setup, the exact
  change (file and lines, or a pointer to the numbered block in `SHEET.md` when the diff is long),
  its source, and your recommendation.
- Close with the answer format: `1 y`, `2 n <reason>`, `3 l`, one per line or comma separated;
  `rec` takes your recommendation on every item not otherwise answered.

Each answer maps onto the source command's own outcome:

| Answer | changelog | areas (`/optimise`) | top-tips |
|---|---|---|---|
| `y` | APPLIED | Apply now, or Add to habits | ADOPTED |
| `n` | DECLINED (final) | Drop, with an Out of scope note | DECLINED (final) |
| `l` | LATER (30 days) | Skip for now, into the `improvements.md` backlog | LATER (30 days) |

An unanswered item stays wherever its command keeps pending work (`## Pending`, `optimise.md`) and
is listed in the report. It is never applied.

## 3. Apply, ledger, commit

Set `status: applying`. Apply the `y` items one at a time with Read and Edit, each validated as
its source command validates it (JSON and TOML parse, `claude plugin validate` on any touched
command, skill or agent, `claude doctor` or `codex doctor` after a settings change). A failed check
reverts that item and records it as FAILED with the output.

Then finish each stage command's own ledger steps. The changelog §5: watermark advanced,
`## Pending` cleared, and the config repo committed and pushed, which is that command's standing
rule. `/optimise` §6 and §7 for every area: audit-log row, `last_audit`, `optimise.md` deleted
when empty. `/top-tips` §5. Commit all area tracking and the top-tips ledger together
(`docs(projects): record the <date> optimise and top-tips passes`). A change to a shipped artifact
gets its `CHANGELOG.md` entry in the same commit.

Then, in this order, because the publish dry run reads committed HEAD:

1. `python3 scripts/validate-artifacts.py`
2. Commit anything still uncommitted.
3. `bash scripts/publish.sh` (dry run), where the hub has it. Fix and commit any leak before
   anything else.
4. Ask one question: push the hub's `main` to `origin`, and, where the hub has
   `scripts/publish.sh`, publish the mirror with `bash scripts/publish.sh --push`? Push only on a
   yes.

Set `status: done`.

## 4. Report

Lead with the outcome. Then one line per stage with exact counts: transcripts fetched and pulled;
lessons written, verified and dropped; consolidation passes with merged, split and pruned counts;
releases triaged per changelog; lessons traced and the count per verdict; keepers per area; tips
offered; sheet answers as y, n, l and unanswered; items applied and failed. Name every skipped
stage and what it leaves stale. Owner follow-ups (a `git pull` on the other machine, a sync step an
area's notes name, a declined `claude update`) go after the counts, one command per single-line
code block.

## Abort conditions

Write the reason into the state file, then stop and report, when:

- the course server fails the §0 check and the owner has not said to go on without it;
- the working tree holds changes this run did not make;
- `validate-artifacts.py` fails for a cause outside the stage that just ran;
- the leak gate fails on something this run did not write;
- a stage's command file is missing, or its own stop condition fires for a reason other than a
  prerequisite the §0 table lists.

Running `/weekly-update` again resumes from the state file.

## Self-check

- [ ] Every stage in the state file is done (with its SHA where it commits), skipped with a reason, or failed with its output.
- [ ] No question was asked before the sheet, except at an abort.
- [ ] The trace's verdict count equals its scope count, and every area's tally comes from it.
- [ ] Every sheet answer is ledgered in its source command's ledger, and nothing unanswered was applied.
- [ ] Every area's audit-log row matches its `last_audit`.
- [ ] `validate-artifacts.py` passed, the publish dry run ran on the final HEAD (where the hub has one), and nothing was pushed without the final yes.
- [ ] The report gives numbers, not adjectives.
