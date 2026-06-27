---
description: Audit a tracked project's Claude Code setup, fold in new lessons, then apply open improvements one at a time with approval. Takes a project name from projects/.
argument-hint: <project-name>
---

# Optimise

Audit a tracked project's Claude Code setup, reconcile its notes with the latest lessons, then walk through the open improvements one at a time and apply the ones the user approves.

**Argument:** `$ARGUMENTS` — a project name matching a folder under `projects/` (e.g. `your-project`, `another-project`, `personal-notes`).
- If empty or no matching folder exists: list the available folders under `projects/` and stop.

## Steps

### 1. Resolve the project

- Confirm `projects/$ARGUMENTS/` exists; read `current.md`, `improvements.md`, `applied-improvements.md`, and `habits.md` (the last two may not exist — treat as empty, create on first use).
- Get the project's real path from frontmatter (`path:` / `actual_path:`). Verify it exists before proceeding — if not, stop and report.
- Read the project's "Notes for audits" section and obey its quirks (e.g. your-project: em dashes banned in anything generated *for* the project; its `.claude/` is gitignored and syncs via a separate config repo, not the project's git).
- **Ensure the central tracker exists (force-create on first use).** If `projects/audit-log.md` does not exist, create it: one row per existing `projects/*/` folder, each row's `last_audit` read from that project's `improvements.md` frontmatter (`null` → "never"). If the tracker exists but this project has no row, add one. This file is the single source of truth for "when was each project last optimised" — the per-project `last_audit:` frontmatter stays authoritative for one project; the tracker is the rollup, rewritten by this command so it never drifts.

### 2. Refresh the snapshot (`current.md`)

- Spawn an **Explore subagent** to inventory the project's `.claude/` (keeps the noisy listing out of main context). Ask it for: settings.json + settings.local.json (hooks, permissions, statusLine, env), agent frontmatter (model/tools/isolation), skills, commands, hooks files vs hooks *wired in settings*, plugins, scripts, references, GSD version if present. Pass it the previous snapshot so it reports **diffs**, not a full dump.
- Update `current.md`: correct anything that drifted, update the drift table, bump `snapshot:` to today.
- Anything in `improvements.md` the fresh snapshot shows is already done → move it to `applied-improvements.md` with today's date.

### 3. Reconcile lessons (`improvements.md`)

- Read `lessons/INDEX.md`. Collect lessons whose `created` date is after the project's `last_audit` (check frontmatter of candidate lesson files; superseded lessons are already excluded from INDEX).
- Evaluate each new lesson for fit against the project's stack and traits (in `improvements.md` Summary). Most won't fit — only add ones with a concrete, project-specific application. Cite the lesson path and say *why it fits this project*.
- Fix any existing recommendations that cite a lesson now marked superseded (point to the successor).
- Bump `last_audit:` to today.

### 4. Apply improvements interactively

Walk `improvements.md` top-down (high-impact → medium → low → hygiene), **one item at a time**:

- **Classify the item first.** If it's a *user habit* (something the user does at the keyboard — a command to type, a discipline to follow) rather than a config/file change Claude can make, route it to `projects/$ARGUMENTS/habits.md` instead: a prioritised ledger of keyboard habits (sections High / Medium / Low by payoff for this project), each entry with the habit, when to use it, and the lesson citation. Create the file on first use. The question options become **Add to habits** / **Skip** / **Drop** / **Stop**; on *Add*, write it into habits.md under the right priority and remove it from improvements.md.
- For config/file items, ask via AskUserQuestion with options **Apply now** / **Skip for now** (stays in backlog) / **Drop** (remove — no longer wanted) / **Stop here** (end the loop, keep the rest). **The question dialog must be self-contained** — the user decides from the dialog alone, without reading chat prose above it:
  - **The `question` text itself** carries the explanation: 3-5 plain-language sentences assuming the user has NEVER heard of the pattern — what Claude does today without it, what would change, and the cost. No jargon, no lesson names, no pattern names as if they're known terms.
  - **The "Apply now" option's `preview`** shows the concrete change: the exact lines/diff/settings block that would be written, with the target file path as a heading.
  - Option `description`s state plainly what happens on selection (e.g. "Writes the lines shown in the preview to <file>").
- Longer background (lesson citation, analogies, broader context) can go in chat prose before the call, but never rely on it being read.
- On *Apply*: make the changes in the target project's `.claude/` directly, verify (e.g. JSON parses, referenced files exist), then move the item to `applied-improvements.md` with today's date and a one-line note of what was done.
- On *Drop*: remove from `improvements.md`, note the removal in the final report.
- Items flagged "verify from a project session" or blocked on missing info (e.g. an upstream URL): present them, but only to ask keep/drop — don't attempt them.

### 5. Commit

- **Update the tracker.** Rewrite this project's row in `projects/audit-log.md` from its just-updated state: `status` and `last_audit` from `improvements.md` frontmatter, the `current.md` snapshot date, and a one-line note for this run (e.g. "Jun 21 batch: 4 config + 4 habits").
- In **claude-setup**: commit the `projects/$ARGUMENTS/` updates **and `projects/audit-log.md`** (`docs(projects): ...`, conventional commits, no co-author lines). Push only if the user asks or asked earlier in the session.
- Changes inside the **target project** follow that project's own sync rules from step 1 (e.g. your-project: remind the user to run the config repo's `sync.sh push`; its `.claude/` won't sync via git).

### 6. Report

- Snapshot: what drifted since the last check.
- Lessons: N evaluated, M added as recommendations.
- Improvements: applied / skipped / dropped counts, with one line each for applied items.
- Anything that needs a session inside the target project to finish.
