---
description: "Read the Codex CLI release notes and the OpenAI Codex changelog since the last run, triage every entry against the global Codex setup (config.toml, feature flags, hooks, skills, AGENTS.md, model pins), and apply the improvements the owner approves. Ledgered, so nothing is re-offered."
argument-hint: "[--since <version>] [--dry-run]"
disable-model-invocation: true
---

# /changelog-codex: keep the global Codex setup current with the release notes

Codex ships a stable release most days, and the global setup only changes when the owner
remembers a release. This command reads every stable release since the
last run, decides for each entry whether it changes what the setup should look like, and applies
the changes the owner approves. Scope is the **global** setup: a tracked project's `AGENTS.md`
and `.codex/` are `/optimise <slug> --codex`'s job.

Sibling of `/changelog-claude` and `/top-tips`: same hub, same ledger discipline, same per-item
walkthrough. Runs from any directory. Needs `gh` (authenticated) and `codex` on `PATH`.

## 0. Inputs and locations

- `$ARGUMENTS`: `--since <version>` (a stable CLI version such as `0.150.0`) overrides the ledger
  watermark for this run; `--dry-run` triages and reports, edits nothing, leaves the ledger alone.
- **Hub** (the claudex-setup checkout): `git rev-parse --show-toplevel` when that directory holds
  `projects/README.md`; otherwise two directories above the target of
  `readlink -f ~/.claude/commands/changelog-codex.md`. If neither resolves, stop and ask.
- **Ledger**: `<hub>/projects/changelog-codex-ledger.md`. Frontmatter: `watermark` (the newest
  stable CLI release already triaged), `docs_changelog_since` (ISO date), `windows_codex_home`
  (the other machine's `~/.codex`, empty when there is none). Missing file: create it from the §5
  template with the watermark at the tenth most recent stable release, and say so.
- **Config root**: `CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"`. Files that matter: `config.toml`,
  `rules/`, `AGENTS.md`, `skills/` (ignore `.system`), `agents/*.toml` (installer-managed, only
  their model pins matter), `plugins/`. `hooks.json` is absent by design: GSD writes one that does
  nothing under Codex, and the linker retires it.
- **Dotcodex** (since 2026-09-12): `config.toml`, `rules/` and `AGENTS.md` are symlinks into a
  private dotfiles repo, which also holds the Windows variant at `windows/config.toml`. Below,
  `<dotcodex>` means your local checkout of that repo and `<dotcodex-windows>` the Windows
  clone; the concrete paths live in the owner's global CLAUDE.md, not here. Git is the undo and
  the record of every edit (§4, §5). The Windows clone pulls the mirror; its live files are
  symlinks into it.
- **Versions**: `codex --version` against the newest stable `rust-v` tag; `codex doctor` prints
  both in its Notes block.
- `$SCRATCH` below is the session scratchpad directory named in your system prompt.

## 1. Fetch and slice

Two sources, fetched with `gh` and `curl`, never WebFetch.

**(a) CLI release notes**, the structured source and the one config changes come from:

```bash
gh release list --repo openai/codex --exclude-pre-releases --limit 60 --json tagName -q '.[].tagName' | grep '^rust-v' > "$SCRATCH/codex-tags.txt"
{ echo "rust-v$WATERMARK"; cat "$SCRATCH/codex-tags.txt"; } | sort -Vu | awk -v w="rust-v$WATERMARK" 'f{print} $0==w{f=1}' > "$SCRATCH/codex-new-tags.txt"
while read -r tag; do printf '\n# %s\n' "$tag"; gh release view "$tag" --repo openai/codex --json body -q .body | sed -n '1,/^## Changelog/p'; done < "$SCRATCH/codex-new-tags.txt" > "$SCRATCH/codex-notes.md"
```

Read the curated sections only (New Features, Bug Fixes, Breaking Changes, Documentation,
Chores); the PR list after `## Changelog` is noise unless a curated line needs its PR for detail.
Pre-releases (`-alpha`) are excluded on purpose. If `codex-new-tags.txt` is empty and `--since`
was given, the version was mistyped: stop rather than read nothing.

**(b) The OpenAI Codex changelog page**, the product-level source (model retirements,
deprecations, cloud and app features). It is HTML, so write `strip.py` from the block below into
`$SCRATCH` first, then:

```bash
curl -sL https://developers.openai.com/codex/changelog -o "$SCRATCH/codex-changelog.html"
python3 -I "$SCRATCH/strip.py" "$SCRATCH/codex-changelog.html" > "$SCRATCH/codex-changelog.txt"
```

```python
import html, re, sys
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
m = re.search(r"<main[^>]*>(.*)</main>", s, flags=re.S)
body = m.group(1) if m else s
tag = r"<(?:[^>\"']|\"[^\"]*\"|'[^']*')*>"
body = re.sub(r"<(script|style|nav|svg)[^>]*>.*?</\1>", "", body, flags=re.S)
body = re.sub(r"<h([1-6])(?:[^>\"']|\"[^\"]*\"|'[^']*')*>", lambda h: "\n" + "#" * int(h.group(1)) + " ", body)
body = re.sub(r"<li(?:[^>\"']|\"[^\"]*\"|'[^']*')*>", "- ", body)
body = re.sub(r"</(h[1-6]|p|li|div|section|article|tr)>", "\n", body)
text = html.unescape(re.sub(tag, "", body))
text = re.sub(r"[ \t]+\n", "\n", re.sub(r"\n{3,}", "\n\n", text))
sys.stdout.write(text)
```

Entries are dated lines (`-     2026-09-05`) followed by a `###` title. Keep the entries newer
than `docs_changelog_since` that concern Codex (CLI, app server, cloud, models, plugins); the
ChatGPT iOS and desktop entries are Skip unless they change Codex behaviour.

- **Read the raw notes, not a summary**, in chunks of at most 15 releases; after each chunk write
  its candidates into the ledger's `## Pending` block before reading the next, so a compaction
  mid-run loses nothing. A non-empty `## Pending` at the start of a run is resumed first.
- If the installed version is older than the newest stable release, the run's first proposal is
  `codex update`. Until it lands, entries above the installed version describe things the setup
  cannot use yet: their outcome is `PENDING-UPDATE` (§4), not a decision.

## 2. Inventory the setup the entries are judged against

Batch these reads; none depends on another.

- `config.toml`, parsed rather than skimmed: `model`, `review_model`, `model_reasoning_effort`,
  `approval_policy`, `sandbox_mode`, `[features]`, `[projects]` trust rows, `[mcp_servers]`,
  `[agents]`, `[hooks.state]` (trusted hashes: editing `hooks.json` changes them and Codex asks
  for trust again). Keep the comments; they record why a key is set.
- `codex features list`: every flag with its stage and effective state. An entry saying a
  feature graduated, was renamed or was removed is checked here, not guessed.
- `hooks.json` (absent by design; if a GSD update re-created it, `<dotcodex>/link.sh`
  retires it again); `skills/` and what each links to; `grep -h '^model' agents/*.toml | sort | uniq -c`
  for model pins; `AGENTS.md` (global, tracked in dotcodex); `codex mcp list`; `codex doctor`.
- `<dotcodex>/windows/config.toml`, the Windows variant (`<windows_codex_home>/config.toml` is
  its symlink once the Windows clone is current): the same keys, for the mirror decision.
- Hub files an entry can affect: `projects/habits.md` (Codex entries), `projects/*/codex/current.md`
  (the hub's own inventories), the root `AGENTS.md`, the skills shipped into Codex, and
  `.claude/commands/codex-loop.md`, which encodes `codex review` behaviour (`review_model`, output
  quirks), so an entry that changes `codex review` changes that command.

## 3. Triage every entry

One line per entry, into exactly one bucket. Quote the entry verbatim from the fetched notes,
never retyped, and name its release (or the page date).

- **Config**: a new config key, feature flag, hook event, CLI flag or subcommand that would
  improve the setup. Proposal: the exact diff, on the file it belongs in.
- **Retire**: a change that makes part of the setup obsolete: a `[features]` line for a flag
  that is now stable and on by default (or removed), a workaround comment in `config.toml`, a
  habit in `projects/habits.md`, a hook guarding a fixed bug. Proposal: the deletion, with the
  entry as evidence.
- **Risk**: a security fix, a sandbox or approval-policy change, a default flip, a removed
  command or entry point. Surfaced even when nothing needs changing.
- **Habit**: something the owner does at the keyboard (a new slash command, keybinding, mode).
  Goes to the ledger's `## For the owner` list; offered for `projects/habits.md`.
- **Skip**: platforms not in use, IDE and app surfaces not in use, cosmetic. Counted, not listed.

Rules that decide the bucket:

- Already present in the inventory means Skip with the note "already adopted", never a proposal.
- **Feature flags are checked against `codex features list`, not the notes.** Stable and on by
  default: the explicit line is Retire. Under development: Skip unless the owner's workflow
  needs it, and say so. Removed: Retire the line.
- **Model entries hit pins, not the picker.** A retirement or rename is checked against
  `config.toml` (`model`, `review_model`), every `agents/*.toml` pin, and any scheduled
  automation; propose the pin change with the retirement date.
- A change to `codex review` is a proposal against `/codex-loop` as well as the config.
- **Verify what you can observe instead of trusting the entry.** A release note is a claim; a
  flag in `codex --help`, a row in `codex features list`, a line in `codex doctor` is evidence.
  Record what you saw against the installed version.
- Mirror only same-key, OS-neutral changes into `<dotcodex>/windows/config.toml`, each with its
  own approval: that file differs from this machine's on purpose (trust rows and `[windows]` are
  per-machine; model, effort, approval policy and sandbox may differ too, though today they
  match). The Windows clone picks the edit up on its next `git pull`.

## 4. Walk the proposals

Print the triage table first: release, entry, bucket, proposed action, target file. With
`--dry-run`, stop there. Otherwise walk the Config and Retire items with `AskUserQuestion`, up to
four items per call, each offering **Apply / Decline / Later**:

- **Apply**: before the first edit of the run, check `git -C <dotcodex> status --short`
  is clean (commit or set aside anything pending, so the run's diff is only the run's). Edit the
  repo files with Read and Edit, not `sed`, keeping "why" comments between root keys (Codex drops
  comments that sit directly above a table it rewrites), then validate before moving on:
  `python3 -I -c 'import tomllib,sys; tomllib.load(open(sys.argv[1],"rb"))' <file>` for
  `config.toml`, `codex execpolicy check --rules <file> -- <cmd>` for `rules/default.rules`, then
  `codex doctor` (it re-reads the config) and `codex features list` when `[features]` changed. A
  failed check reverts that file with `git checkout -- <file>` and ledgers the item as `FAILED`
  with the output. Apply the §3 mirror edit in the same step when one applies.
- **Decline**: final, never re-offered. Record the reason.
- **Later**: re-enters after 30 days.
- **PENDING-UPDATE**: set without asking for items above the installed version when the update
  was declined; re-enters once `codex --version` reaches that release.

Habit items are offered as one multi-select rather than one by one; accepted ones are appended
to `projects/habits.md` in its existing entry shape.

## 5. Ledger, commit, report

Ledger shape (created on first run):

```markdown
---
name: /changelog-codex ledger
updated: <date>
watermark: <version>
docs_changelog_since: <date>
windows_codex_home: <path or empty>
---
## Pending
## Runs
### <date>: <old watermark> to <new watermark>, installed <version>
- <release> `<entry, shortened>`: **APPLIED** -> <file> | **DECLINED**, <reason> | **LATER** | **PENDING-UPDATE** | **RISK** noted | **FAILED**, <output>
## For the owner
- <release>: <the thing to try>
```

- Advance `watermark` to the newest stable release triaged and `docs_changelog_since` to today,
  clear `## Pending`, and ledger every outcome in the same run.
- **Commit dotcodex** (Conventional Commits, one commit per run) and push it, so the Windows clone
  can pull; the ledger is the record of why. **Commit the hub** for the ledger and any artifact
  edit (`/codex-loop`, a shipped skill), without pushing; a changed shipped artifact gets its
  `CHANGELOG.md` entry in the same commit.
- Report with exact counts: releases read, page entries read, entries triaged, per-bucket totals,
  applied / declined / later / pending-update / failed, watermark before and after, installed
  against newest. Then the owner follow-ups, each in its own single-line code block: run
  `codex update` if it was declined, `git -C <dotcodex-windows> pull` on the Windows
  machine when `windows/config.toml` changed, apply any change that was not mirrored.

## Self-check

- [ ] Every proposal quotes the raw release note or page entry and names its release or date.
- [ ] Nothing proposed duplicates something the inventory showed already present.
- [ ] Every `[features]` line was checked against `codex features list` this run.
- [ ] Every model pin (`config.toml`, `agents/*.toml`) was checked against any retirement entry.
- [ ] Every outcome is ledgered, APPLIED entries name their file, `## Pending` is empty.
- [ ] `config.toml` parses and `codex doctor` ran clean after the last edit; dotcodex is committed and pushed.
- [ ] The report gives numbers, not adjectives, and the follow-up commands are one per block.
