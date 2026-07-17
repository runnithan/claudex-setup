# Contributing

Thanks for wanting to improve claudex-setup. Commands, subagents, hooks, skills, and
lessons are all welcome.

## Ground rules

- **Keep it portable.** Anything you add should work in a fresh project, not just yours.
  Read project commands from `CLAUDE.md` rather than hardcoding a stack; guard shell tools
  with `command -v`; use repo-relative or `$CLAUDE_PROJECT_DIR`-anchored paths in hooks.
- **No personal data.** No real names, emails, machine paths, private repo/org/project names,
  or secrets — in files *or* commit messages.
- **Keep it lean.** A focused, well-described command beats ten vague ones. `CLAUDE.md` and
  `SKILL.md` files stay under ~200 lines; push detail into referenced files.

## Adding things

- **Slash command** → `.claude/commands/<name>.md` with a `description:` frontmatter line.
  Add `disable-model-invocation: true` for side-effecting commands you only want run manually.
  Register it in `.claude-plugin/plugin.json` `commands` if it should ship in the plugin.
- **Subagent** → `agents/<name>.md` with `name`/`description`/`tools`/`model` frontmatter.
  Give read-only roles (reviewers, QA) a restricted toolset (`Read, Bash, Glob, Grep`).
- **Hook** → a script in `hooks/`, wired in `settings.json`. Exit `2` to *block*, `0` to allow
  (exit `1` is a silent no-op — see `references/hooks-gotchas.md`). Keep hooks fast and
  degrade gracefully.
- **Skill** → `skills/<name>/SKILL.md` with frontmatter and progressive disclosure.
- **Lesson** → don't hand-place these; they come from `/extract-lessons` /
  `/extract-social-lessons` and are curated by `/consolidate-lessons`. See `lessons/README.md`.

## Before you open a PR

- Run `bash scripts/publish.sh` (build + verify) or rely on the `validate` CI workflow — it
  JSON-checks settings/manifests and syntax-checks shell/python/node hooks.
- **Commits follow [Conventional Commits](https://www.conventionalcommits.org):**
  `<type>(<scope>): <subject>` — imperative, lowercase, no trailing period. Types: `feat`,
  `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- PRs target `main`. Keep them focused; explain the *why* in the description.
