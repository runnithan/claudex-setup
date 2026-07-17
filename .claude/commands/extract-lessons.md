---
description: "Extract actionable agent-tooling lessons (Claude Code, Claude Design, Codex) from transcripts. Newer lessons supersede older contradicting ones."
---

# Extract Lessons

Mine reusable agent-tooling lessons from locally saved practitioner transcripts and file each one into the `lessons/` library as its own markdown file, keeping `lessons/INDEX.md` and the processed-transcript ledger in sync. Newer lessons supersede older contradicting ones on the same topic.

A "lesson" is a concrete, transferable improvement to how someone uses the **agent tooling this repo tracks — Claude Code, Claude Design, or Codex**: a command, flag, hook, skill pattern, workflow, config, design-surface technique, or gotcha that a reader could apply. Marketing claims, hype, product announcements without a usable technique, and generic AI-coding platitudes are NOT lessons.

> **Scope covers all three tools — do not silently drop two of them.** This command was Claude-Code-only until 2026-07-17, and the omission was self-confirming: Claude Design and Codex transcripts were marked processed while yielding ~0 lessons, so `/optimise --design` and `--codex` kept concluding "no relevant lessons exist" when the truth was that nobody had ever looked. A 28k-word Claude Design course and a 1-hour Codex course both extracted **zero**. If a transcript teaches real Claude Design or Codex technique, that is **in scope** and must be filed under `design` or `codex`. A zero-lesson result for a technique-dense transcript is a red flag to re-read it, not a valid outcome.

## Arguments

`$ARGUMENTS`:
- empty or `new` (default): process only transcripts not yet in `lessons/.processed.json`
- `all`: reprocess every transcript (rare — only when the extraction criteria change). **The criteria changed on 2026-07-17** (scope widened to Claude Design + Codex), so every transcript ledgered before that date was mined against Claude-Code-only criteria and its `.processed.json` entry is **not** evidence that its design or Codex content was ever considered. Re-run with `all` over the design/Codex-heavy scopes to backfill.
- a path or glob (e.g. `transcripts/ray-amjad/`): process just that scope, minus already-processed (unless `all` is also passed)

## Paths (all relative to the repo root — resolve the root first)

- Transcripts: `transcripts/<creator>/<slug>_<YYYYMMDD>.txt`
- Lessons library root: `lessons/`
- Index: `lessons/INDEX.md`
- Processed ledger: `lessons/.processed.json` (JSON `{"processed": ["transcripts/…/x.txt", …]}`)
- One file per lesson: `lessons/<category>/<slug>.md`

The 17 categories (create the dir on demand if a needed one is missing):
`agents`, `automation`, `commands`, `configuration`, `context-management`, `gotchas`, `hooks`, `mcp`, `memory`, `model-selection`, `permissions`, `plugins`, `prompting`, `remote-access`, `settings`, `skills`, `workflows`.
Pick the single best-fit category. If a lesson genuinely fits none, use `gotchas` as the fallback for pitfalls, else the closest topical dir. Do not invent new category names.

### Category vs tool — two axes, do not conflate them

**`category` is the TOPIC** (what the lesson is about) and lives in the folder tree. **`tool` is the PRODUCT** (which thing it applies to) and lives in frontmatter. They are independent: a Claude Design lesson about prompting is `category: prompting`, `tool: claude-design`. Never file a lesson by tool — there is deliberately no `design/` or `codex/` folder.

`tool:` values are `claude-code`, `claude-design`, `codex`. Three rules:

1. **Omitted means `claude-code`.** The pre-2026-07-17 corpus has no `tool:` field and is overwhelmingly Claude Code, so absent = `claude-code` and no backfill of old files is needed. **Set it explicitly on every NEW lesson**, including Claude Code ones.
2. **It may be a list** when a lesson genuinely spans tools: `tool: [claude-code, codex]` (e.g. `portable-setup-via-open-standards` — AGENTS.md as an open standard is true of both). This is the case a tool-keyed folder tree could not express, and the corpus is full of it: 69% of Claude Design transcripts are also Claude-Code-heavy (the export→code handoff is inherently two-tool), as are 40% of Codex-heavy ones (running them side by side, migrating projects, routing between them).
3. **Tool = where the reader TYPES, not what gets invoked.** `codex-second-opinion-three-mechanisms` is `tool: claude-code` (you type it in Claude Code; it calls Codex) — not `codex`. Use the optional `about:` field when a lesson targets another tool from one tool.

`/optimise` scopes each tracked area by `tool:`, not by folder — `--design` reads every lesson with `claude-design` in its `tool:`, wherever it sits. A lesson with no `tool:` is invisible to the `--design` and `--codex` audits, which is exactly how Claude Design went unmined before this field existed.

## Procedure

### 1. Locate the library and detect fresh-start vs. incremental

1. Find the repo root: the nearest ancestor directory that contains a `lessons/` directory or a `transcripts/` directory. If both exist, use that root. Run all later paths from there.
2. Determine state:
   - **Fresh start** if `lessons/` is missing OR `lessons/INDEX.md` is missing OR `lessons/.processed.json` is missing. This happens on a standalone/plugin install with no library yet.
   - **Incremental** otherwise.
3. Handle the source list gracefully:
   - If `transcripts/` is missing or contains no `*.txt` files, STOP and report: "No transcript source found at `transcripts/` — nothing to extract." Do not error out. This is a valid standalone/plugin state.

### 2. Fresh-start layout (only if fresh start)

Create the library skeleton before extracting:
1. Create `lessons/` and each of the 17 category directories on demand (create a category dir only when you actually write a lesson into it — do not pre-create all 17 empty).
2. Create `lessons/.processed.json` with `{"processed": []}`.
3. Create `lessons/INDEX.md` with this exact top structure:

```markdown
# Lessons Index

Active lessons learned from transcripts about improving Claude Code usage. Generated by `/extract-lessons`.

**How to use this file:** read this index first to scan known lessons. Drill into individual files for detail. Lessons are filed under `lessons/<category>/`. Superseded lessons are not listed here — find them via `grep -lr "status: superseded" lessons/`.

---

## Active lessons

## Last extraction run
```

(Optionally also write a `lessons/README.md` describing the format if none exists — but INDEX + ledger are the load-bearing files.)

### 3. Build the work list

1. Read `lessons/.processed.json` → set of already-processed transcript paths.
2. Enumerate transcripts per the argument: default/`new` → every `transcripts/**/*.txt`; a path/glob → just that scope. Exclude non-transcript `.txt` files (e.g. `transcripts/urls.txt`, the URL seed list — anything not under a per-creator folder); do not mine or ledger them.
3. Work list = enumerated files MINUS already-processed (skip the subtraction when `all` was passed). If empty, STOP and report "All transcripts already processed (N in ledger); no new lessons." Do not re-mine processed transcripts.

### 4. Load the dedupe corpus

Before mining, build the picture of what already exists so you don't produce duplicates:
1. Read `lessons/INDEX.md` in full — the one-line hooks under each `###` category are your fast duplicate scan.
2. Note existing slugs: `ls lessons/*/` gives every existing `<slug>.md`. Duplicate detection is by *topic/claim*, not just slug.

### 5. Mine transcripts via subagents (transcripts are large — keep them out of main context)

Never read transcripts in the main session; the mining always happens in `Explore` subagents:

- **If the work list is ≤ ~10 transcripts:** spawn ONE `Explore` subagent with the whole list.
- **If more than ~10:** fan out to parallel `Explore` subagents. Split the work list into N batches of roughly 8–15 transcripts each (aim for 4–10 batches; keep batches small enough to avoid OOM — do not launch dozens of subagents at once). Launch all batch subagents in a single message so they run concurrently.

Give each miner subagent this instruction set:
- Here is your batch: `<explicit list of absolute transcript paths>`.
- Here is the current lesson corpus to dedupe against: `<the INDEX.md hooks + existing slug list>`.
- For each transcript, extract only concrete, transferable Claude Code usage lessons:
  - **In scope — Claude Code:** specific workflows, slash commands, hooks, settings, agent patterns, MCP usage, plugin recipes, prompt techniques, gotchas.
  - **In scope — Claude Design** (`tool: claude-design`): canvas and draw-tool technique, Tweaks panel, anchoring generations to a design system or tokens, structure-then-copy prompting, rendering full UI state matrices, export and handoff into code, quota tactics, Open Design. Note the export→code handoff usually earns `tool: [claude-design, claude-code]`.
  - **In scope — Codex** (`tool: codex`): `AGENTS.md` and `.codex/config.toml` practice, Codex CLI commands/approvals/sandboxing, splitting work between Codex and Claude Code, running them side by side. Side-by-side/routing/migration lessons usually earn `tool: [claude-code, codex]`. Calling Codex *from* Claude Code is `tool: claude-code` + `about: codex`, category `mcp`.
  - **Set `tool:` on every lesson you return**, Claude Code ones included, and use the list form rather than forcing a single tool onto a genuinely cross-tool lesson.
  - **Out of scope:** generic LLM tips, news/announcements without an action, opinions without evidence, marketing/hype. **Model comparisons** are out of scope as verdicts ("X beats Y"), but a comparison video that yields a concrete *routing* rule ("use Codex for X because Y") IS a lesson — file it under `codex` or `model-selection`.
  - **Each lesson must be:** actionable (a thing the user can do or stop doing), specific (not "use Claude well"), and grounded (cite the transcript).
- Return candidates as a single JSON object — do NOT write files:
  ```json
  {
    "new_lessons": [
      {"id": "slug-form", "title": "...", "tldr": "...", "why": "...", "how": "...",
       "category": "workflows", "tool": "claude-design", "sources": ["transcripts/..."]}
    ],
    "supersedes": [
      {"new_id": "slug-form", "old_id": "existing-slug", "reason": "..."}
    ],
    "processed": ["transcripts/path/to/transcript.txt"]
  }
  ```
  `supersedes` names any existing corpus entry a candidate duplicates or contradicts. `processed` lists every transcript the miner actually read, even zero-lesson ones.

Collect all candidates from all miners into one list.

### 6. Dedupe and resolve

For each candidate, in order:
1. **Duplicate of an active lesson (same claim, same advice):** drop it. Do not write a file.
2. **Contradicts / supersedes an active lesson (same topic, better or corrected advice):** write a NEW file (never edit the old one). The old file lives at `lessons/<old-category>/<old-id>.md` — use `Glob lessons/**/<old-id>.md` if the category is unknown. Mark the old file `status: superseded` and add `superseded_by: <new-id>`; the new file gets `supersedes: <old-id>`. Remove the old lesson's bullet from INDEX (INDEX lists active only).
3. **Genuinely new:** write a new file.
4. Merge near-identical candidates that came from different transcripts into ONE lesson whose `sources:` lists all contributing transcript paths.

### 7. Write lesson files

Each lesson is `lessons/<category>/<slug>.md`. Slug = kebab-case of the core claim (short, descriptive, unique). If a file with that slug already exists in the category and is NOT being superseded, append a numeric suffix (`<slug>-2.md`). Exact format:

```markdown
---
id: <slug>
created: <YYYY-MM-DD>            # today's date
status: active
supersedes: null                # or <old-id> when this replaces one
category: <one of the 17>       # TOPIC — what it's about (mirrors the folder)
tool: claude-code               # PRODUCT — claude-code | claude-design | codex
                                #   list several when it genuinely spans: [claude-code, codex]
                                #   = where the reader TYPES, not what gets invoked
about: <tool>                   # OPTIONAL — the tool being driven, when different
                                #   e.g. tool: claude-code / about: codex
sources:
  - transcripts/<creator>/<file>.txt
  - transcripts/<creator>/<other>.txt   # list every contributing transcript
---

# <Imperative, specific lesson title>

## TL;DR

<One or two sentences: the takeaway a reader can act on.>

## Why it matters

<Why this is true / what breaks without it. Ground it in what the transcript showed.>

## How to apply

<Concrete steps, exact command/flag/setting names.>

## Related

[[other-lesson-slug]], [[another-slug]]   # optional; omit the section if none
```

Notes:
- `supersedes:` is `null` unless this lesson replaces one.
- Add `source_type: canonical` or `source_type: post` ONLY for non-transcript sources (docs/changelog/social); plain transcript lessons omit `source_type`.
- Cross-link related lessons with `[[slug]]` wikilinks in an optional `## Related` section.

### 8. Update INDEX.md

1. **INDEX is grouped by TOOL first, then category.** The folder tree is topical, so the index is where a tool's lessons become browsable as a set — this is the tool-scoped view, and it is why no `design/` or `codex/` folder is needed. Top-level `##` sections, in this order:
   - `## Claude Design` — every lesson whose `tool:` includes `claude-design`
   - `## Codex` — every lesson whose `tool:` includes `codex`
   - `## Cross-tool` — lessons whose `tool:` lists more than one (append ` — <tool-a> + <tool-b>` to the hook). List each here **only**, not again under its individual tools.
   - `## Claude Code` — everything else (the bulk; `tool:` omitted or `claude-code`), sub-grouped by `### <Category>` as before.

   Under the three tool sections, group by `### <Category>` too once a section has enough entries to warrant it; a short section can be a flat bullet list. Bullet format is identical everywhere — the path is the lesson's real topical folder, which is the point:
   ```
   - [<Lesson Title>](<category>/<slug>.md) — <one-sentence hook, same as TL;DR essence>.
   ```
   So a Claude Design lesson living at `lessons/workflows/claude-design-draw-to-code.md` appears under `## Claude Design`, linking into `workflows/`. Nothing moves on disk.
2. For any superseded lesson, delete its bullet.
3. Append/refresh the `## Last extraction run` footer with a dated entry at the top of that section:
   ```
   <YYYY-MM-DD> — /extract-lessons: <N> new, <M> superseded, <K> transcripts processed (<short note on creators/sources and how many candidates were dropped as duplicates/low-signal>). <highlights, optional>.
   ```
   Keep prior run entries below it (newest first). Leave `## Last social run` and `## Last consolidation run` untouched.

### 9. Update the ledger

Add every transcript path from this run's work list to `lessons/.processed.json` `processed` array (even ones that yielded zero lessons — they are "processed"). Keep it valid JSON, sorted or append-only is fine; do not drop existing entries.

### 10. Self-check (do all before reporting done)

- [ ] Every new lesson file has valid YAML frontmatter with `id`, `created`, `status: active`, `supersedes`, `category`, **`tool`**, and a non-empty `sources` list pointing at real transcript paths.
- [ ] **`tool:` is set explicitly on every new lesson** (never left to the absent-means-claude-code default), uses only `claude-code`/`claude-design`/`codex`, and uses the list form for genuinely cross-tool lessons rather than forcing one. No lesson was filed into a `design/` or `codex/` folder — those deliberately do not exist; tool is a field, category is the folder.
- [ ] Every new lesson appears as a bullet under the correct tool section (`## Claude Design` / `## Codex` / `## Cross-tool` / `## Claude Code`) and `### Category` in INDEX.md; cross-tool lessons appear under `## Cross-tool` only; no superseded lesson still appears there.
- [ ] Any supersession is bidirectional (old has `superseded_by`, new has `supersedes`).
- [ ] No duplicate of an existing active lesson was written.
- [ ] `.processed.json` now contains every transcript from this run and is valid JSON.
- [ ] The `## Last extraction run` footer has today's dated entry with accurate counts.
- [ ] Category dirs used all exist; no invented category names.

### 11. Report

Report concisely: N lessons written (by category), M superseded, K transcripts processed, how many candidates were dropped as duplicates/low-signal, and a few highlight titles. State plainly if the run was a fresh start or found no new transcripts.
