# claudex-setup

[![validate](https://github.com/runnithan/claudex-setup/actions/workflows/validate.yml/badge.svg)](https://github.com/runnithan/claudex-setup/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Turn the [Claude Code](https://claude.com/claude-code) creators you follow into a lessons library your agent actually uses.**

You watch the tutorials, read the threads, star the gists — and the best tips evaporate.
`claudex-setup` is a Claude Code config you run yourself: it mines those tips into
**source-cited lessons from the creators *you* pick**, curates them, and audits your projects
against them — alongside a battle-tested set of slash commands, subagents, and hooks.

Keep it as a **standalone repo alongside your projects** — you run it *from* here, and
`/optimise` improves your other projects' Claude Code setups in place. You don't install it
into each repo. Point it at your favourite voices; make it yours.

> **Why "claudex"?** **Claude** Code + Co**dex**. The lessons library is Claude-Code-first, but
> `/optimise` audits whichever agent tools a project actually uses — its Claude Code setup by
> default, its Claude Design usage with `--design`, and its OpenAI Codex setup with `--codex` —
> keeping one tracker per tool.

## Quickstart (60 seconds)

It's a hub you run *from*, not a config you install into each project:

**Requirements:** Claude Code, [`uv`](https://docs.astral.sh/uv/), Python 3.x.

```bash
git clone https://github.com/runnithan/claudex-setup
cd claudex-setup && uv sync     # then open Claude Code here
```

```text
/extract-lessons            # mine your tracked creators into a lessons library
/optimise <your-project>    # audit another project's setup against those lessons, apply fixes
```

→ **Full walkthrough:** [`USER_GUIDE.md`](USER_GUIDE.md). Prefer the commands available
*inside* another repo? It's also a plugin: `/plugin marketplace add runnithan/claudex-setup`.

## Learn from the creators you pick

Most configs "improve themselves" from your own sessions. This one learns from the
practitioners you actually trust:

1. **Pick your sources** — drop creator video URLs in `transcripts/urls.txt`, or add voices
   to [`references/agentic-coding-voices.md`](references/agentic-coding-voices.md).
2. **Mine them** — `/extract-lessons` (YouTube transcripts) or `/extract-social-lessons`
   (X/blog posts, via a research subagent team) distil them into one-file-per-lesson markdown,
   each citing its source.
3. **Curate + apply** — `/consolidate-lessons` keeps the library lean; `/optimise <project>`
   audits a project's setup against it and applies the fixes you approve.

> **Example:** point it at Boris Cherny and Simon Willison and you get lessons like *"pre-compute
> context with inline bash in slash commands"* and *"clone a reference repo to /tmp"* — each
> linked to the post it came from. Browse [`lessons/INDEX.md`](lessons/INDEX.md) to see ~100
> already mined.

## Everything you can run

| Run… | …to |
|------|-----|
| `/extract-lessons` | mine Claude Code tips from YouTube transcripts you fetch |
| `/extract-social-lessons` | mine tips from practitioner posts (X, blogs) via a research subagent team |
| `/consolidate-lessons` | merge duplicate lessons and prune the archive |
| `/optimise <project>` | audit a project's setup against your lessons and apply fixes one at a time (`--design` audits Claude Design, `--codex` audits OpenAI Codex) |
| `/review-pr` | multi-agent review of a pull request |
| `/test [suite]` | run the project's tests / lint / build |
| `/pr`, `/ticket` | GitHub PR + Jira ticket flow [†](#pr-ticket-note) |
| `/fact-check` | verify claims in content against real sources |

<a id="pr-ticket-note"></a>† `/pr` and `/ticket` require the GitHub and Jira MCP servers (see [`.mcp.json.example`](.mcp.json.example)) and are **not bundled in the plugin** — they're available when you run the repo as a hub with those servers configured.

Plus subagents (`code-reviewer`, `qa`, `backend-dev`, `frontend-dev`, `code-simplifier`,
`pr-test-analyzer` — read-only roles tool-restricted), lifecycle hooks (an advisory security
reminder, a portable auto-formatter, GSD statusline/context-monitor), and skills
(`claude-md-improver`, `frontend-design`).

## Customising for your stack

The defaults lean toward a `backend/` (Python + `uv`) + `frontend/` (Node) layout, but the
commands read your project's real commands from `CLAUDE.md`, so it adapts. Tune `CLAUDE.md`
(your commands + conventions), `settings.json` (tool/secret rules), `hooks/auto-format.sh`
(formatters), and `agents/` (roles).

## Using it inside another project (advanced)

If you do want the config *in* a specific repo (via the plugin, or by copying it into `.claude/`):

- **The repo must become the `.claude/` folder itself** — `settings.json` references hooks as
  `.claude/hooks/…`, so copying it into a subfolder silently breaks them.
- **`settings.json` does not cascade** — each project needs its own copy.
- **Verify with `/hooks`** after copying. A single JSON typo in `settings.json` silently
  disables all hooks; the `validate` CI workflow catches malformed config.
- `settings.local.json` is gitignored (personal/machine overrides); shareable rules go in `settings.json`.

## Contributing, layout & versioning

Contributions welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). Directory tree:
[`references/project-structure.md`](references/project-structure.md). Changes are logged in
[`CHANGELOG.md`](CHANGELOG.md); releases are tagged `vX.Y.Z`.
