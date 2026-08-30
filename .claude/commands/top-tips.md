---
description: "Rank the high-value lessons that never reached the owner (no trace in habits, config, or backlogs) and offer the top few for adoption. Complements /optimise: it delivers the class with no config surface."
argument-hint: "[n]"
---

# Top Tips

`/optimise` delivers lessons that touch a tracked project's config, and it does that well. This command delivers the class that structurally leaks past it (measured 2026-08-30 at a steady ~25% of high-value general lessons): owner-performed, cross-project workflow habits with no config file to patch, which no process revisits once the extraction run that filed them ends. It ranks the corpus's unadopted general lessons and walks the owner through the top N.

## Arguments

`$ARGUMENTS`: N, how many tips to offer this run (default 3).

## Ledger

`projects/top-tips-ledger.md` records every offer and outcome: ADOPTED (with the destination file), DECLINED (with the reason), or LATER (with the date). Never re-offer an ADOPTED or DECLINED entry; re-offer LATER entries after 30 days. Create the ledger on first run if missing. The ledger is what makes each dialog final; without it every run re-litigates the same tips.

## Procedure

1. **Build the candidate set.** Active lessons (`status: active`) whose `tool:` includes `claude-code` or is absent. Exclude, in order:
   - lessons already in the ledger (offered);
   - lessons cited in `projects/habits.md`, any `projects/*/*/habits.md`, any `projects/*/*/applied-improvements.md`, or encoded in the global `~/.claude/CLAUDE.md` (adopted);
   - lessons cited in any `projects/*/*/improvements.md` backlog (queued: that is `/optimise`'s pipeline, do not duplicate it);
   - superseded, niche, or project-specific lessons (this command's lane is general and owner-facing).
2. **Trace via subagents, not in the main session.** Fan out Explore subagents over the INDEX by category with the grep corpus (`projects/` tree, global CLAUDE.md, `.claude/commands/`); match by slug AND distinctive phrases, since a CLAUDE.md rule encoding a lesson rarely cites its path. Only finalists get read in full.
3. **Rank the untraced remainder** by expected value against how the owner actually works (read `projects/habits.md` and `projects/audit-log.md` for grounding): exposure of the standing practice the lesson protects, frequency of the situation, and the cost of not knowing. A lesson guarding a risky standing practice (unattended runs, auto-merge) outranks a convenience.
4. **Offer the top N, one dialog each**: the tip, why it ranks for THIS owner (grounded in their setup, not generic value), and the exact entry text it would become. Outcomes: **Adopt** (route per `/optimise` §5: agent-performable becomes a config change applied now; owner-performed becomes a habits-file entry), **Decline**, **Later**.
5. **Ledger every outcome in the same run** and report the remaining untraced count, so the owner knows the depth of what is still unranked.

## Self-check

- [ ] No offered lesson had a trace in habits, config, backlogs, or the ledger.
- [ ] Every outcome is ledgered; ADOPTED entries name their destination file.
- [ ] Adopted agent-performable tips were routed to config, not filed as habits (§5 of `/optimise` applies here too).
- [ ] The run reported the remaining untraced count.
