---
description: "Consolidate the lessons/ archive: merge near-duplicate lessons, split compound ones, prune superseded files, refresh INDEX. Counterpart to /extract-lessons."
argument-hint: "[category-or-glob]"
---

# Consolidate Lessons

`/extract-lessons` only ever *adds* (newer supersedes older on direct contradiction). Over many runs the archive accumulates near-duplicate active lessons and dead superseded files. This command does the periodic cleanup the extract loop can't: it merges overlapping lessons, splits compound ones whose sub-tips are invisible downstream, and prunes stale ones, so `INDEX.md` stays signal-dense.

**Argument:** `$ARGUMENTS`
- empty (default): propose a consolidation plan and apply it after listing the changes.
- `dry-run`: produce the plan only, list proposed merges/prunes, change nothing.
- a category (e.g. `agents`): scope consolidation to `lessons/<category>/` only.

## Steps

1. **Load the archive:**
   - `Read lessons/INDEX.md` and `lessons/README.md` (for the file format + supersession rules).
   - `Glob lessons/**/*.md` (exclude `INDEX.md`, `README.md`). Read each one's frontmatter (`id`, `status`, `category`, `supersedes`/`superseded_by`, `created`) and TL;DR.

2. **Spawn Explore subagents** to find redundancy and buried sub-tips (keep the bulk reading out of main context). One subagent suffices up to ~150 active lessons; above that, fan out over category batches, all launched in one message. Give each the per-lesson `{id, category, status, tldr, created}` records for its batch plus the full active slug list for dedupe, and ask it to return JSON identifying:
   - **merge clusters**: 2+ *active* lessons that cover the same idea and should become one canonical lesson (e.g. several "keep it under 200 lines" lessons). Pick the strongest as canonical; the rest get superseded by it. Same-claim redundancy ONLY: never merge two distinct actionable claims into one body, since that bundling is exactly the burial the split pass below exists to undo.
   - **split candidates**: an *active* lesson whose body carries one or more independently-actionable sub-tips absent from its title and TL;DR (a setting, a hook, a keyboard habit inside a bigger workflow's body). The subagent must read candidate bodies, not just TL;DRs. Downstream routing (`/optimise` habits, `/top-tips` tracing) reads titles and TL;DRs, so a buried sub-tip never surfaces; this pass is the retroactive counterpart of the `/extract-lessons` §5 atomicity rule for the corpus mined before 2026-08-29. A split-out tip that duplicates an existing active lesson is not a split, it is already covered: skip it.
   - **stale**: lessons whose advice is outdated/contradicted or whose feature no longer exists.
   - Tell it: be conservative, only cluster lessons that are genuinely redundant, not merely adjacent. Distinct nuances stay separate.
   ```json
   {
     "merges": [
       {"canonical_id": "keep-context-lean", "merge_in": ["id-a", "id-b"], "merged_tldr": "...", "merged_body": "...", "reason": "..."}
     ],
     "splits": [
       {"source_id": "compound-lesson-slug",
        "new_lessons": [{"id": "sub-tip-slug", "title": "...", "tldr": "...", "why": "...", "how": "...", "category": "workflows", "tool": "claude-code"}],
        "reason": "..."}
     ],
     "prune_stale": [ {"id": "...", "reason": "..."} ]
   }
   ```

3. **If `dry-run`:** print the proposed merges, splits, and prunes with reasons, then stop. Change nothing.

4. **Apply (default):**
   - **Merges:** update the `canonical_id` file with the merged TL;DR/body and union of `sources`. For each `merge_in` id: set `status: superseded`, add `superseded_by: <canonical_id>`. (Same mechanism as `/extract-lessons`, applied across same-topic actives.)
   - **Splits:** write each `new_lessons` entry as its own file in the `/extract-lessons` §7 format (`created:` today, `tool:` set explicitly, `supersedes: null`, `sources:` copied from the parent). Cross-link parent and child under `## Related` in both files; adding that link is the only edit the parent's body gets. The parent stays active with its headline claim, and the clause is not stripped from its body.
   - **Stale:** set `status: superseded` with a `superseded_by: null` and a `pruned: <today>` frontmatter note.
   - **Prune superseded files:** delete every `status: superseded` file (git history preserves them: they're already excluded from INDEX). Skip this deletion if a lesson was superseded in *this same run* and you want one cycle of review; otherwise remove.
   - **Normalise:** convert any relative dates ("last week") in frontmatter/body to absolute `YYYY-MM-DD`.

5. **Regenerate `lessons/INDEX.md`** exactly as `/extract-lessons` §8 does (active lessons only, grouped by TOOL then category, one bullet each; split-out lessons get their own bullets), and update the run summary line: `consolidated: N merged, K split, M pruned`.

6. **Report:** list merged clusters (canonical ← merged ids), split-out lessons (parent → new ids), pruned files, and the new active-lesson count.
