---
description: "Consolidate the lessons/ archive: merge near-duplicate lessons, prune superseded files, refresh INDEX. Counterpart to /extract-lessons."
argument-hint: "[category-or-glob]"
---

# Consolidate Lessons

`/extract-lessons` only ever *adds* (newer supersedes older on direct contradiction). Over many runs the archive accumulates near-duplicate active lessons and dead superseded files. This command does the periodic cleanup the extract loop can't: it merges overlapping lessons and prunes stale ones, so `INDEX.md` stays signal-dense.

**Argument:** `$ARGUMENTS`
- empty (default): propose a consolidation plan and apply it after listing the changes.
- `dry-run`: produce the plan only — list proposed merges/prunes, change nothing.
- a category (e.g. `agents`): scope consolidation to `lessons/<category>/` only.

## Steps

1. **Load the archive:**
   - `Read lessons/INDEX.md` and `lessons/README.md` (for the file format + supersession rules).
   - `Glob lessons/**/*.md` (exclude `INDEX.md`, `README.md`). Read each one's frontmatter (`id`, `status`, `category`, `supersedes`/`superseded_by`, `created`) and TL;DR.

2. **Spawn an Explore subagent** to find redundancy (keep the bulk reading out of main context). Give it the per-lesson `{id, category, status, tldr, created}` records and ask it to return JSON identifying:
   - **merge clusters** — 2+ *active* lessons that cover the same idea and should become one canonical lesson (e.g. several "keep it under 200 lines" lessons). Pick the strongest as canonical; the rest get superseded by it.
   - **stale** — lessons whose advice is outdated/contradicted or whose feature no longer exists.
   - Tell it: be conservative — only cluster lessons that are genuinely redundant, not merely adjacent. Distinct nuances stay separate.
   ```json
   {
     "merges": [
       {"canonical_id": "keep-context-lean", "merge_in": ["id-a", "id-b"], "merged_tldr": "...", "merged_body": "...", "reason": "..."}
     ],
     "prune_stale": [ {"id": "...", "reason": "..."} ]
   }
   ```

3. **If `dry-run`:** print the proposed merges and prunes with reasons, then stop. Change nothing.

4. **Apply (default):**
   - **Merges:** update the `canonical_id` file with the merged TL;DR/body and union of `sources`. For each `merge_in` id: set `status: superseded`, add `superseded_by: <canonical_id>`. (Same mechanism as `/extract-lessons`, applied across same-topic actives.)
   - **Stale:** set `status: superseded` with a `superseded_by: null` and a `pruned: <today>` frontmatter note.
   - **Prune superseded files:** delete every `status: superseded` file (git history preserves them — they're already excluded from INDEX). Skip this deletion if a lesson was superseded in *this same run* and you want one cycle of review; otherwise remove.
   - **Normalise:** convert any relative dates ("last week") in frontmatter/body to absolute `YYYY-MM-DD`.

5. **Regenerate `lessons/INDEX.md`** exactly as `/extract-lessons` step 6 does (active lessons only, grouped by category, one bullet each), and update the run summary line: `consolidated: N merged, M pruned`.

6. **Report:** list merged clusters (canonical ← merged ids), pruned files, and the new active-lesson count.
