# Hook gotchas

Mechanics that silently break Claude Code hooks. The hooks in this repo
(`hooks/`, wired in `settings.json`) follow these; check them when editing.

## Exit codes are the contract

- **Exit 0**: success. stdout is shown in the transcript (and fed back to Claude
  for `UserPromptSubmit`/`SessionStart`).
- **Exit 2**: *blocks* the action. For `PreToolUse`, the tool call is denied and
  stderr is shown to Claude. This is the only "stop it" signal.
- **Any other non-zero (incl. exit 1)**: a *non-blocking* error. The hook's
  warning prints, but the action proceeds anyway. **A guard that `exit 1`s looks
  like it works and enforces nothing**, the most common hook bug. Use `exit 2`
  to actually block (see `security_reminder_hook.py`, which is advisory `exit 0`
  by design and only blocks under `SECURITY_HOOK_BLOCK=1`).

## A JSON error disables *all* hooks

A single syntax error in `settings.json` silently disables the entire `hooks`
block, no warning. After editing, run `/hooks` in Claude Code to confirm they
loaded, and rely on the `validate` CI workflow to catch malformed JSON.

## Portability & safety

- Reference scripts by `${CLAUDE_PROJECT_DIR}`-anchored or repo-relative paths
  that resolve once the repo is the project's `.claude/` (see README install
  contract). Hooks here use `.claude/hooks/…`, which only works because the repo
  *becomes* `.claude/`.
- Formatting/lint hooks must degrade gracefully: guard tools with `command -v`,
  keep them fast, and `exit 0` so a missing formatter never blocks an edit.
- `Stop` hooks that block can loop, check `stop_hook_active` before re-blocking.
