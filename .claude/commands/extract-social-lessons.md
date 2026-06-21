---
description: "Mine Claude Code lessons from recent posts by notable practitioners (X/Twitter, blogs, GitHub) and canonical sources (changelog, docs, issues, Hacker News) via a research subagent team. Counterpart to /extract-lessons (transcripts)."
---

# Extract Social Lessons

`/extract-lessons` mines YouTube transcripts. This mines **recent public posts** from
people who build and push Claude Code — Boris Cherny, Anthropic's Claude Code team, and
sharp community voices — **plus the canonical non-person sources** where Claude Code's own
behaviour is documented first (changelog, docs, GitHub issues, Hacker News). It runs a
fan-out research team and writes into `lessons/` alongside the transcript lessons, tagged
`source_type: post` for people and `source_type: canonical` for the primary sources.

**Argument:** `$ARGUMENTS`
- empty / `new` (default): search for posts not already in `lessons/.processed-social.json`
- `all`: ignore the dedup ledger and re-search everything
- a name/handle (e.g. `boris-cherny`): scope to one voice

## Steps

1. **Load context:**
   - Read `references/agentic-coding-voices.md` → both the people (name, handle, links) AND the **Canonical / non-person sources** tier (changelog, docs, GitHub issues, HN). Skip `#`/comment lines. **If this file doesn't exist** (e.g. the commands were installed standalone, without the rest of the repo), report: "No source list found — add `references/agentic-coding-voices.md` (see the claude-setup repo for the format)." and stop.
   - Read `lessons/.processed-social.json` (post URLs already mined; treat a missing file as `{ "processed": [] }`).
   - Read `lessons/INDEX.md` and skim active lesson ids + TL;DRs (so new posts dedup against what's already known, including transcript lessons). **If `lessons/` or `INDEX.md` doesn't exist yet, treat this as a fresh start** (no existing lessons) — don't error; it's created when lessons are written and the index regenerated.

2. **Spawn a research subagent TEAM** — one agent per voice (or small group), each with `WebSearch` + `WebFetch`, run in parallel. Give each its target person(s), the existing active lesson ids/TL;DRs, and the already-processed post URLs. Each agent:
   - Finds that person's **recent** (prefer ~last 60 days) public posts about Claude Code — search X/Twitter (incl. thread-reader and nitter-style mirrors when the direct page is login-walled), their blog, the Anthropic engineering blog, and GitHub. 
   - Extracts only **actionable Claude Code lessons** — same bar as `/extract-lessons`: a concrete thing to do or stop doing, specific (not "use Claude well"), and **grounded in a real quoted post with its URL**.
   - Skips any post already in the processed ledger.
   - Returns JSON:
     ```json
     {
       "new_lessons": [
         {"id": "slug", "title": "...", "tldr": "...", "why": "...", "how": "...",
          "category": "workflows", "source_type": "post", "sources": ["https://post-url"]}
       ],
       "supersedes": [ {"new_id": "slug", "old_id": "existing-slug", "reason": "..."} ],
       "processed": ["https://post-url", "..."]
     }
     ```
   - **Caveats to pass every agent:** X/Twitter has no open API — rely on what web search surfaces and on mirrors; **verify each post is real and quote it** before extracting; ignore paraphrased/second-hand or unverifiable claims; never invent a post or a quote. A product announcement or hot take is **not** a lesson — drop it.

   **Also spawn a canonical-sources agent** (or one per source) with `WebSearch` + `WebFetch` (and `Bash` for `gh` / the HN Algolia API). Same extraction bar, dedup, and JSON return as the voice agents, but tag these `source_type: canonical`:
   - **Claude Code changelog** — read entries newer than the last run; for each new command / flag / hook, extract the *usage* lesson (what to now do or stop doing), not just "X was added."
   - **Claude Code docs** (best-practices page) — pull concrete guidance not already captured as a lesson.
   - **`anthropics/claude-code` GitHub issues & discussions** — mine confirmed gotchas and team-suggested workarounds (prime "never do X" material); quote the issue and link it.
   - **Hacker News** — query the Algolia API for recent Claude Code threads; extract concrete workflows from substantive comments, quoting and linking the comment. Skip announcements and hot takes.

3. **Merge + dedup** across agents and against existing active lessons. Apply supersession on direct contradiction (newer wins), same rule as `/extract-lessons`.

4. **Apply:** for each new lesson write `lessons/<category>/<id>.md` (creating the `lessons/<category>/` folder if it doesn't exist) with frontmatter (`id`, `created: <today>`, `status: active`, `supersedes: <old-id-or-null>`, `category`, `source_type: post` — or `canonical` for changelog/docs/GitHub/HN sources, `sources: [URLs]`) and the body (TL;DR, Why it matters, How to apply). If a lesson overlaps an existing transcript lesson, add a `[[other-id]]`-style cross-reference rather than duplicating. Use category folders from the same list `/extract-lessons` uses.

5. **Update `lessons/.processed-social.json`** — merge in the post URLs seen (deduped, sorted). Kept separate from the transcript ledger (`.processed.json`).

6. **Regenerate `lessons/INDEX.md`** exactly as `/extract-lessons` does (active lessons only, grouped by category).

7. **Report:** "N lessons from M voices." List new lesson ids with their TL;DR and source URL, and note any superseded lessons.

## Notes
- Public posts only — no login-walled scraping, respect each platform's ToS.
- Quality over coverage: when a post is borderline, drop it. A wrong or hallucinated "lesson" is worse than a missing one.
- Maintain the voice list in `references/agentic-coding-voices.md`.
