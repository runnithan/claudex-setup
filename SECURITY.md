# Security

This repo is a portable Claude Code configuration: agents, commands, hooks,
skills, and the transcript→lessons tooling. It's a standalone hub you run from
(and can optionally adopt into a project's `.claude/`). The notes below describe
how this config is built to be safe and how the public mirror is kept clean.
They are specific to this repo — nothing here invents a process that doesn't exist.

## Permission model

`settings.json` defines an allow/deny permission policy that travels with the
config:

- **Allow list** — narrowly scoped commands and MCP tools that are safe to run
  without a prompt (e.g. `Bash(git *)`, `Bash(npm run *)`, `Bash(uv run *)`,
  read-only Atlassian/GitHub MCP calls, `WebSearch`). Everything not listed still
  prompts.
- **Deny list** — blocks reading and editing of credentials regardless of what
  any agent or command asks for. This covers `.env` files (`**/.env`,
  `**/.env.*`, plus the explicit `backend/.env` / `frontend/.env`), private keys
  (`**/*.pem`, `**/*.key`, `**/*.p12`, `**/id_rsa`), `**/.ssh/**`, `**/.aws/**`,
  and service-account JSON (`**/*service-account*.json`,
  `firebase-service-account.json`). Destructive `git push --force` / `-f` is also
  denied.

Deny rules take precedence over allow rules, so an agent cannot read a secret
even if a broader allow pattern would otherwise permit it.

## Hooks

Hooks in `hooks/` are wired through `settings.json`. They are **advisory by
default**: the security reminder hook (`hooks/security_reminder_hook.py`) surfaces
warnings for risky patterns (`eval(`, `dangerouslySetInnerHTML`, `document.write`,
`innerHTML =`) on `Edit`/`Write`/`MultiEdit` but **exits 0 so the edit proceeds**.
Blocking is opt-in via the `SECURITY_HOOK_BLOCK=1` environment variable, which
makes a match hard-block with `exit 2`. The formatting hook
(`hooks/auto-format.sh`) is tool-guarded and always exits 0, so a missing
formatter never blocks an edit.

Why advisory: a guardrail that blocks legitimate edits gets disabled, which is
worse than no guardrail. The exit-code contract that makes this work — `exit 2`
blocks, `exit 1` does *not* — is documented in
[references/hooks-gotchas.md](references/hooks-gotchas.md). Note also that a
single JSON syntax error in `settings.json` silently disables *all* hooks; the CI
`validate` workflow catches malformed JSON.

## Data & privacy

- `transcripts/` holds locally fetched YouTube transcripts used as input to
  `/extract-lessons`. They are working inputs only and are **not published**.
- `projects/` holds private per-project working data and is **not published**.
- Neither tree ships to the public mirror (see below).

## Public / private split

The public showcase repo is a sanitized snapshot of a private source-of-truth
repo, built by `scripts/publish.sh`, which:

- exports the tracked tree (`git archive HEAD`) to a temp dir — the private repo
  is never modified;
- strips personal trees (`projects/`, `transcripts/`), the publish script itself,
  and any `settings.local.json`;
- scrubs personal specifics (org/repo/Jira prefixes, machine paths, usernames)
  out of a handful of command and task files;
- **hard-fails** if any forbidden pattern survives the scrub, so nothing is
  published when a leak is detected;
- pushes only with `--push`, as a normal commit on top of the public history (no
  private commits are ever exposed).

The public repo's `main` is **branch-protected** (no force-push, no deletion).

## Reporting a security issue

Found a leaked secret in the public mirror, or a problem with these protections?
Use [GitHub's private vulnerability reporting](https://docs.github.com/code-security/security-advisories/working-with-repository-security-advisories/privately-reporting-a-security-vulnerability)
on the public repository (Security → Report a vulnerability) rather than opening a
public issue. Please do not include the leaked credential itself in the report.
