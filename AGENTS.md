# claudex-setup: Codex guide

Codex reads this file the way Claude Code reads `CLAUDE.md`. This repo is the **claudex** hub
(**Claude** Code + Co**dex**): you run it *from* here to mine agentic-coding lessons and to
audit your other projects' agent setups in place.

## CLAUDE.md is authoritative, read it first

**The working rules are shared between both tools and live in [CLAUDE.md](CLAUDE.md).** Read it
before touching anything. Architecture, the transcript→lessons pipeline, Conventional Commits and
the no-`Co-Authored-By` rule, CHANGELOG discipline, and the validation steps all live there and
apply to Codex verbatim. They are deliberately **not** restated here, because a second copy would drift,
which is exactly what this repo is built to prevent. If a convention changes, it changes in
`CLAUDE.md` only.

The short safety net below is the one deliberate exception. Codex reads `AGENTS.md` but does not
automatically read `CLAUDE.md`, so the rules where a miss is *catastrophic and unrecoverable* are
mirrored here, and only those, because they effectively never change. **If this file and
`CLAUDE.md` ever disagree, `CLAUDE.md` wins.**

- **Never commit secrets.** `.env` files, private keys, and service-account JSON stay gitignored.
- **Public mirror + leak-gate.** This private repo publishes a sanitized public mirror via
  `scripts/publish.sh`, which strips `projects/`+`transcripts/`, freezes the public lesson set,
  and hard-fails on any leak. Run `bash scripts/publish.sh` (dry run) before publishing.
- **Never name a private project in `CHANGELOG.md`**: it is *not* in the scrub set, so a private
  name written there fails the leak gate. Describe the feature, not the project.

## Codex-specific notes

- **This repo's Codex config surface** is exactly what `/optimise --codex` inventories anywhere
  else: this `AGENTS.md`, a project `.codex/` directory (none here yet), and the relevant
  `~/.codex/config.toml`. Adding a new top-level file? It must also be added to the `ALLOWED`
  path allowlist in `scripts/publish.sh`, or publishing hard-fails by design.
- **Tracked Codex usage** lives in the registry: a multi-tool project gets a `projects/<slug>/codex/`
  sub-area (its own `current.md` / `improvements.md` / `applied-improvements.md` / `habits.md`),
  audited by `/optimise <slug> --codex` and keyed `<slug>/codex` in `projects/audit-log.md`.
- **Honest scope.** The lessons library is Claude-Code-first: `/extract-social-lessons` mines a
  Codex/OpenAI voice cluster, but keeps only lessons that transfer to general agentic coding.
  Codex is first-class in what this repo **audits and tracks**, not in what it ships. The slash
  commands and hooks are Claude Code artifacts and run there.
