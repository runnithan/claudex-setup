# Lessons

Distilled, actionable improvements to Claude Code usage, extracted from transcripts in `transcripts/` by `/extract-lessons`.

## File layout

- `INDEX.md`, auto-maintained list of active lessons. Read this first.
- `<topic-slug>.md`, one file per discrete lesson topic.
- `.processed.json`, internal: tracks which transcripts have been processed so reruns skip them.

## Lesson file format

```markdown
---
id: parallel-tool-calls
created: 2026-04-25
status: active            # active | superseded
supersedes: null          # id of file this replaces, or null
sources:
  - transcripts/path/to/transcript.txt
---

# Lesson title

**TL;DR:** one-sentence takeaway.

## Why it matters
...

## How to apply
...
```

## Supersession rule

Newer lessons win. If `/extract-lessons` finds a lesson that contradicts an existing active lesson on the same topic, it writes a **new** file (so each run produces new lessons, not edits) and marks the old one `status: superseded` with a `superseded_by: <new-id>` field. The new file gets `supersedes: <old-id>`. `INDEX.md` only lists `status: active`.

## Consolidation

`/extract-lessons` only ever adds. Run `/consolidate-lessons` periodically to merge near-duplicate active lessons into one canonical file and prune dead `superseded` files, so the archive and `INDEX.md` stay signal-dense rather than growing unbounded. Use `/consolidate-lessons dry-run` to preview the plan first.

## Promoting lessons to CLAUDE.md

Lessons live here as a learning archive. When a lesson proves itself, manually copy the actionable rule into the relevant `CLAUDE.md` section so it loads into every session. Don't auto-promote, CLAUDE.md is curated.
