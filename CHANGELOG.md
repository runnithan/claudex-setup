# Changelog

## [Unreleased]

### Changed
- `/optimise` now maintains a central `projects/audit-log.md` tracker — force-created on first use and rewritten each run — so "when was each project last optimised" lives in one command-maintained place instead of drifting across per-project frontmatter and the registry README.

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
