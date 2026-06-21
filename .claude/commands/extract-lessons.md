---
description: "Extract actionable Claude Code improvement lessons from transcripts. Newer lessons supersede older contradicting ones."
---

# Extract Lessons

Mine `transcripts/` for actionable improvements to Claude Code usage and write them to `lessons/`. Newer lessons supersede older contradicting ones on the same topic.

**Argument:** `$ARGUMENTS`
- empty or `new` (default): only process transcripts not in `lessons/.processed.json`
- `all`: reprocess every transcript (rare — use only when changing extraction criteria)
- a path or glob (e.g. `transcripts/ray-amjad/`): process just that scope

## Steps

1. **Resolve target transcripts:**
   - If `lessons/.processed.json` does not exist, treat as empty `{ "processed": [] }`
   - For `new`/empty: `Glob` `transcripts/**/*.txt` minus already-processed paths
   - For `all`: every `transcripts/**/*.txt`
   - For a path/glob: `Glob` that scope, minus processed (unless `all` is also passed)
   - If the resolved list is empty: report "No new transcripts to process." and stop

2. **Read existing lesson context:**
   - If `lessons/` or `lessons/INDEX.md` doesn't exist yet, treat this as a fresh start (no existing lessons) — don't error. The folder, category subdirs, and `INDEX.md` are created in steps 4 and 6.
   - Otherwise `Read lessons/INDEX.md`
   - List active lesson files: `Glob lessons/**/*.md` (exclude `INDEX.md`, `README.md`)
   - Lessons are filed under `lessons/<category>/<id>.md` — keep that layout
   - Skim their frontmatter + TL;DR so you know what's already known

3. **Spawn an Explore subagent** to do the actual mining (transcripts are large — keep them out of main context). Pass it:
   - The list of target transcript paths
   - The list of existing active lesson IDs and TL;DRs
   - These extraction criteria:
     - **In scope:** specific Claude Code workflows, slash commands, hooks, settings, agent patterns, MCP usage, plugin recipes, prompt techniques, gotchas
     - **Out of scope:** generic LLM tips, model comparisons, news/announcements without an action, opinions without evidence
     - **Each lesson must be:** actionable (a thing the user can do or stop doing), specific (not "use Claude well"), and grounded (cite the transcript)
   - Ask the subagent to return JSON. Each lesson must include a `category` chosen from: `workflows`, `agents`, `skills`, `plugins`, `hooks`, `settings`, `configuration`, `permissions`, `context-management`, `model-selection`, `mcp`, `memory`, `prompting`, `automation`, `remote-access`, `commands`, `gotchas`. Fall back to `uncategorized` only if nothing fits.
     ```json
     {
       "new_lessons": [
         {"id": "slug-form", "title": "...", "tldr": "...", "why": "...", "how": "...", "category": "workflows", "sources": ["transcripts/..."]}
       ],
       "supersedes": [
         {"new_id": "slug-form", "old_id": "existing-slug", "reason": "..."}
       ],
       "processed": ["transcripts/path/to/transcript.txt", ...]
     }
     ```

4. **Apply the subagent's output:**
   - For each entry in `supersedes`:
     - Read the old file (it lives at `lessons/<old-category>/<old-id>.md`; use `Glob lessons/**/<old-id>.md` if the category is unknown). Add `superseded_by: <new_id>` to its frontmatter and change `status: active` → `status: superseded`.
   - For each entry in `new_lessons`:
     - Ensure the category folder exists: `lessons/<category>/`.
     - Write `lessons/<category>/<id>.md` with frontmatter (`id`, `created: <today>`, `status: active`, `supersedes: <old-id-or-null>`, `category: <category>`, `sources: [...]`) and the body sections (TL;DR, Why it matters, How to apply).
     - If a file with that id already exists in that category folder and is NOT being superseded, append a numeric suffix (`<id>-2.md`).

5. **Update `lessons/.processed.json`:**
   - Merge the returned `processed` list into the existing one (deduped, sorted)

6. **Regenerate `lessons/INDEX.md`:**
   - List every `lessons/**/*.md` (excluding `INDEX.md`, `README.md`) where frontmatter `status: active`
   - Group by the lesson's `category` frontmatter field (matches its parent folder)
   - One bullet per lesson: `- [<title>](<category>/<id>.md) — <tldr>`
   - Update the "Last extraction run" section with today's date and a one-line summary (`N new, M superseded, K transcripts processed`)

7. **Report to user:**
   - "Added N lessons, superseded M, processed K transcripts."
   - List new lesson IDs with TL;DRs
   - Note any superseded lessons with the reason
