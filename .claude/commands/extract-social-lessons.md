---
description: "Mine Claude Code lessons from recent posts by notable practitioners (X/Twitter, blogs, GitHub) and canonical sources (changelog, docs, issues, Hacker News) via a research subagent team. Counterpart to /extract-lessons (transcripts)."
---

# Extract Social Lessons

Fan out a small team of research subagents over **recent public posts** by the
practitioners listed in `references/agentic-coding-voices.md` (plus the canonical
non-person sources), extract concrete Claude-Code / agentic-coding lessons, dedupe
them against what already exists, and write each new lesson as one file under
`lessons/<category>/`, indexed in `lessons/INDEX.md`.

This is the **web counterpart** to `/extract-lessons`. That command mines local
YouTube/transcript files; this one mines the open web. Both write into the same
`lessons/` archive in the same format, so a lesson is a lesson regardless of where it
came from — the only frontmatter difference is `source_type` and the `sources` URL.

Run this from the root of the `claudex-setup` repo (the one containing `references/`
and `lessons/`).

---

## What counts as a lesson

A **concrete, actionable thing to do or stop doing** when using Claude Code (or a
transferable agentic-coding practice), grounded in a **real quoted line** with its
**source URL**. Test each candidate against all four:

1. **Actionable** — it tells you to *do X* or *stop doing Y*, not just "X exists."
   A bare feature announcement is not a lesson; extract the **usage implication**
   ("now do X instead of Y") or drop it.
2. **Specific** — names the command / flag / hook / setting / pattern precisely
   enough to act on without re-reading the source.
3. **Grounded** — you can quote a real sentence from the post and cite its URL.
   No quote, no lesson.
4. **Non-obvious** — it isn't already common knowledge or already in `lessons/`.

Reject vague sentiment ("Claude Code is great for refactors"), pure marketing, and
anything you can't tie to a specific quoted line.

---

## Arguments

- `$ARGUMENTS` — optional. Free text controlling scope. Recognized hints:
  - empty / `new` (default): search for posts not already in `lessons/.processed-social.json`;
  - `all`: ignore the processed ledger and re-search everything;
  - a name/handle (e.g. `boris-cherny`): scope the run to that one voice;
  - a recency window, e.g. `last 30 days`, `since 2026-06-01` (default: **the last
    8 weeks** from today);
  - a tier filter, e.g. `canonical only` or `tier 1 only`;
  - `dry-run` — do everything except write files; report the plan and the candidate
    lessons instead.

If no arguments, use the defaults: `new`, last 8 weeks, all tiers, write mode.

---

## Preflight (do this first, in the main session)

1. **Load the voice list.** Read `references/agentic-coding-voices.md`.
   - **If it does not exist → STOP.** Report cleanly: "`references/agentic-coding-voices.md`
     is missing; this command reads its voice list from there. Restore or create it
     (see the claudex-setup repo for the format), then re-run." Do not guess a voice
     list from memory.
   - Parse it into its tiers. Lines starting with `#` are section headers, not voices.
     Each voice line is `- Name — role — @handle (X) / blog-url`. Note the
     **Canonical / non-person sources** tier separately — those get `source_type: canonical`.
2. **Load the processed ledger.** Read `lessons/.processed-social.json` (post URLs
   already mined on prior runs; treat a missing file as `{"processed": []}`). Unless
   `all` was passed, these URLs are out of scope — pass the list to every subagent so
   they skip them. This ledger is what makes re-runs cheap; the recency window alone
   does not prevent re-mining the same post. It is kept separate from the transcript
   ledger (`.processed.json`).
3. **Load existing lessons for dedupe.** Read `lessons/INDEX.md` if present, and glob
   `lessons/**/*.md`. Build a lightweight in-memory list of `{id, title, TL;DR,
   category, sources}` for every existing lesson (both `status: active` and
   `superseded` — you dedupe against all of them).
   - **If `lessons/` or `INDEX.md` is absent → fresh start.** Create `lessons/` and an
     empty `INDEX.md` scaffold on first write. Do not treat absence as an error.
4. **Compute the recency window.** Resolve the cutoff date (default: today − 8 weeks).
   Only posts **published on or after** the cutoff are in scope. Older posts are out
   of scope even if excellent — this command harvests *what's new*.
5. **Note the categories.** Use the SAME category list as `/extract-lessons` (the
   two commands share the archive): `agents`, `automation`, `commands`,
   `configuration`, `context-management`, `gotchas`, `hooks`, `mcp`, `memory`,
   `model-selection`, `permissions`, `plugins`, `prompting`, `remote-access`,
   `settings`, `skills`, `workflows`. Pick the single best-fit category per lesson;
   create the category folder on write if it doesn't exist. Do not invent new
   category names.

---

## Subagent fan-out plan

Spawn **five research subagents in parallel**, one per source cluster. Under a tier or
voice filter (e.g. `canonical only`, `tier 1 only`, a single name), spawn ONLY the
matching cluster(s) — do not run the full fan-out for a scoped request. Each is
read-only (WebSearch + WebFetch; no Write/Edit — the **canonical-scout** may also use
Bash for the `gh` CLI and the HN Algolia API). Give each the recency cutoff, the
"what counts as a lesson" bar above, the list of already-known lesson titles/TL;DRs
for its likely categories (so it can self-dedupe), and the **exact candidate-return
format** (below). Each subagent returns a list of candidate lessons as text — it does
**not** write files. The main session does all writing.

Do NOT hand a subagent a narrow checklist of "find exactly these 3 things"; give it
the source cluster, the bar, and let it surface what's actually there. Cap each
subagent at a sensible search budget (roughly 8–15 web searches / fetches) so the run
stays bounded.

| # | Subagent | Sources it scouts | source_type it tags |
|---|----------|-------------------|---------------------|
| 1 | **canonical-scout** | The **Canonical / non-person** tier: Claude Code CHANGELOG (for each new command/flag/hook, extract the *usage* lesson — what to now do or stop doing — not just "X was added"), Claude Code docs (esp. best-practices page), `anthropics/claude-code` GitHub issues & discussions (confirmed gotchas and team-suggested workarounds), Hacker News (Algolia API; substantive comments, not announcements). Scout every run — highest signal. | `canonical` |
| 2 | **tier1-publishers** | Tier 1 open publishers (Simon Willison, Geoffrey Huntley, Armin Ronacher, Mitchell Hashimoto, Sid Bidasaria, Thariq Shihipar, Anthropic engineering blog). Open blogs — read first-hand. | `post` |
| 3 | **cc-team-x** | Tier 2 Anthropic Claude Code team (Boris Cherny, Cat Wu, Adam Wolff, Alex Albert) + Occasional (Gergely Orosz, swyx, Indragie Karunaratne). X-primary — best-effort, reblog/mirror-dependent. | `post` |
| 4 | **transferable** | Agentic-general / adjacent transferable voices (Thorsten Ball, Steve Yegge, Hamel Husain, Eugene Yan, Kent Beck, Thoughtworks "Exploring Gen AI", Drew Breunig). | `post` |
| 5 | **codex-openai** | Codex / OpenAI cluster (Tibo Sottiaux, Alex Embiricos, Peter Steinberger, OpenAI engineering blog). Keep only lessons that **transfer to Claude Code / general agentic coding**. | `post` |

Always read the tiers **from the file at run time** — the table above mirrors the
list as of authoring, but the file is the source of truth. If a new voice or tier has
been added, fold it into the nearest cluster.

### How each subagent searches

- **WebSearch first** to find recent posts: query the person's name + handle +
  "Claude Code" / "agents" / "Codex" plus recency terms (e.g. `simonwillison claude
  code 2026`). For blogs, search the site directly (e.g. `site:simonwillison.net
  claude code`). For canonical: fetch the CHANGELOG raw file, search GitHub issues
  (`site:github.com/anthropics/claude-code`), and hit the HN Algolia endpoint
  `https://hn.algolia.com/api/v1/search_by_date?query=claude%20code` for recent threads.
- **WebFetch** each promising URL to read the actual post and pull the exact quote.
  - **X/Twitter caveat:** direct `x.com` fetches are usually login-walled. X-only
    voices only land when the post is **reblogged, quoted, or mirrored** (e.g. on a
    blog, in an HN thread, or via a Nitter-style mirror). If you can't reach the
    original and can't verify a quote, **drop the candidate** — never fabricate a quote.
- **Public posts only** — no login-walled scraping; respect each platform's ToS.
- **Respect the recency cutoff.** Confirm each post's publish date; discard anything
  older than the window. Exception — the CHANGELOG has no per-entry dates: treat
  entries as newest-first and take versions not yet in the processed ledger (or, on a
  first run, the top-of-file versions), rather than trying to date them.
- **Self-dedupe.** Before returning a candidate, check it against the known-lesson
  titles/TL;DRs you were given. If it's clearly the same lesson, drop it.

### Candidate-return format (each subagent returns this, one block per candidate)

```
CANDIDATE
title: <imperative, specific lesson title>
category: <one of the 17 categories>
source_type: post | canonical
source_url: <exact URL of the post/page>
author: <name or "canonical: <source>">
published: <YYYY-MM-DD or best estimate + "approx">
quote: "<verbatim sentence from the source>"
tldr: <one-sentence takeaway>
why: <1–2 sentences on why it matters>
how: <1–2 sentences on how to apply it>
```

If a subagent finds nothing new in scope, it returns `NO NEW LESSONS` with a one-line
note on what it checked.

---

## Merge & write step (main session)

After all subagents return:

1. **Pool** every candidate.
2. **Cross-subagent dedupe.** Two subagents may surface the same lesson (e.g. a
   CHANGELOG entry and a blog post about it). Merge into one lesson; keep **all**
   distinct source URLs in the `sources:` list; prefer `source_type: canonical` if any
   source is canonical.
3. **Dedupe against the existing archive.** For each surviving candidate, compare its
   title + TL;DR against existing lessons in the same category:
   - **New topic** → write a new lesson file.
   - **Duplicate** of an existing active lesson (same claim) → **skip it**; note it in
     the report as "already covered by `<existing-id>`."
   - **Contradicts / updates** an existing active lesson (newer guidance on the same
     topic) → **write a new file** (never edit the old one), set the new file's
     `supersedes: <old-id>`, and mark the old file `status: superseded` with
     `superseded_by: <new-id>`. Newer wins. INDEX lists only `status: active`.
4. **Write each new lesson** using the format below. If a candidate overlaps an
   existing transcript lesson without contradicting it, prefer a `[[other-id]]`
   cross-reference over a near-duplicate file.
5. **Update `lessons/INDEX.md`** — add a bullet under the lesson's category heading
   (create the heading if the category is new to the index). Bullet format matches the
   existing index:
   `- [<Title>](<category>/<id>.md) — <TL;DR>.`
6. **Update `lessons/.processed-social.json`** — merge in every post URL the subagents
   examined this run (both accepted and rejected candidates), deduped and sorted. Keep
   it valid JSON; never drop existing entries. Skip this in `dry-run`.
7. **Do not touch `CLAUDE.md`.** Lessons live in the archive; promotion to CLAUDE.md
   is a separate, manual, curated step (per `lessons/README.md`).

### Lesson file format

Path: `lessons/<category>/<id>.md`, where `<id>` is a short kebab-case slug derived
from the title (unique within the archive).

```markdown
---
id: <kebab-case-slug>
created: <YYYY-MM-DD>            # today's date
status: active                  # active | superseded
supersedes: null                # id this replaces, or null
category: <one of the 17>
source_type: post               # post | canonical
sources:
  - <exact source URL>          # one or more; all distinct URLs for this lesson
---

# <Imperative, specific lesson title>

## TL;DR

<one-sentence takeaway>

## Why it matters

<1–3 sentences: the underlying reason this is worth doing>

## How to apply

<1–3 sentences: the concrete action, naming the exact command/flag/hook/pattern>

> "<verbatim quote from the source>" — <Author> (<source, if canonical>)
```

Notes on the format:
- `source_type: canonical` for anything from the Canonical / non-person tier
  (CHANGELOG, docs, GitHub issues, HN); `source_type: post` for a named person's post.
- Keep the quote **verbatim**. Attribute to the author; for canonical sources attribute
  to the source (e.g. "— Claude Code CHANGELOG 2.1.178").
- Add a `## Related` section with `[[other-lesson-id]]` links when a clear sibling
  lesson exists (optional, but preferred when obvious).

---

## Final report & self-check

End by reporting, in the main session's final message:

- **Sources scouted** per subagent and the recency window used.
- **Lessons written** — list `id`, category, and source_type for each new file.
- **Superseded** — any old lesson marked superseded and by which new one.
- **Skipped as duplicates** — candidate → existing lesson it duplicated.
- **Dead ends** — voices/sources that yielded nothing in window (esp. login-walled X
  voices), so the next run knows what was already checked.

Quality over coverage: when a post is borderline, drop it. A wrong or hallucinated
"lesson" is worse than a missing one. Maintain the voice list in
`references/agentic-coding-voices.md`.

Before declaring done, verify each item:

- [ ] `references/agentic-coding-voices.md` was read this run; tiers parsed from the
      file, not from memory.
- [ ] Every new lesson has a **verbatim quote** and a **real, fetchable source URL**.
- [ ] Every new lesson's `category` is one of the 17 and the folder exists.
- [ ] `source_type` is `canonical` for canonical-tier sources, `post` otherwise.
- [ ] No fabricated quotes; any candidate that couldn't be verified (e.g. login-walled
      X post) was **dropped**, not invented.
- [ ] Each new lesson passed the 4-part "what counts as a lesson" bar.
- [ ] Dedupe ran against the **existing archive**; no duplicate of an active lesson was
      written; contradictions were handled via supersession (new file + old marked
      superseded), never by editing the old file.
- [ ] `lessons/INDEX.md` has one new bullet per new active lesson, under the right
      category heading, and lists no superseded lessons.
- [ ] `lessons/.processed-social.json` now includes every post URL examined this run
      and is valid JSON.
- [ ] `CLAUDE.md` was not modified.
- [ ] In `dry-run`, nothing was written — the plan and candidates were reported instead.
