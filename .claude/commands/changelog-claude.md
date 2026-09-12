---
description: "Read the Claude Code changelog since the last run (plus the Claude Platform release notes for model changes), triage every entry against the global Claude Code setup, and apply the improvements the owner approves. Ledgered, so nothing is re-offered."
argument-hint: "[--since <version>] [--dry-run]"
disable-model-invocation: true
---

# /changelog-claude: keep the global Claude Code setup current with the changelog

Claude Code ships several times a week, and the global setup (the dotfiles repo behind
`~/.claude`) only catches up when the owner happens to read a release. This command reads every
release since the last run, decides for each entry whether it changes what the setup should look
like, and applies the changes the owner approves. Scope is the **global** setup: a tracked
project's `.claude/` is `/optimise`'s job, and mining lessons is `/extract-lessons`'.

Sibling of `/top-tips`: same hub, same ledger discipline, same per-item walkthrough. Runs from
any directory.

## 0. Inputs and locations

- `$ARGUMENTS`: `--since <version>` overrides the ledger watermark for this run (the ledger still
  advances at the end); `--dry-run` triages and reports, edits nothing, leaves the ledger alone.
- **Hub** (the claudex-setup checkout): `git rev-parse --show-toplevel` when that directory holds
  `projects/README.md`; otherwise two directories above the target of
  `readlink -f ~/.claude/commands/changelog-claude.md`. If neither resolves, stop and ask.
- **Ledger**: `<hub>/projects/changelog-claude-ledger.md`. Frontmatter: `watermark` (the newest
  release already triaged), `platform_notes_since` (ISO date), `windows_claude_home` (the other
  machine's `~/.claude`, empty when there is none). Missing file: create it from the §5 template
  with the watermark at the tenth most recent release, and say so in the report.
- **Config root**: `CLAUDE_ROOT="$(dirname "$(readlink -f ~/.claude/CLAUDE.md)")"`, the dotfiles
  repo when `CLAUDE.md` is a symlink into one, else `~/.claude` itself. Files that matter:
  `CLAUDE.md`, `settings.json`, `windows/settings.json` (the other OS's variant, if present),
  `settings.local.json`, `keybindings.json`, `skills/` (ignore `gsd-*`), `hooks/`.
- **Versions**: `claude --version` against the newest `## x.y.z` heading in the changelog.
- `$SCRATCH` below is the session scratchpad directory named in your system prompt.

## 1. Fetch and slice

`curl`, never WebFetch: WebFetch answers through a small model, and the raw file is the evidence
every proposal quotes.

```bash
curl -sL https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md -o "$SCRATCH/cc-changelog.md"
grep -qx "## $WATERMARK" "$SCRATCH/cc-changelog.md" || echo "watermark $WATERMARK not in changelog, stop"
awk -v w="## $WATERMARK" '$0==w{exit} {print}' "$SCRATCH/cc-changelog.md" > "$SCRATCH/cc-slice.md"
grep -c '^## ' "$SCRATCH/cc-slice.md"
```

- The slice is every release newer than the watermark, newest first. A watermark that is not in
  the file (a mistyped `--since`) stops the run; it must not fall through to the whole file.
- **Read the raw version blocks, not a summary.** The hub's method notes record, twice, that the
  entries that mattered most (a silent permission bypass, a default flip) surfaced only on
  re-reading the raw blocks after a scout had summarised them. Read the slice in chunks of at
  most 15 releases; after each chunk, write its candidates into the ledger's `## Pending` block
  before reading the next, so a compaction mid-run loses nothing. A non-empty `## Pending` at the
  start of a run is resumed before anything new is read.
- **Platform release notes, model changes only.** `curl -sL https://platform.claude.com/docs/en/release-notes/overview.md`
  and keep the dated sections newer than `platform_notes_since` that announce a model launch,
  deprecation, retirement or price change. The global `CLAUDE.md` hardcodes model ids, cutoffs
  and a routing ladder; those entries are the only platform notes that can change the setup.
- If the installed version is older than the newest release, the run's first proposal is
  `claude update`. Until it lands, entries above the installed version describe things the setup
  cannot use yet: their outcome is `PENDING-UPDATE` (§4), not a decision.

## 2. Inventory the setup the entries are judged against

Batch these reads; none depends on another.

- `CLAUDE.md`: every rule, and specifically every `REVISIT:` tag with the version or date it
  names. Those tags are the stale-workaround policy's contract, and a changelog run is exactly
  the moment they were written to be re-checked.
- `settings.json` and `windows/settings.json`: top-level keys, `permissions`, `env`, the hook
  events wired, `statusLine`, `fileSuggestion`, `model`. `settings.local.json` and
  `keybindings.json` likewise.
- `skills/` (non-`gsd-*`), `hooks/`, and `ls -l ~/.claude/commands` (which hub commands are linked
  in).
- `claude plugin list`, `claude mcp list`, `claude doctor`.
- Hub files an entry can affect: `projects/habits.md` (an owner habit a fix may retire) and the
  frontmatter of the shipped artifacts (`.claude/commands/*.md`, `skills/*/SKILL.md`,
  `agents/*.md`), since an entry about frontmatter fields or hook events applies to them.
- The auto-memory index (`~/.claude/projects/*/memory/MEMORY.md`): `feedback` entries often
  encode a workaround for a limitation a release has since removed.

## 3. Triage every entry in the slice

One line per entry, into exactly one bucket. Quote the entry verbatim from the curled file, never
retyped, and name its version.

- **Config**: a new setting, env var, hook event, CLI flag, frontmatter field or command that
  would improve the setup. Proposal: the exact diff, on the file it belongs in.
- **Retire**: a fix or change that makes part of the setup obsolete: a `REVISIT`-tagged rule, a
  habit in `projects/habits.md`, a defensive `CLAUDE.md` line, a hook guarding a fixed bug, a
  feedback memory. Proposal: the deletion, with the entry as evidence.
- **Risk**: a security or permission-bypass fix, a default flip, a removed behaviour. Surfaced
  even when nothing needs changing, because it changes what the existing guardrails actually do.
- **Habit**: something the owner does at the keyboard (a new slash command, keystroke, mode).
  Goes to the ledger's `## For the owner` list; offered for `projects/habits.md`.
- **Skip**: gateway, managed settings, enterprise, SDK-only, platforms and IDEs not in use,
  cosmetic. Counted, not listed.

Rules that decide the bucket:

- Already present in the inventory means Skip with the note "already adopted", never a proposal.
- Prefer a setting, hook or slash command over a new `CLAUDE.md` line: the global file loads on
  every turn of every session, and a rule the model already follows only degrades it. When an
  entry retires a rule, the proposal is the shorter file.
- **Verify what you can observe instead of trusting the entry.** A changelog line is a claim.
  When a `REVISIT` tag concerns something visible from inside this session (a system-prompt
  directive, a tool description, a flag in `claude --help`), look, and record what you saw
  against the installed version. Worked example: the rule that says to ignore the auto-mode
  directive preferring `sed` over the editing tools is re-checked by searching your own context
  for that directive. Present or absent, the tag's version and date move to today.
- An OS-neutral change to `settings.json` is mirrored into `windows/settings.json`; hook paths
  and OS-specific env stay per file. A Windows `commands/` copy is refreshed by hand (§5).

## 4. Walk the proposals

Print the triage table first: version, entry, bucket, proposed action, target file. With
`--dry-run`, stop there. Otherwise walk the Config and Retire items with `AskUserQuestion`, up to
four items per call, each offering **Apply / Decline / Later**:

- **Apply**: edit with Read and Edit, not `sed`, then validate before moving on:
  `python3 -I -c 'import json,sys; json.load(open(sys.argv[1]))' <file>` for every JSON file
  touched, `claude plugin validate <dir>` for any skill or command touched, `claude doctor` after
  a settings change. A failed check reverts that item and ledgers it as `FAILED` with the output.
  Apply the §3 mirror edit in the same step.
- **Decline**: final, never re-offered. Record the reason.
- **Later**: re-enters after 30 days.
- **PENDING-UPDATE**: set without asking for items above the installed version when the update
  was declined; re-enters once `claude --version` reaches that release.

Habit items are offered as one multi-select rather than one by one; accepted ones are appended
to `projects/habits.md` in its existing entry shape.

## 5. Ledger, commit, report

Ledger shape (created on first run):

```markdown
---
name: /changelog-claude ledger
updated: <date>
watermark: <version>
platform_notes_since: <date>
windows_claude_home: <path or empty>
---
## Pending
## Runs
### <date>: <old watermark> to <new watermark>, installed <version>
- <version> `<entry, shortened>`: **APPLIED** -> <file> | **DECLINED**, <reason> | **LATER** | **PENDING-UPDATE** | **RISK** noted | **FAILED**, <output>
## For the owner
- <version>: <the thing to try>
```

- Advance `watermark` to the newest release triaged and `platform_notes_since` to today, clear
  `## Pending`, and ledger every outcome in the same run.
- **Commit the config repo** (`CLAUDE_ROOT`, when it is one): stage only the files this run
  changed, Conventional Commits, no attribution lines, then push (the owner's standing rule for
  that repo). **Commit the hub** for the ledger and any artifact edit, without pushing; a changed
  shipped artifact gets its `CHANGELOG.md` entry in the same commit.
- Report with exact counts: releases read, entries triaged, per-bucket totals, applied / declined
  / later / pending-update / failed, watermark before and after, installed against newest. Then
  the owner follow-ups, each in its own single-line code block: pull the config repo on the
  other machine, recopy any changed command into `<windows_claude_home>/commands`, run
  `claude update` if it was declined.

## Self-check

- [ ] Every proposal quotes the raw changelog line and names its version.
- [ ] Nothing proposed duplicates something the inventory showed already present.
- [ ] Every `REVISIT` tag in `CLAUDE.md` was re-checked and its date moved, kept or retired.
- [ ] Every outcome is ledgered, APPLIED entries name their file, `## Pending` is empty.
- [ ] Every JSON file touched parses; every artifact touched passed `claude plugin validate`.
- [ ] The report gives numbers, not adjectives, and the follow-up commands are one per block.
