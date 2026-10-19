---
description: "Mine transcripts for discoveries: the tools, repos, MCP servers and products people pair with Claude Code and Codex, and the things they build with them. Keeps a verified catalogue for keeping up with the space, relevant to the owner or not. Counterpart to /extract-lessons, which keeps only how-to lessons."
argument-hint: "[new | <path-or-glob>]"
---

# /discover: what people use alongside these tools, and what they build

`/extract-lessons` keeps only lessons that change how the owner uses Claude Code, Claude Design
or Codex, so everything else a video shows is dropped. The 2026-10-13 video "I tried 100 GitHub
repos for Claude, these 6 are the best" yielded 4 lessons, and the list of repos itself
(Hyperframes, Google Workspace CLI, Humanizer, Scrollcraft, agent-skills) went nowhere. This
command keeps that layer: what exists, what it does, who showed it, and how often it comes up.
Relevance to the owner is not a filter; keeping up with the space is the point.

## What a finished run leaves behind

- `discoveries/catalogue.json` and the `discoveries/INDEX.md` rendered from it, holding every
  discovery once, verified where it can be, each citing the transcripts that mention it, with a
  `## Latest run` section naming what this run added or saw again.
- `discoveries/.processed.json` listing every transcript this run mined, zero-yield ones included.
- A report with exact counts.

Out of scope: lessons (that is `/extract-lessons`), web sources (transcripts only for now),
Claude Code and Codex built-in features (the changelog commands cover them), and judging whether
the owner should adopt anything.

## What counts

- **tool**: anything a person can install, run or sign up for that someone pairs with these
  tools: a GitHub repo, CLI, library, MCP server, plugin, skill pack, app or service.
- **use**: a concrete thing someone built or runs with these tools, such as an agent that manages
  ad campaigns or a content pipeline, with what it does and which tools it is built from.

Not a discovery: a passing name-drop with nothing said about it, generic AI news, or a feature of
Claude Code or Codex itself. A sponsor segment counts only if the video shows the tool in use, and
is marked sponsored.

## Hard rules

- **Never read transcripts in the main session.** Mining runs in subagents on the cheap or fast
  tier, about 10 transcripts each, at most 5 at once. This is an explicit request to delegate.
- **State only what the source states.** A miner records what the video says a thing does and
  quotes a short phrase from the transcript; it adds nothing from its own knowledge.
- **Verify every tool before it is listed.** Captions garble names, so confirm each tool exists and
  find its real URL: `gh repo view <owner>/<name>` when the owner is known, else
  `gh search repos "<name>" --limit 5 --json fullName,url,description`, or `curl -sIL` on its
  site. Match on what the description says it does, not on the name alone. A tool that cannot be
  confirmed is listed as `unconfirmed`, with the name as heard and no link; never guess a URL.
  GitHub search allows 30 requests a minute: on a rate-limit error, wait 60 seconds and retry.
- **The script owns the catalogue.** `scripts/discoveries.py` dedupes, counts, ledgers and renders;
  never edit `catalogue.json`, `INDEX.md` or `.processed.json` by hand. Merge each batch as it lands
  (`python3 scripts/discoveries.py merge --run <today> <batch.json>`): that writes its entries and
  ledgers its transcripts together, so an interrupted run resumes instead of re-mining, and a
  re-merged batch changes nothing.
- **Nobody retypes a miner's JSON.** Give miners a subagent type that can write files, have each
  write its JSON to `<scratchpad>/discover-batch-<n>.json` and reply with that path only; the
  quotes in it are evidence.

## Work list

`$ARGUMENTS`: empty or `new` mines every transcript `python3 scripts/discoveries.py pending` lists
(all transcripts not yet ledgered); a path or glob limits that to its scope. With no ledger yet,
`new` is the whole library: a backfill of over a thousand transcripts, run in waves, which an
interrupted run resumes from the ledger. If `transcripts/` holds no transcripts, stop and say so.

Each miner gets its transcript paths and the path to `discoveries/catalogue.json`, where it looks up
a tool already listed instead of searching GitHub for it again (the script does the deduping), and
writes JSON only:

```json
{"discoveries": [
  {"kind": "tool", "name": "Hyperframes", "as_heard": "hyper frames", "url": "https://github.com/...",
   "verified": true, "category": "design and media", "what": "renders video from HTML",
   "sponsored": false, "transcript": "transcripts/<creator>/<file>.txt", "quote": "..."},
  {"kind": "use", "name": "Agent that runs Google Ads accounts", "tools": ["Claude Code", "Google Ads API"],
   "category": "business and marketing", "what": "...", "transcript": "...", "quote": "..."}
 ],
 "processed": ["transcripts/<creator>/<file>.txt"]}
```

Categories, one per entry: `agent tooling` (skills, plugins, harnesses, orchestration), `mcp
servers`, `dev tools`, `design and media`, `data and research`, `business and marketing`,
`personal and productivity`.

## Check before merging

Before each merge, re-check every GitHub URL the batch marks verified (`gh repo view <owner>/<name>
--json description`) and `curl -sIL` every other site, and confirm the description fits what the
video said. Retry each unconfirmed name once with a different query. Correct the batch file by
script, never by retyping it: a wrong match goes to unconfirmed, a found one gets its URL, and two
spellings of one tool get one name. On 2026-10-19 the main session's re-check confirmed all 25
miner-verified repos and resolved 3 of 9 unconfirmed names (Whop, Impello, Hermes Agent).

The script merges a candidate into an existing entry when the URL matches (or, for unconfirmed
tools and for uses, the normalised name), adding its source and quote; a tool seen in several
videos is what is catching on. Sponsorship is recorded per video, so one sponsor read does not
label later unpaid mentions.

## Report

Exact counts from the merge output: transcripts mined, candidates, new tools (verified and
unconfirmed), new uses, entries seen again from earlier runs, how many names the re-check fixed,
and the 5 entries seen in the most videos overall.

## Self-check

- [ ] No transcript was read in the main session; no more than 5 subagents ran at once.
- [ ] Every listed tool has a verified URL or says `unconfirmed`; none carries a guessed link.
- [ ] Every batch was re-checked before its merge, and corrected by script, not retyped.
- [ ] `python3 scripts/discoveries.py pending` lists none of this run's work list afterwards.
- [ ] The report gives numbers, not adjectives.
