# Changelog

## [Unreleased]

### Added
- **5 new lessons** from the 8 pending Jul-10 transcripts (a new creator, `simon-scrapes`, plus austin-marchese and sean-kochel; four Fable-5-vs-GPT-5.6 model-comparison videos yielded nothing in scope): `/goal`'s ~4k-char limit (reference a spec file instead of pasting), a privacy "quiet mode" env-var bundle for confidential work, clone-the-real-reviewer skills, prove-a-process-as-a-hand-run-skill-before-automating, and a max-effort-plateaus-at-high finding that was **merged** with the existing `effort-control-for-token-intensive-work` lesson into one balanced model-selection lesson superseding it (keeps the match-effort-to-risk core, corrects the top end: high not max on capable models). Lesson library now ~401 active.
- **36 new lessons** from the Jul 3–6 transcript fetch backlog (77 transcripts: mark-kashef ×46, sean-kochel ×21, plus 10 mixed), extracted via 6 parallel Explore miners deduped against the ~250 active lessons — highlights: Fable-5 strong-model-for-cheaper-executor tactics (war-game plans, golden references, load-bearing refactor, JSONL behavior playbook), the dynamic-workflows pairwise tournament, OpenSpec/DeepSec/Compound-Engineering/Open-Design tools, and skill-hygiene (cold-trigger test, wrong-primitive question, PreCompact context re-injection). New lessons are private by default (public set stays frozen). Lesson library now ~398 active.
- Agentic Coding School transcript source: 314 course-video transcripts pulled via the platform's official MCP (`agentic-coding-school` `get_video`) into `transcripts/ray-amjad-agentic-coding-school/` (private — stripped from the public mirror), and **166 new lessons** extracted from them via a 10-miner → synthesis → 7-adversarial-reviewer pipeline (lesson library now ~363 private / 197 public).

### Changed
- The three lessons-pipeline / audit commands rewritten as explicit step-by-step procedures with final self-checks, folding in the improvements from a skill-format rebuild while keeping all existing behaviour: `/extract-lessons` gains repo-root resolution, a fresh-start library scaffold, exclusion of non-transcript `.txt` seed files, parallel batched Explore miners for large backlogs (mining still never enters the main context), an exact lesson-file format with `## Related` wikilinks, and incremental INDEX updates that preserve the other run footers; `/extract-social-lessons` gains named per-cluster subagents with search budgets, a configurable recency window, tier/voice filters, a `dry-run` mode, and a verbatim-quote-or-drop bar; `/optimise` gains explicit area/mode resolution (including offering to scaffold a missing design sub-area or register an unknown project), an exact audit-log skeleton, a config-vs-habit routing rule, an exact-preview requirement for apply dialogs, and a registry field reference.
- `publish.sh` now **freezes the public lesson set**: only lessons listed in `scripts/public-lessons.allowlist` (the pre-existing ~197) ship to the public mirror, with a frozen public `INDEX.md` + `.processed.json`; newly extracted lessons are private by default, so the public set stays a showcase of `/extract-lessons` output without growing.
- `/optimise` now maintains a central `projects/audit-log.md` tracker — force-created on first use and rewritten each run — so "when was each project last optimised" lives in one command-maintained place instead of drifting across per-project frontmatter and the registry README.
- `/optimise` now supports **multi-tool projects**: a tracked project's folder can hold per-tool sub-areas (`claude-code/`, `claude-design/`), each with its own `current.md` / `improvements.md` / `applied-improvements.md`. `/optimise <project>` audits the Claude Code area (unchanged behaviour); the new `--design` flag audits the Claude Design area — a hand-maintained snapshot, since Claude Design has no `.claude/` to inventory (and no `habits.md`, a CLI-only concept). Single-tool projects keep the flat layout unchanged; the audit log gets one row per sub-area, keyed `<slug>/<tool>`. Documented in the USER_GUIDE and README.

### Fixed
- Transcript fetcher now defeats YouTube's per-IP caption-endpoint throttle by replaying a real Chrome TLS handshake: `fetch_transcripts.py`'s HTTP client swapped from plain `requests` to `curl_cffi` with `impersonate="chrome"`. Added `curl-cffi` to the dev deps (`pyproject.toml`, `uv.lock`) and the `.venv-linux` create command. Applied after pacing alone stopped clearing the flag (three consecutive zero-fetch runs); smoke-tested clean on the throttled IP. See `references/transcript-fetch-throttling.md`.
- Transcript titles/creators scraped from YouTube's embedded JSON are now decoded (JSON string escapes + HTML entities) before use, so filenames and `index.md` show real characters instead of raw escape sequences (e.g. an ampersand rendered as a literal backslash-u-0026).

## [0.2.0] - 2026-06-21

Hardening, safety, and a richer lessons pipeline.

### Added
- `SECURITY.md` documenting the permission model, advisory hooks, data/privacy boundaries, and the sanitized public-mirror split.
- Canonical non-person sources tier for `/extract-social-lessons` — it now also mines the Claude Code changelog, docs, `anthropics/claude-code` GitHub issues, and Hacker News (tagged `source_type: canonical`).
- More agentic-coding voices to mine (Kent Beck, Thoughtworks "Exploring Gen AI", Drew Breunig, Thorsten Ball, Steve Yegge, Hamel Husain, Eugene Yan).
- 16 new lessons (library now ~116), including the first batch grounded in the official changelog/docs.
- `scripts/validate-artifacts.py` and a `tests/` suite; CI now validates agent/skill/command frontmatter + plugin manifests, runs the unit tests, and runs a public-mirror **leak-gate** on every push/PR.
- A `/optimise` per-project files explainer in the USER_GUIDE, plus README license/requirements badges.

### Changed
- `publish.sh` is now a durable guard: a publishable-path **allowlist** (a new private tree hard-fails instead of shipping), a shared `forbidden-patterns.txt`, and an rsync-free push path.
- Docs reframed to the standalone-hub model; clarified that `team-lead` is the main-session role, not a spawnable agent.
- Consolidated the lessons archive (merged a duplicate parallel-session lesson).

### Fixed
- Pipeline reliability: `.last_run` now stamps on success (a crash no longer burns the 24h retry window), discovery is guarded, transcript filenames are collision-free.
- Closed a permission gap (`cat` on `.env`/keys is now denied) and hardened hooks (portability, version-compare, statusline).
- Extractor commands degrade gracefully on a standalone/plugin install (missing `lessons/` or source list).
- Scrubbed a stray name and template scaffolding from public-facing files.

## [0.1.0] - 2026-06-21

Initial public release — a portable Claude Code configuration.

- Slash commands for everyday work: `/extract-lessons`, `/extract-social-lessons`, `/consolidate-lessons`, `/optimise`, `/test`, `/review-pr`, `/pr`, `/ticket`, `/fact-check`, and Ralph-loop helpers
- Subagents (`backend-dev`, `frontend-dev`, `qa`, `code-reviewer`, `code-simplifier`, `pr-test-analyzer`), with read-only roles tool-restricted
- Lifecycle hooks: an advisory security reminder, a portable auto-formatter, and GSD statusline / context-monitor / update-check
- Skills: `claude-md-improver` and `frontend-design`
- A lessons library of actionable Claude Code tips, grown from practitioner content via `/extract-lessons` (transcripts) and `/extract-social-lessons` (posts), and curated with `/consolidate-lessons`
- Installable as a plugin marketplace (`/plugin marketplace add runnithan/claude-setup`), or copy the repo into a project's `.claude/`
- CI workflow validating settings, plugin manifests, and hook syntax
- A curated `CLAUDE.md` plus reference docs covering integrations, structure, and hook gotchas
