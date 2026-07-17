# Project Structure

This repo is a standalone Claude Code hub you run *from*, kept alongside your projects rather than copied into each one (see [README.md](../README.md)). You mine lessons here, and `/optimise` reaches out to improve your *other* projects' `.claude/` setups in place. (Copying the repo into a project's own `.claude/` is the advanced/plugin exception — see the README's "Using it inside another project" section.)

```
claudex-setup/
  CLAUDE.md                 # project instructions (curated — see lessons/README.md)
  IMPLEMENT.md              # optional third-party tools to install into the hub or a target project (GSD, Ralph)
  README.md                 # how to run the hub (and the advanced copy-into-.claude path)
  settings.json             # shared Claude Code settings (hooks, permissions)
  settings.local.json       # machine-local settings (not portable)
  package.json              # JS deps for hooks
  pyproject.toml / uv.lock  # Python deps for scripts/ (youtube-transcript-api)

  .claude-plugin/           # plugin manifest (plugin.json) — the auto-updating commands/agents/skills path
  .claude/commands/         # slash commands (/extract-lessons, /optimise, /test, ...)
  agents/                   # custom subagent definitions (backend-dev, frontend-dev, qa,
                            #   code-reviewer, code-simplifier, pr-test-analyzer)
  hooks/                    # lifecycle hook scripts (auto-format, security reminder,
                            #   gsd-* hooks written by the GSD installer)
  skills/                   # locally-tuned skills (claude-md-improver, frontend-design)
  references/               # detail docs CLAUDE.md points to (integrations, this file)

  scripts/                  # transcript pipeline + scheduled-task setup
                            #   update_urls.py, fetch_transcripts.py, run_pipeline.py,
                            #   install_scheduled_task.ps1, ralph-*.sh

  transcripts/              # fetched YouTube transcripts, one folder per creator
                            #   urls.txt (source list), index.md (manifest),
                            #   no-transcript-available.md (skip ledger)
  lessons/                  # mined lessons, one file per lesson under <category>/
                            #   INDEX.md (active-lesson index), .processed.json (dedup)

  projects/                 # per-project improvement notes (one folder per tracked project)
                            #   multi-tool projects nest per-tool sub-areas (claude-code/,
                            #   claude-design/, codex/); /optimise --design and --codex target those
```

Third-party tooling (GSD, Ralph) is installed separately — see [IMPLEMENT.md](../IMPLEMENT.md). Its generated files (`get-shit-done/`, `gsd-file-manifest.json`) stay uncommitted.
