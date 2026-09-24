---
description: Audit a tracked project's Claude Code, Claude Design, or Codex setup, fold in new lessons, then apply open improvements one at a time with approval. Takes a project name from projects/.
argument-hint: <project-slug> [--design|--codex]
---

# /optimise: audit a project's Claude setup and apply improvements

You are auditing ONE registered project's Claude tooling setup against the repo's
`lessons/` library, then walking the owner through concrete improvements interactively and
applying the ones they approve. This is **not** a code review of the project's application
code, every finding is about *how the owner works with Claude on this project* (config,
agents, skills, hooks, prompting/keyboard habits), never about whether the app itself is
buggy.

This command runs from inside the **claudex-setup** repo (the hub). The project being audited
usually lives elsewhere on disk (its real path is in the registry frontmatter). You edit two
places: the audited project's actual `.claude/` (applying approved config changes), and the
claudex-setup repo's `projects/` tracking files (recording what you found and did).

Tune your behaviour to run reliably and unattended-friendly: follow the numbered steps in
order, use the exact file paths and formats below, stop where the stop conditions say to stop,
and run the final self-check before reporting done.

---

## 0. Inputs and mode resolution

1. Read the argument string. The first bare token is the **project slug** (e.g. `your-project`,
   `claudex-setup`, `another-project`, `personal-notes`). If no slug is given, list the
   registered projects (the subdirectories of `projects/`, excluding the root-level registry
   files `README.md`, `audit-log.md`, and `habits.md`) and ask the owner which one to audit,
   then stop until they answer.
2. Detect a tool flag anywhere in the argument string: `--design` selects the **Claude Design
   sub-area**, `--codex` selects the **Codex sub-area**, and `--code` (or no flag) selects the
   default **Claude Code area**. Set `MODE = design`, `MODE = codex`, or `MODE = code`
   accordingly. If the project is multi-tool and no flag was given, tell the owner the project
   has sub-areas and which flags reach the others (`--design`, `--codex`), the default must be
   a visible choice, not a silent one, then proceed with `claude-code/`. `--design` or
   `--codex` on a flat (single-tool) project is an error: only a multi-tool project has those
   sub-areas.
3. Establish the repo root. This command lives in the claudex-setup repo; the registry is at
   `<repo-root>/projects/`. Use `<repo-root>` as the base for every `projects/...` path below.

### Resolve the sub-area directory (`AREA_DIR`)

A registered project is a folder under `projects/<slug>/`. It is laid out one of two ways:

- **Flat (single-tool):** the tracking files live directly in `projects/<slug>/`
  (`current.md`, `improvements.md`, `applied-improvements.md`, `habits.md`). Only the Claude
  Code area exists.
- **Multi-tool:** `projects/<slug>/` holds per-tool subfolders: `claude-code/` and
  `claude-design/`, each with its own tracking files.

Resolve `AREA_DIR` like this:

- If `MODE = code`:
  - If `projects/<slug>/claude-code/` exists, `AREA_DIR = projects/<slug>/claude-code/`.
  - Else `AREA_DIR = projects/<slug>/` (flat layout).
- If `MODE = design`:
  - `AREA_DIR = projects/<slug>/claude-design/`.
  - If that folder does not exist, tell the owner the project has no Claude Design sub-area
    and ask whether to scaffold one (create `projects/<slug>/claude-design/` with a starter
    `current.md` and `improvements.md`, and migrate any existing flat files into a
    `claude-code/` subfolder so the project becomes multi-tool). Do not silently create it;
    stop for confirmation.
- If `MODE = codex`:
  - `AREA_DIR = projects/<slug>/codex/`.
  - If that folder does not exist, tell the owner the project has no Codex sub-area and ask
    whether to scaffold one (create `projects/<slug>/codex/` with a starter `current.md`,
    `improvements.md`, `applied-improvements.md`, and `habits.md`, and migrate any existing
    flat files into a `claude-code/` subfolder so the project becomes multi-tool). Do not
    silently create it; stop for confirmation.

Set `AREA_KEY`, the audit-log row key:
- Flat layout: `AREA_KEY = <slug>`.
- Multi-tool: `AREA_KEY = <slug>/<tool>` where `<tool>` is `claude-code`, `claude-design`, or
  `codex`.

If `projects/<slug>/` does not exist at all, the project is not registered. Tell the owner and
ask whether to register it (you would create the folder and a starter `improvements.md` with
frontmatter, see §8 for field definitions, and, for a live codebase, a first `current.md`
snapshot). Stop for confirmation before creating anything.

> **Self-referential note.** The claudex-setup repo is itself a registered project
> (`projects/claudex-setup/`). Auditing it means auditing *how the owner works with Claude when
> developing claudex-setup* (authoring commands/skills, the lessons pipeline, the
> publish/sanitize safety), not cataloguing the artifacts claudex-setup ships to others. Treat
> it like any other project; the flow is identical.

---

## 1. Force-create / load the central audit log

The file `projects/audit-log.md` is the **single source of truth for when each project
sub-area was last optimised**. You maintain it on every run.

1. If `projects/audit-log.md` does not exist, create it now with this exact skeleton (this is
   the "force-create on first use" behaviour, do it even before you have new data):

   ```markdown
   # Projects audit log

   Single source of truth for **when each tracked project was last optimised**. Auto-maintained
   by `/optimise`: the command force-creates this file on first use, and rewrites the audited
   project's row at the end of every run (from that project's `improvements.md` frontmatter +
   `current.md` snapshot date). Do not hand-edit dates here unless you are also fixing the
   project's frontmatter, they are meant to stay in sync.

   `last_audit = never` means no lessons-reconciliation pass has run yet (the project may still
   have a `current.md` snapshot and a starter backlog from registration).

   Multi-tool projects get **one row per tool sub-area**, keyed `<slug>/<tool>` (e.g.
   `your-project/claude-code`, `your-project/claude-design`), since `/optimise` audits each
   independently.

   | Project | Status | Last audited | Snapshot | Notes |
   |---------|--------|--------------|----------|-------|
   ```

   Then populate one row per already-registered sub-area from the existing project files
   (read each project's `improvements.md` frontmatter for `status` and `last_audit`, and each
   `current.md` for the `snapshot:` date).

2. If the file exists but the audited `AREA_KEY` has no row (e.g. a newly registered area),
   add one now.
3. Read the existing table into memory. You will rewrite exactly one row (the audited
   `AREA_KEY`) at the end of the run in §7, leaving every other row untouched.

---

## 2. Load the sub-area's existing tracking files

Read whichever of these exist in `AREA_DIR`, so you do not re-investigate from scratch and do
not re-suggest done or already-tracked items:

- `current.md`, the factual snapshot of what is already wired (the ground truth).
- `improvements.md`, the open backlog (recommendations not yet applied) + frontmatter.
- `applied-improvements.md`, the ledger of what is already done (skip re-suggesting these).
- `decisions.md`, if present: the frozen record of settled decisions, including things
  deliberately declined and why. A candidate that matches a record here is not a keeper; it is
  already answered. Records are frozen, so a decision that has genuinely changed gets a NEW
  record marked as superseding, never an edit to the old body.
- `habits.md`, the prioritised list of things **the owner must do** rather than things you can
  apply, scoped to *this* area. **Any area may have one**, including Claude Design. Read it if
  present; never read its absence as proof the area cannot have one (see §5).

Also read one file from outside `AREA_DIR`:

- `projects/habits.md`: the **cross-area** habits registry, holding owner actions that hold in
  any repo, for all three tools. Read it on every run, whichever area you are auditing, for two
  reasons. It is context the owner already accepted, and it is the dedup list that stops this
  run re-proposing a general habit that is already recorded (§5).
- `optimise.md`, the **run scratchpad**: this run's freshly-reconciled keepers, written before
  the walkthrough so a mid-run stop cannot lose them (see §4). It is gitignored and deleted on
  clean completion, so a file being present here means **a prior run was interrupted
  mid-walkthrough**.

**Resume an interrupted run.** If `optimise.md` exists and still lists un-walked items, do not
discard them: carry those pending suggestions into this run's walkthrough (§6), deduped against
the fresh reconciliation in §4 so nothing is offered twice. This is the whole point of the
scratchpad, the previous run's mined suggestions resume instead of being re-derived from
`lessons/` from scratch.

Read the area's **"Notes for audits"** section (in `improvements.md`) and obey its quirks
throughout the run (e.g. your-project: em dashes banned in anything generated *for* the project;
its `.claude/` is gitignored and syncs via a separate config repo, not the project's git).

Also read `projects/README.md` once for the registry conventions if anything is ambiguous.

---

## 3. Refresh the snapshot (`current.md`)

The refresh method differs by mode.

### 3a. MODE = code or codex: inventory the real config tree

For `MODE = codex`, inventory the project's **Codex** config surface instead of `.claude/` , 
`AGENTS.md`, any project `.codex/` directory, and the relevant `~/.codex/config.toml`, the
same diff-against-previous-snapshot way; everything else in this subsection applies unchanged.

1. Find the project's real location: the `path:` in `improvements.md` frontmatter and/or the
   `actual_path:` in `current.md`. If the two disagree, trust `current.md`'s `actual_path:`
   (the `improvements.md` `path:` is known to go stale) and note the discrepancy. Verify the
   resolved path exists before proceeding, if not, stop and report.
2. Spawn an **Explore subagent** to inventory the project's `.claude/` directory and root
   config, so the noisy file-reading stays out of your main context. Give it a specific
   purpose: "produce a factual inventory of this project's Claude Code setup, settings.json,
   settings.local.json, agents (models/tools/isolation), commands, hooks (matchers + targets,
   and hook files vs hooks actually wired in settings), skills, references, scripts, plugins,
   MCP servers, and any GSD/`.planning` state, so an audit can diff against it." Pass it the
   previous `current.md` snapshot so it reports **diffs**, not a full dump. Have it report
   counts and specifics, not opinions.
3. Diff the inventory against the existing `current.md`. Update `current.md`:
   - Rewrite the inventory sections to match observed reality.
   - Bump the `snapshot:` frontmatter date to today, with a short note of what changed (or
     "NO drift vs <prev date>" if nothing did). Preserve the running history of prior snapshot
     notes, append, do not erase them.
   - Update the "Drift vs improvements.md" table if any recommendation is now stale (e.g. a
     rec that has since shipped).
4. If a non-codebase area (a `path: null` environment/workflow entry like `another-project` or
   `personal-notes`) has no `.claude/` to inventory, skip the Explore step and refresh
   `current.md` (if it exists) conversationally, the same way as design mode below.

### 3b. MODE = design: refresh conversationally

Claude Design has no `.claude/` config tree to inventory, so **do not run an Explore
inventory**. Instead refresh `current.md` by asking/observing:

1. Ask the owner (or read from pasted screenshots/session notes) the current design usage:
   which surface (hosted Claude Design vs Open Design/local), the project/pages, which panels
   or tweaks are in active use, the export→code handoff, and whether generations are anchored
   to the project's design tokens.
2. Update the hand-maintained `current.md` snapshot and bump `snapshot:` to today. Update its
   drift table against `improvements.md`.
3. The design area **can** have a `habits.md`, and the split that works is: `habits.md` = what
   the owner does *during* a session (model picker, prompt discipline, where to trigger a
   hand-off); `improvements.md` = what gets set up *before* one (attached files, design systems,
   reference artifacts). Because the design surface is entirely owner-driven, expect more
   findings to route to habits here than in a CLI area, not fewer.

### 3c. Both modes: sweep the backlog against the fresh snapshot

Anything in `improvements.md` the fresh snapshot shows is **already done** → move it to
`applied-improvements.md` now, with today's date and a one-line note, so it is not walked in
§6.

---

## 4. Reconcile new lessons into the backlog

Now decide which `lessons/` apply to THIS project that are not already in place or already
applied.

> **Design-area caveat.** The `lessons/` corpus is Claude-Code-focused, so it is **not** the
> source for a `--design` run. Draw design recommendations from design-relevant material
> instead (Claude Design product updates landing in `transcripts/`, the project's
> design-system needs, gaps vs the shipped visual language). If there is no design-lessons
> source yet, say so and skip reconciliation, keep the refreshed snapshot and walk whatever
> is already in the design backlog. Still bump `last_audit:`. This caveat is **design-only** , 
> a `--codex` run reconciles from `lessons/` normally (the corpus includes Codex-relevant
> lessons); scope it to lessons that apply to the Codex CLI.

1. Determine what is new since the last pass. The `last_audit` frontmatter date in
   `improvements.md` marks the previous reconciliation. The window is every lesson created
   after that date, not only the batch that prompted this run: count candidates by `created:`
   date for every date after `last_audit`, reconcile all of them, and write the window and its
   count into the new `last_audit` note ("window <from> to <to>, <N> lessons"). Only a pass
   that reconciled lessons moves `last_audit`; a resume-only walkthrough leaves it alone.
   Superseded lessons are already excluded from INDEX. On a first pass (`last_audit: null`),
   consider the whole relevant library.
2. **Scope by TOOL first, then by `focus:` category.** These are two independent axes in
   `lessons/`, and conflating them is what made the design area report a phantom zero for
   months (see the warning below):
   - **Tool** lives in each lesson's `tool:` frontmatter (`claude-code` / `claude-design` /
     `codex`; may be a list; **absent means `claude-code`**). Filter to the audited area's
     tool: a `--design` run takes every lesson whose `tool:` includes `claude-design`
    , **wherever it sits in the tree**, plus cross-tool lessons that list it. There is no
     `design/` or `codex/` folder by design; never look for one.
   - **Category** is the topical folder, and is what `focus:` lists (`agents`, `skills`,
     `hooks`, `automation`, `workflows`, `prompting`, `context-management`, `permissions`,
     `model-selection`, `configuration`, `mcp`, …). Use it to narrow *within* the tool.

   `lessons/INDEX.md` is grouped by tool (`## Claude Design` / `## Codex` / `## Cross-tool` /
   `## Claude Code`), so read it first, the tool section IS the candidate list, even though
   the links point into topical folders. Then open candidate lesson files. For a large batch,
   spawn parallel Explore miners and dedup their results against the existing backlog +
   applied ledger; keep the judgement (fit-to-this-project) in your main context. Run the
   miners on the cheap or fast tier and keep the judgement in the main session at its own
   tier, and say in the report which tier the miners ran on. Named by role rather than by
   model id, since this command ships to consumers with different ladders.

   > **A zero here is a claim that needs evidence.** If a tool's reconciliation comes back
   > empty, do NOT record "no relevant lessons exist", verify the corpus was ever mined for
   > that tool. `/extract-lessons` was Claude-Code-only until 2026-07-17, so any lesson
   > written before then has no `tool:` field and defaults to `claude-code`, and any
   > transcript ledgered before then had its design/Codex content ignored. A
   > `.processed.json` entry is **not** evidence a transcript was mined for this tool. Report
   > an empty result as "the corpus has not been mined for X", not as a fact about the
   > material.
   > **Refute before you flush.** A keeper needs evidence too, not just a zero. For each
   > keeper, actively try to kill it: search `current.md`, `applied-improvements.md`, this
   > area's `habits.md`, `projects/habits.md` and the run scratchpad's declined and parked
   > items for the same change, then test its "why it fits this project" sentence by deleting
   > the project hook and seeing whether the claim still stands. A keeper that survives goes
   > to section 6; one that does not is reclassified with the evidence that killed it, in the
   > tally. On a large batch, give the refutation to a different subagent from the one that
   > raised the keepers, since the raiser grades its own reasoning leniently. Every keeper
   > costs the owner an approval dialog, so a weak one is a slot a real one does not get.

3. Classify every candidate lesson into exactly one bucket:
   - **Keeper**: genuinely fits this project and is not already in place or applied. These
     become proposed improvements (or habits, see §5). Cite the lesson path and say *why it
     fits this project*.
   - **Already covered**: the setup already does this (per `current.md`) or it is already in
     `applied-improvements.md`. Skip.
   - **Out of scope / owner-decision**: does not apply, or the owner has already decided
     against it (e.g. an all-Opus decision means "route read-only agents to Haiku" is a
     standing NO). Skip; do not re-litigate settled decisions.
   - **General habit:** a real, specific technique the owner would use in *any* repo, with no
     project-specific hook. **Do not skip it.** This bucket read "too generic · Skip" until
     2026-08-22, which threw good advice away for the sole reason that it was broadly true,
     the single largest leak in the transcript → lesson → project pipeline. Route it to the
     cross-area `projects/habits.md` instead (§5). Reject a candidate outright only when it is
     *vague* ("use Claude well", "write good prompts"), not merely *general*: a concrete action
     that happens to apply everywhere is a keeper, not a reject. **General says where it
     applies, not who performs it.** If the model could carry the action itself given a standing
     rule, a command or a hook ("do not fold adjacent improvements into the task", "quote code in
     docs from executed commands", "shape a Codex prompt as phases plus a not-building list"), it
     is a **config keeper** even though it is general, and §5 routes it to the owner's global
     config rather than to any habits file. A habits file is only for what needs a human hand.
4. Fix any existing recommendation that cites a lesson now marked superseded (point it at the
   successor).
5. For each keeper, decide **config vs habit** (see §5).

Report a one-line tally of the buckets (e.g. "14 new lessons: 3 keepers, 5 already-covered,
4 out-of-scope, 2 general habits") so the owner sees the funnel before the walkthrough.

6. **Flush this run's keepers to the run scratchpad before walking them.** Write every keeper , 
   config and habit alike, each with its full outline (what · why it fits *this* project · the
   exact change or habit text · source `lessons/<category>/<id>.md`), into `AREA_DIR/optimise.md`
   **now**, before the §6 walkthrough starts. This is the durable holding pen for freshly-mined
   suggestions: if the owner stops the run (or it is interrupted) before an item is walked, it
   survives here instead of evaporating from context, and §2 of the next run resumes it. Include
   any items you carried in from a prior interrupted run (§2). Pre-existing `improvements.md`
   backlog items do **not** need copying in, they are already durable; `optimise.md` only
   protects this run's new keepers. As each item is resolved in §5/§6, strike it from
   `optimise.md`; when the walkthrough finishes with nothing left, delete the file.

---

## 5. Config change vs keyboard habit: the routing rule

**First test, before anything else: who performs the action?** Ask whether the model could do
it unprompted given a standing rule, a slash command or a hook, or whether only the owner can
(clicking through an app, reading `/usage`, choosing a preference, phrasing their own prompt,
watching a recording). Agent-performable findings are **config changes**, even when they hold in
every repo; a habits file is for what genuinely needs a human hand. Until 2026-08-23 a number of
agent-side behaviours were filed as habits purely because they were general (scope-creep
discipline, quoting code from executed commands, how to shape a Codex prompt), which left the
owner remembering rules the harness could have carried. Being general decides *where* a config
change lands, not *whether* it is one.

Every keeper has one of **three** destinations. Route it correctly:

- **Config change (Claude can apply it):** anything that edits a file, such as a
  `settings.json` key, an agent/command/hook/skill file, a `CLAUDE.md` rule, or a reference
  doc. These go through the apply flow in §6 and, once applied, into `applied-improvements.md`.
  - **General config** (agent-performable, holds in any repo) lands in the owner's **global**
    setup rather than in the audited project, and the destination follows the shape of the
    finding. An always-on behaviour rule goes into the global `~/.claude/CLAUDE.md` (the
    `dotclaude` repo: edit, commit, push, then fast-forward the other mirror's checkout so both
    machines carry it). An on-demand capability goes into a user-scope slash command, authored in
    this repo's `.claude/commands/` and symlinked into `~/.claude/commands/` on WSL and copied on
    Windows (the `codex-loop` precedent), so it costs nothing until invoked. A deterministic check
    goes into a hook (user settings are per-OS, so both mirrors). A general *setting* (an
    `outputStyle`, a `defaultMode`) is a config change offered as an owner choice, not a habit.
    **Prefer commands and hooks over new CLAUDE.md lines:** the global file loads into every
    session on every turn, and the prompt-audit lesson warns that defensive rules a strong model
    already follows degrade it rather than help. Still record the applied item in the audited
    area's `applied-improvements.md` (it is where the finding surfaced), with the global path
    named as *where it landed*.
- **Project habit (the OWNER must do it, *here*):** a command to type, a discipline to keep, a
  workflow the owner drives, whose payoff depends on a concrete trait of *this* area (a
  gitignored `.claude/` that syncs by allowlist, a paywall matrix, a 3-file CLAUDE.md
  hierarchy). Not enforceable via config, so it goes into `AREA_DIR/habits.md`.
- **General habit (the OWNER must do it, *anywhere*):** the same kind of owner action, but the
  reasoning holds in any repo: a product behaviour, a CLI flag, an account-level fact, a
  prompting move. These go into the cross-area **`projects/habits.md`**, not into any area file.

When choosing the enforcement strength of a config keeper, escalate one tier per observed
violation (convention -> CLAUDE.md line -> hook/mechanical check) rather than jumping to a hook
for a failure that has never occurred; keep the mechanically-enforced surface small.

**The test that separates the last two:** draft the "why it fits this project" sentence. If it
is load-bearing (remove it and the habit stops being worth doing here), it is a project habit.
If it is filler you had to invent so the entry could qualify, it is a general habit, so file it
at `projects/habits.md` and drop the invented hook.

> **Why this destination exists.** Before 2026-08-22 an area `habits.md` was the only home for
> owner actions, so a genuinely general habit survived only by dressing itself as
> project-specific, and anything that could not be dressed up was binned by §4's old
> "too generic · skip" rule. The observable result: `your-project/claude-code/habits.md` held ~30
> entries, most of them general technique with a bolted-on hook, while
> `claudex-setup/claude-code/habits.md` held 4. Not because the second area has fewer
> applicable habits, but because the first was audited earlier and absorbed them. A general
> habit is now recorded once, in one place, and every area inherits it.

Rules for habits:
- Route **project** habit findings to `AREA_DIR/habits.md` and **general** habit findings to
  `projects/habits.md` (repo root registry, one file for all areas and all three tools).
- **Every area type can have an `AREA_DIR/habits.md`**, Claude Design included. If the area has
  none yet, ask before creating one, then create it; absence means "none has emerged yet", not
  "this area is not allowed one". _(Precedent: the design area was specified as habit-free on
  the reasoning that keyboard habits are a CLI concept. That was backwards, because a hosted
  design surface has no config at all, so **everything** there is owner-driven. Its `habits.md`
  was created 2026-07-26 on request.)_
- `projects/habits.md` always exists; never scaffold a second copy inside an area folder.
  Tag any entry that is not Claude Code with a leading `(Codex)` or `(Claude Design)` marker,
  since one file serves all three tools.
- **Do not re-propose a general habit that is already in `projects/habits.md`** (read in §2).
  Without this check every area audit re-offers the same cross-cutting habits forever.
- **Promotion, offered opportunistically:** if while reading `AREA_DIR/habits.md` you hit an
  existing entry whose project hook is filler by the test above, offer to promote it, using
  AskUserQuestion with **Promote to general** / **Leave here** / **Stop**. On *Promote*, move
  the entry into `projects/habits.md` (stripping the invented hook), delete it from the area
  file, and bump both `updated:` dates. Offer at most 3 promotions per run so this never
  displaces the actual walkthrough, and never promote an entry whose hook is load-bearing.
- Both files use the same `## High` / `## Medium` / `## Low` headings. Order an area file by
  payoff *for that project*; order `projects/habits.md` by payoff across all your work.
- Each habit entry: a bold one-line title, a couple of sentences explaining the habit and why
  it is worth doing (for an area file, why it fits *this* project specifically; for the general
  file, the mechanism and when it bites), and a trailing citation to the source
  `lessons/<category>/<id>.md` (multiple allowed).
- Bump the destination file's `updated:` frontmatter to today when you add or change entries.
- Habit findings still get a dialog, the owner decides what enters their habit list. Use
  AskUserQuestion with options **Add to habits** / **Skip** / **Drop** / **Stop**, and name the
  destination file in the option description so the choice is visible: on *Add*, write it into
  the resolved habits file under the right priority heading, then strike it from `optimise.md`
  (and remove it from `improvements.md` if it was ever mis-filed there); on *Skip*, leave it in
  `optimise.md` so it resumes next run; on *Drop*, strike it from `optimise.md` and note the
  removal in the report; on *Stop*, end the walkthrough (the remaining items stay in
  `optimise.md`). Never run a habit through the config apply flow in §6, you cannot "apply"
  a keyboard habit.

---

## 6. Walk the config keepers one at a time (interactive apply)

Present the config keepers **one improvement at a time**, in priority order (high-impact →
medium → low → hygiene). Merge pre-existing backlog items from `improvements.md` and this
run's newly reconciled keepers into ONE priority-ordered walkthrough, not two separate
passes. For each one:

### 6a. Print a full item outline in chat first

Before the dialog, write a short self-contained outline the owner can read without prior
context:
- **What** the pattern is, explained from scratch in plain language (assume the reader has
  never heard of it, no jargon, no undefined lesson names).
- **Why it fits this project specifically** (cite the concrete trait: the LaTeX pipeline, the
  paywall, the 3-file CLAUDE.md hierarchy, the private-repo-with-PII fact, etc.).
- **The exact change** you would make: which file, and the concrete before/after or the lines
  added.
- The source `lessons/<category>/<id>.md`.

### 6b. Ask with a self-contained AskUserQuestion dialog

Use the `AskUserQuestion` tool. The dialog must stand entirely on its own, the chat prose is
supplementary and must never be *required* to understand the choice:

- **question text:** the from-scratch explanation of the pattern (what it is and why it fits
  this project), written so someone who has not read the chat can decide. No jargon.
- **options:** **Apply now** / **Skip for now** (stays in backlog) / **Drop** (remove: no
  longer wanted) / **Stop here** (end the loop, keep the rest).
  - The **Apply now** option's **`preview` field** carries the concrete change: the exact
    lines/diff/settings block that would be written, with the target file path as a heading.
    This is the load-bearing preview, use the `preview` field, not the description.
  - Option `description`s state plainly what happens on selection (e.g. "Writes the lines
    shown in the preview to <file>").
- Keep one question per improvement (single-select).
- Items flagged "verify from a project session" or blocked on missing info (e.g. an upstream
  URL): present them, but only to ask keep/drop, don't attempt to apply them.

Never present an improvement whose diff you have not worked out, the owner is approving the
preview, so the preview must be exact. If the change involves a settings key or value you
have not seen used in this config before, verify the exact key name and value type (against
the settings JSON schema referenced at the top of settings.json, or the docs) before
presenting the dialog, never guess a literal in a preview.

### 6c. Apply the approved change

For each **Apply** answer:
1. Make the edit in the project's real `.claude/` (or the relevant file) at its actual path.
2. If the changed file is JSON (`settings.json` etc.), re-validate that it still parses after
   the edit.
3. If the project has repo-specific content rules (e.g. your-project bans em dashes in anything
   generated *for* the project), respect them in whatever you write into that project.
4. Record the item in `AREA_DIR/applied-improvements.md`: newest first, under a `## <today's
   date>` heading, with **what** changed, **why**, **where it landed** (file path), any
   **follow-up**, and the source lesson. Then remove it from its holding place, strike it from
   `optimise.md` (fresh keepers live there), and remove it from `improvements.md` if it was a
   pre-existing backlog item. This ledger entry is what stops it being re-suggested next run.
5. If the project notes a cross-machine sync mechanism (e.g. a separate config repo whose
   `sync.sh push` propagates the gitignored `.claude/`), add the sync reminder to the ledger
   entry, do not perform any push/commit yourself unless explicitly asked.

For **Skip for now**, keep the item as an open recommendation: if it is a fresh keeper (only in
`optimise.md`), write it into `improvements.md`'s open backlog now, that is its durable home , 
then strike it from `optimise.md`; a pre-existing backlog item just stays in `improvements.md`.
For **Drop**, record the decision (a one-line "not pursued: <reason>" note in `improvements.md`'s
"Out of scope" section) and strike it from both `optimise.md` and the open backlog so it isn't
re-raised. For **Stop here**, end the walkthrough and keep the remaining items untouched, they
stay in `optimise.md`, so the next run resumes them (§2).

**When the walkthrough finishes with every item dispositioned** (each one applied, added to
habits, written to the `improvements.md` backlog, or dropped), `optimise.md` has nothing left , 
**delete it**. A non-empty `optimise.md` after the run means items are deliberately carried
forward (owner stopped, or skipped a habit with no other home); that is the intended resume
signal for §2, not an error.

### 6d. Stop conditions

- If the owner does not answer a dialog, stop and wait, do not auto-apply.
- Do not batch-apply multiple improvements behind a single approval; one dialog per item.
- Do not touch application source code, run tests, or push/commit in the audited repo unless
  the owner explicitly asks. This command tunes the Claude setup, not the app.

---

## 7. Rewrite the audit-log row

After the walkthrough, rewrite exactly the `AREA_KEY` row in `projects/audit-log.md` (leave
all other rows untouched; add the row first if it is somehow still missing). The table
columns are:

`| Project | Status | Last audited | Snapshot | Notes |`

- **Project**: a markdown link to the sub-area's `improvements.md`, using `AREA_KEY` as the
  link text: e.g. `[your-project/claude-code](your-project/claude-code/improvements.md)` or
  `[your-project/codex](your-project/codex/improvements.md)` for a multi-tool sub-area, or
  `[another-project](another-project/improvements.md)` for a flat project.
- **Status**: from the project's `improvements.md` frontmatter `status:`
  (`active`/`paused`/`archived`/`ideation`).
- **Last audited**: today's date if you ran a lessons-reconciliation pass this run;
  otherwise `never` (an inventory-only pass with no lessons folded in still counts as
  `never`). Keep this in sync with the `last_audit:` you write into `improvements.md`
  frontmatter.
- **Snapshot**: the `snapshot:` date from `current.md` (or `-` for a non-codebase area with
  no snapshot).
- **Notes**: a one-line summary of this run: the lesson tally and what was applied / routed
  to area habits / routed to general habits / promoted out to `projects/habits.md` / dropped,
  plus the drift verdict from the snapshot refresh.

Also update the audited `improvements.md` frontmatter `last_audit:` to match (with a short
inline note of the batch), so the two never drift.

Then **commit the tracking updates in claudex-setup**: stage the `AREA_DIR` files,
`projects/audit-log.md`, and `projects/habits.md` if this run touched it (added a general habit
or promoted one), and commit with a conventional message (`docs(projects): ...`), no
co-author lines (repo rule). (`optimise.md` is gitignored, the transient run scratchpad never
enters a commit; only the durable files do.) Push only if the owner asks or asked earlier in
the session.
Changes made inside the audited project follow that project's own sync rules (e.g. a
gitignored `.claude/` synced by a separate config repo gets a `sync.sh push` reminder, not a
git commit).

---

## 8. Registry field reference (for reading/writing frontmatter)

`improvements.md` frontmatter fields:

| Field | Purpose |
|-------|---------|
| `name` | Display name |
| `path` | Local absolute path where the project actually lives (`null` for non-codebase areas) |
| `repo` | Git remote URL, optional |
| `stack` | Languages / frameworks the project is built on |
| `status` | `active`, `paused`, `archived`, `ideation` |
| `focus` | Which Claude areas to recommend in (categories mirror `lessons/` folders) |
| `last_audit` | ISO date of the most recent recommendation pass, or `null` |
| `tool` | (design or codex sub-area) e.g. `Claude Design`, `Codex` |

`improvements.md` body sections: **Summary** (what the project is + Claude-relevant traits) ·
**Recommended Claude Code/Design patterns** (grouped by impact; each cites its lesson and says
why it fits *this* project) · **Out of scope** (patterns deliberately not pursued) ·
**Notes for audits**.

`current.md` (codebases): frontmatter `name`, `snapshot:` (dated, with running history),
`actual_path:`, `repo`, `default_branch`, `inspected_from`; body = the factual inventory + a
"Drift vs improvements.md" table + a "How to refresh this snapshot" section.

`applied-improvements.md`: newest-first ledger, `## <date>` headings, one entry per applied
item (what / why / where it landed / follow-up / source lesson).

`habits.md` (any area): frontmatter `name`, `updated:`; body = `## High` / `## Medium` / `## Low`
prioritised owner-action entries, each citing its source lesson. Holds what the owner must do
during a session **on this project**; `improvements.md` holds what gets set up before one.

`projects/habits.md` (repo root, one file): same frontmatter and same three priority headings,
but scoped to owner actions that hold in **any** repo, across all three tools (a product
behaviour, a CLI flag, an account-level fact, a prompting move). Non-Claude-Code entries carry a
leading `(Codex)` / `(Claude Design)` marker. This is the destination for §4's **General habit**
bucket and for §5's promotions out of area files. It lives under `projects/`, which
`scripts/publish.sh` strips wholesale, so it is private by construction and may name real
projects, paths, and account specifics freely. A general habit that proves itself gets copied by
hand into the owner's global `~/.claude/CLAUDE.md`, the same promotion path `lessons/README.md`
defines from `lessons/` to a curated CLAUDE.md. This file is the staging area, not the
loaded-every-session form.

`optimise.md` (transient, gitignored): the current run's scratchpad. Holds this run's freshly
reconciled keepers, each with its full outline (what · why it fits · exact change or habit text
· source lesson), from the moment they are mined (§4) until each is dispositioned to a durable
home (applied to `applied-improvements.md`, backlogged to `improvements.md`, added to
`habits.md`, or dropped to "Out of scope"). Deleted when empty at the end of a clean run; a
leftover file is the resume signal read in §2. Never committed.

---

## 9. Final self-check (run before reporting done)

Confirm every item; if any fails, fix it before reporting:

1. **Mode & area resolved correctly**, the right `AREA_DIR` for `code` vs `--design` vs
   `--codex`, flat vs multi-tool; `AREA_KEY` matches.
2. **audit-log.md exists**, force-created if it was missing; the audited `AREA_KEY` row is
   rewritten and every other row is byte-for-byte unchanged.
3. **Snapshot refreshed**, `current.md` `snapshot:` bumped to today (inventory-diffed for
   code, conversationally for design), prior snapshot history preserved; already-done backlog
   items moved to the applied ledger.
4. **Lessons reconciled**, a bucket tally was reported; keepers were split across the three
   destinations (config · area habit · general habit); settled owner-decisions were not
   re-raised; recommendations citing superseded lessons were repointed. **No candidate was
   discarded for being general**, since that bucket has a home now (§4/§5); only *vague* ones
   were rejected. **The window started the day after the previous `last_audit`**, and the
   tally gives its per-date counts; a pass that took only its own day's batch has left a gap.
5. **Habits routed, not applied**, owner-action findings landed in the right habits file with
   `updated:` bumped: project-hooked ones in `AREA_DIR/habits.md`, any-repo ones in
   `projects/habits.md`, deduped against what that file already holds. None were pushed through
   the apply dialog. If the area had no `habits.md` and one was needed, it was created after
   asking. Any promotion out of an area file was approved item-by-item, capped at 3, and
   removed from the source file rather than duplicated. **And the inverse held:** no finding
   the model could perform itself under a rule, command or hook was filed as a habit; those went
   through the apply dialog as config (global config when they hold in any repo).
6. **Each apply dialog was self-contained**, from-scratch explanation in the question text,
   exact diff in the Apply option's preview, full outline printed in chat first.
7. **Applied items moved**, every approved change is out of `improvements.md` and into
   `applied-improvements.md` with what/why/where/lesson; JSON re-validated where edited;
   project content rules (e.g. em-dash ban) respected; sync reminder noted where relevant.
7a. **Scratchpad reconciled**, this run's keepers were flushed to `optimise.md` before the
   walkthrough; any prior interrupted run's items were resumed from it (§2); every dispositioned
   item was struck; the file was deleted if empty, or left with exactly the deliberately
   carried-forward remainder. `optimise.md` was **not** staged in the §7 commit.
8. **Frontmatter in sync**, `improvements.md` `last_audit:` matches the audit-log "Last
   audited" cell.
9. **No unrequested side effects**, no app source edits, test runs, commits, or pushes in
   the audited repo unless the owner asked. The claudex-setup tracking commit (§7) is the one
   expected commit; no push without approval.

Then report a short summary: the lesson tally, what was applied, what was routed to habits,
what was skipped/dropped and why, and the snapshot drift verdict.
