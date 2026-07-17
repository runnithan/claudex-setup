# claudex-setup

Portable Claude Code configuration for bootstrapping project-local agent instructions, commands, hooks, plugins, skills, and reference material.

## Architecture

- **Library docs**: Context7 MCP is available for fetching up-to-date package documentation when training data may be outdated. GSD agents use it; available for general use too.

## Project structure

See [references/project-structure.md](references/project-structure.md) for the full directory tree.

- **Transcript → lessons pipeline**: YouTube transcripts land in `transcripts/` (fetched by the `YouTube URL Updater` scheduled job, scripts in `scripts/`). Run `/extract-lessons` (`.claude/commands/extract-lessons.md`) to mine them into one-file-per-lesson under `lessons/<category>/`, indexed in [lessons/INDEX.md](lessons/INDEX.md) and dedup-tracked by `lessons/.processed.json`. Don't hand-place lessons or copy lesson content into CLAUDE.md — per `lessons/README.md`, CLAUDE.md stays curated (promote a proven rule manually).

## Workflow

- PRs target `main`.
- **Commit messages follow [Conventional Commits](https://www.conventionalcommits.org):** `<type>(<optional scope>): <subject>` — imperative mood, lowercase subject, no trailing period. Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Use the body to explain *why*; add a `BREAKING CHANGE:` footer for incompatible changes. Examples: `feat(transcripts): add daily fetch job`, `docs(projects): add entries index`, `fix(fetch): cap runs to avoid YouTube throttle`.
- Commits are authored solely by the repository owner — omit Co-Authored-By lines. This preserves clean authorship in the public commit history.
- After merging a PR, the feature branch auto-deletes (repo setting).
- **Keep `CHANGELOG.md` current — don't let it drift.** Any user-facing change (new/changed commands, agents, skills, hooks, pipeline behaviour, safety/permission changes, notable lessons-pipeline additions) gets a [Keep a Changelog](https://keepachangelog.com) entry (Added/Changed/Fixed) *in the same change* — not batched up "later." On release, bump the version in `CHANGELOG.md`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json` together.
- **Write CHANGELOG entries generically — never name a private project in them.** `CHANGELOG.md` is **not** in `publish.sh`'s scrub set (unlike `.claude/commands/optimise.md` / `references/project-structure.md`, where private project names are auto-genericized), so a private name written here is *not* scrubbed and the public leak-gate hard-fails the publish on it. Describe the feature, not the project that prompted it — e.g. `/optimise <project> --design`, not the real project name.

## Key conventions

- **IMPORTANT — never commit secrets.** `.env` files, private keys, and service-account JSON stay gitignored. Committing these would expose credentials in a public repo.
- **IMPORTANT — public mirror & branch protection.** The public repo (`runnithan/claudex-setup`) is published from this private repo via `scripts/publish.sh`, which strips `projects/`+`transcripts/`, **freezes the public lesson set** (only lessons in `scripts/public-lessons.allowlist` ship — the pre-existing ~197 stay public as a showcase of `/extract-lessons`; newly extracted lessons are private by default, with a frozen public `INDEX.md`/`.processed.json`), scrubs personal specifics, and hard-fails on any leak. To publish a *new* lesson, add its path to the allowlist and its bullet to `scripts/public-lessons-INDEX.md`. The public `main` is **branch-protected** (no force-push, no deletion). Routine publishing (`bash scripts/publish.sh --push`) uses a **normal push** and is unaffected. A history **rewrite** (e.g. scrubbing a leaked term out of past commits) requires a **force-push**, so you must first lift protection (`gh api -X DELETE repos/runnithan/claudex-setup/branches/main/protection`), force-push, then re-enable it — see the header comment in `scripts/publish.sh` for the exact re-enable command.

## Working with code

- Before modifying a file, read the entire file and its imports/dependencies. Code often has implicit contracts with surrounding modules — reading broadly prevents breaking them.
- When editing multiple files, complete all changes to one file before moving to the next. Parallel edits to interdependent files can introduce inconsistencies (e.g., mismatched imports, type signatures, or API contracts).
- When investigating a bug, trace the full call chain before proposing a fix. Surface-level patches often miss the root cause.
- After ~2 failed correction attempts on the same problem, `/clear` or `/rewind` rather than pushing on. Continuing against polluted context compounds the error instead of fixing it.
- After completing a multi-file coding task, consider running the code-simplifier agent for clean, consistent output.
- Use subagents for isolated side-effect tasks (formatting, verification). Keep context-building work (investigation, architecture) in the main session.
- When spawning a subagent, include a specific purpose ("why") in the system prompt. This helps the subagent filter signal from noise and avoids overlapping results when multiple subagents run in parallel.

## Validation

This repo has no application build; "validation" means the config artifacts are well-formed and nothing private leaks to the public mirror. Before reporting done:

- `python scripts/validate-artifacts.py` — checks agent/skill/command frontmatter and the plugin manifests parse with required keys.
- `bash scripts/publish.sh` (dry run, no `--push`) — builds the sanitized public snapshot and HARD-FAILS if any personal pattern would leak. Always run this before publishing.
- The `validate` GitHub workflow (JSON/shell/Python/Node syntax + artifact + leak checks) gates every push and PR.
- If a check fails, fix the issue before reporting the task as done.

## Agent team guidance

### Integrations (Jira + GitHub)

See [references/integrations.md](references/integrations.md) for MCP tool names, usage examples, and the Jira+GitHub workflow.

### When to use solo vs sub-agents vs agent teams

- **Solo**: Single-file changes, quick fixes, research, debugging.
- **Sub-agents**: Independent parallel queries, context isolation, verification tasks. Use for side effects, not context gathering.
- **Agent teams**: Multi-ticket work, cross-cutting backend+frontend features, coordinated releases.
- **Cost**: parallel sub-agents/teams trade tokens — and your review attention — for wall-clock speed; a multi-agent run can burn roughly an order of magnitude more tokens than a single agent. Reserve them for divisible, high-value work; don't fan out trivial or tightly-coupled tasks.
- **Permissions principle**: Read-only agents (QA, reviewers) should have restricted tool access (Read/Bash/Glob/Grep only, no Write/Edit). This prevents accidental modifications and makes their role clear.

### Agent team defaults

Default team structure for multi-ticket work. The **team-lead is the role your main session plays** (the coordinator) — it is *not* a spawnable subagent and has no file in `agents/`; the dev/QA rows below are the actual spawnable agents:

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **team-lead** *(main session)* | Coordinator | Creates Jira tickets, creates branches, reviews diffs, creates/merges PRs, transitions Jira statuses, resolves merge conflicts |
| **backend-dev** | Backend engineer | Code changes, backend tests, commits and pushes branches |
| **frontend-dev** | Frontend engineer | UI code changes, lint/build verification, commits and pushes branches |
| **qa** | QA engineer | Runs tests, lint, and build checks. Validates PRs before merge. Reports failures to team lead. |

- Spawn **backend-dev only** for backend-only work (no frontend changes).
- Spawn **frontend-dev only** for frontend-only work (no backend changes).
- Spawn **both** for full-stack features where backend and frontend need coordinated changes.
- Spawn **qa** alongside dev agents when multiple tickets are in flight, to validate work in parallel.
- The user can override the team structure by specifying agents and roles before work begins.
- Dev agents work in worktrees to avoid conflicts with each other and the team lead.
- Each ticket gets its own branch and PR. Team lead rebases branches onto main before merging.
