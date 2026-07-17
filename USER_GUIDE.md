# User Guide

How to actually operate `claudex-setup` day to day. New here? Start with the
[README](README.md) quickstart; this guide goes deeper on each piece.

## Contents
- [Install](#install)
- [The lessons pipeline](#the-lessons-pipeline) — the core workflow
- [Commands](#commands)
- [Subagents & agent teams](#subagents--agent-teams)
- [Hooks](#hooks)
- [Customising for your stack](#customising-for-your-stack)
- [Troubleshooting](#troubleshooting)

## Install

**Use it as a standalone supporting repo — don't install it into your projects.** claudex-setup
is a hub you run *from*: you mine lessons here, and `/optimise` reaches out to improve your
*other* projects' Claude Code setups in place.

```bash
git clone https://github.com/runnithan/claudex-setup
cd claudex-setup
uv sync          # Python deps for the lessons pipeline (youtube-transcript-api)
```

Then open Claude Code in this folder and run the loop (below). Register each project you want
to improve as a folder under `projects/<name>/` with a `path:` to its real location on disk.

> Prefer having the individual commands available *inside* another repo's session? It's also
> published as a plugin (`/plugin marketplace add runnithan/claudex-setup`) — but that's the
> exception; the standalone-hub model above is the recommended way.

## The lessons pipeline

The loop this config is built around — and the recommended way to use it: **mine lessons
from creators you choose with `/extract-lessons`, then apply them to your projects with
`/optimise`.** Everything else supports those two steps.

**1. Pick your sources.**
- *YouTube:* add video URLs to `transcripts/urls.txt`, one per line, under a `# Creator Name`
  heading. Adding the heading + one URL is enough — `scripts/update_urls.py` discovers that
  channel's newer uploads automatically via its RSS feed (Shorts are filtered out).
- *Posts:* edit [`references/agentic-coding-voices.md`](references/agentic-coding-voices.md) — the
  list of practitioners whose X/blog posts `/extract-social-lessons` scouts.

**2. Fetch transcripts.** Run `uv run python scripts/run_pipeline.py` (discovers new videos +
fetches transcripts into `transcripts/<creator>/`). It caps fetches per run and spaces them to
avoid YouTube throttling; just run it again to drain a backlog. Videos with no captions are
recorded in `transcripts/no-transcript-available.md` and skipped thereafter.

**3. Mine lessons.**
- `/extract-lessons` — distils new transcripts into one-file-per-lesson markdown under
  `lessons/<category>/`, indexed in `lessons/INDEX.md`. Each lesson cites its transcript.
- `/extract-social-lessons` — a research subagent team mines recent posts from your voices
  into the same library (tagged `source_type: post`, citing the post URL).

**4. Curate.** `/consolidate-lessons` merges near-duplicate lessons and prunes stale ones, so
the archive stays signal-dense. Run `/consolidate-lessons dry-run` to preview first.

**5. Apply to your projects — the payoff.** `/optimise <project>` audits a project's Claude
Code setup against your accumulated lessons and walks you through the improvements one at a
time, applying the ones you approve — editing that project's `.claude/` in place. Register
each project as `projects/<name>/` (with a `path:` to its real location; the command creates
its tracking files on first use). This is the main way to fold lessons back into real work.
For a single high-value rule you can also promote it into a `CLAUDE.md` by hand — kept
deliberate, since `CLAUDE.md` loads every turn. See [`lessons/README.md`](lessons/README.md).

> **Tip — what `/optimise` keeps per project.** Each `projects/<name>/` folder builds up a
> small set of files so audits compound instead of starting from scratch. `/optimise`
> maintains them for you:
> - **`current.md`** — a factual snapshot of that project's Claude Code setup, so the next
>   audit diffs against it instead of re-investigating from zero.
> - **`improvements.md`** — the *open* backlog: which lessons apply to this project and why.
> - **`applied-improvements.md`** — the ledger of what's already been done, so `/optimise`
>   stops re-suggesting it (it moves items here once applied).
> - **`habits.md`** — recommendations that are *yours* to do at the keyboard (a command to
>   type, a discipline to keep) rather than a config change Claude can make — kept as a
>   prioritised list so they don't clutter the config backlog.
> - **`optimise.md`** — a transient *run scratchpad* (gitignored). `/optimise` flushes this
>   run's freshly suggested improvements here before walking them, so if you stop partway they
>   aren't lost — the file is deleted when the run finishes cleanly, and a leftover one just
>   means the next run resumes where you left off. You never touch it.
>
> **Multi-tool projects.** If you build a project with more than one agent tool — say Claude
> Code, Claude Design *and* OpenAI Codex — its `projects/<name>/` can split into per-tool
> sub-areas (`claude-code/`, `claude-design/`, `codex/`), each with its own `current.md` /
> `improvements.md` / `applied-improvements.md`. `/optimise <name>` audits the Claude Code area
> as usual; `/optimise <name> --design` audits the Claude Design area — a hand-maintained
> snapshot, since that tool has no `.claude/` to inventory (and no `habits.md`, a CLI-only
> concept); `/optimise <name> --codex` audits the Codex CLI setup (`AGENTS.md` / `.codex/` /
> `~/.codex/config.toml`, with its own `habits.md`). Projects that use only Claude Code stay
> flat; there's nothing to change.
>
> Across all projects, `/optimise` also maintains one rollup file:
> - **`projects/audit-log.md`** — a single table of every registered project with its status
>   and when it was last optimised. The command force-creates it on first use and rewrites the
>   audited project's row each run, so "when did I last tune project X?" lives in one place
>   instead of drifting across files.
>
> You don't create any of these by hand; `/optimise` writes the snapshot, folds new lessons
> into the backlog, moves done items to the ledger, routes keyboard-habit items to `habits.md`,
> and updates the audit log.

## Automate it (recommended)

Run the whole loop on a schedule so your lessons stay current without you thinking about it.

**Fetch transcripts daily.** The pipeline has a 24h gate and a per-run cap, so a *daily*
trigger is ideal — running more often just risks YouTube throttling the IP.
- *macOS / Linux* — `crontab -e`, then:
  ```cron
  0 9 * * * cd /path/to/claudex-setup && uv run python scripts/run_pipeline.py
  ```
- *Windows* — the repo ships `scripts/install_scheduled_task.ps1`; edit the path/user
  placeholders, then run it once to register a Task Scheduler job (login + hourly trigger,
  gated to ~once a day).

**Extract lessons on a schedule (headless Claude Code).** The slash commands run
non-interactively via `claude -p`, so you can schedule them too. Mining is token-heavy, so
*weekly* is plenty — and run it after the transcripts are fresh:
```cron
# Mondays 10am: mine new transcripts, then tidy the archive
0 10 * * 1 cd /path/to/project && claude -p "/extract-lessons" && claude -p "/consolidate-lessons"
```
The same works for posts — `claude -p "/extract-social-lessons"` — but schedule it less often
(it spawns a research subagent team and uses more tokens). Add voices to
[`references/agentic-coding-voices.md`](references/agentic-coding-voices.md) first.

> Headless runs can't answer permission prompts, so configure auto mode or an allowlist for
> non-interactive use (see `lessons/permissions/`). Claude Code also has built-in scheduling
> (`/schedule` routines, `/loop`) if you'd rather not touch the OS scheduler — see
> `lessons/automation/`.

**Keep promotion manual.** Automate the mining and curation, but review the new lessons and
copy the keepers into `CLAUDE.md` yourself — that judgement step shouldn't be on a cron.

## Commands

**Lessons**
- `/extract-lessons [new|all|<path>]` — mine transcripts (default: only unprocessed).
- `/extract-social-lessons [new|all|<name>]` — mine practitioner posts.
- `/consolidate-lessons [dry-run|<category>]` — merge/prune the archive.

**Project audit**
- `/optimise <project>` — audit a tracked project's Claude Code setup against your lessons and
  apply improvements one at a time with your approval. Project notes live under `projects/`. Add
  `--design` to audit a project's Claude Design area instead (for projects you build with both
  tools; see the multi-tool note above).

**Review & ship**
- `/review-pr` — multi-agent PR review. `/test [suite]` — run the project's tests/lint/build
  (reads the commands from your `CLAUDE.md`). `/pr`, `/ticket` — GitHub + Jira flow.
- `/fact-check` — verify claims in content against real sources.

## Subagents & agent teams

Subagents live in `agents/`. Read-only roles (`qa`, `code-reviewer`) are restricted to
`Read/Bash/Glob/Grep` so they can't modify code. For multi-ticket or full-stack work, your
main session acts as the **team-lead** — the coordinator role that creates tickets and
branches, reviews diffs, and merges — while spawning the dev/QA subagents (`backend-dev`,
`frontend-dev`, `qa`) to do the work. There's no `team-lead.md` to spawn; it's the role you
play. See the **Agent team guidance** in `CLAUDE.md`. Reserve teams for divisible, high-value
work: parallel agents trade tokens (and your review attention) for wall-clock speed.

## Hooks

Wired in `settings.json`, scripts in `hooks/`:
- **Auto-format** (PostToolUse) — formats the edited file with whatever formatter is available;
  tool-guarded, so it's a safe no-op where a formatter is absent.
- **Security reminder** (PreToolUse) — *advisory* by default (warns on `eval`, `innerHTML`,
  etc. but doesn't block). Set `SECURITY_HOOK_BLOCK=1` to make matches block.
- **GSD hooks** — statusline, context monitor, update check.

Editing hooks? Read [`references/hooks-gotchas.md`](references/hooks-gotchas.md) first — exit
`2` blocks, exit `1` is a silent no-op, and a JSON error in `settings.json` silently disables
*all* hooks (run `/hooks` to verify).

## Customising for your stack

The defaults assume a `backend/` (Python + `uv`) + `frontend/` (Node) layout, but the commands
read your real commands from `CLAUDE.md`, so it adapts:
- `CLAUDE.md` — document your test/lint/build commands and conventions (commands read these).
- `settings.json` — `allow`/`deny` rules for your tools and secret paths.
- `hooks/auto-format.sh` — formatters per file extension.
- `agents/` — adjust subagent roles to your stack.

## Troubleshooting

- **Hooks not firing** → run `/hooks`. A single JSON typo in `settings.json` disables them all;
  the `validate` CI workflow catches malformed config.
- **Transcripts not fetching / "blocked"** → YouTube is throttling the IP. The fetcher backs
  off and retries next run; keep runs spaced (see `references/transcript-fetch-throttling.md`).
- **A command didn't load** → if installed as a plugin, commands are namespaced
  (`/claudex-setup:<name>`); via copy they're plain (`/<name>`).
- **`/extract-social-lessons` returns little** → it leans on what web search surfaces; voices
  with open blogs (see the list) yield more than X-only ones.
