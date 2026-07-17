# IMPLEMENT.md

Optional third-party tools that pair well with `claudex-setup`. They update independently, so install them fresh from source instead of vendoring snapshots that go stale. Install them into the hub itself, or directly into a target project you're working in — both work.

## What to install

1. GSD — spec-driven planning + execution
2. Ralph (optional) — autonomous loops for long, well-specified tasks

---

## GSD (Get Shit Done)

Spec-driven planning + execution workflow. Adds `/gsd-*` slash commands, planning agents, and `.planning/` state.

**Source of truth:** https://github.com/gsd-build/get-shit-done

**Install (project-local):**
```bash
npx get-shit-done-cc --local
```

**Install (global, ~/.claude/):**
```bash
npx get-shit-done-cc --global
```

**Update:** re-run the same command. GSD writes its own `gsd-file-manifest.json` and `get-shit-done/` folder — do not commit these (already covered in `.gitignore` patterns; add `get-shit-done/` and `gsd-file-manifest.json` if not).

**Why not the plugin marketplace version (`/plugin install gsd@gsd-plugin`):** lags the official release.

---

## Ralph (Wiggum loop)

Autonomous agent loop — feeds a prompt file back to Claude until the task is done. Geoffrey Huntley's original technique; in its purest form a one-line bash loop.

**Source of truth:** https://github.com/ghuntley/how-to-ralph-wiggum
**Background reading:** https://ghuntley.com/ralph/

**Minimal install (the OG one-liner — no repo needed):**
```bash
while :; do cat PROMPT.md | claude -p --dangerously-skip-permissions; done
```

**Install the methodology repo (templates + guidance):**
```bash
git clone https://github.com/ghuntley/how-to-ralph-wiggum.git
```

**Why not Anthropic's plugin (`anthropics/claude-code/plugins/ralph-wiggum`):** the OG repo is the canonical reference and stays closer to Geoffrey's original pattern. Anthropic's plugin wraps the same idea in a Stop hook — fine, but less transparent.

**When to use:** long-running tasks where you'd otherwise babysit Claude (overnight implementations, large refactors with a clear spec).
