---
id: auto-mode-permissions-for-unsupervised-runs
created: 2026-04-25
status: active
supersedes: null
category: permissions
sources:
  - transcripts/simon-scrapes/the-only-claude-code-updates-you-need-to-know-apr-2026_20260424.txt
  - transcripts/simon-scrapes/every-claude-code-concept-explained-for-normal-people_20260307.txt
  - transcripts/ray-amjad/big-claude-code-update-web-mobile-sandbox_20260307.txt
  - https://twitter.com/ClaudeDevs/status/2085794862608318627
---

# Enable Auto Mode or Set Allow/Deny Rules to Run Without Constant Permission Prompts

## TL;DR

Auto mode has been the out-of-the-box permission mode for Pro, Max, and Team users since 14 August 2026: a classifier auto-approves the safe actions (developers approve 93% of prompts anyway) and flags the risky ones. Only accounts that never set a default were flipped, so if you want per-command review, set defaultMode explicitly.

## Why it matters

Approving every file write, package install, and test run is babysitting that defeats the point of an agentic tool, and Anthropic's own research found that 93% of permission prompts get approved regardless. Auto mode automates that safe majority and surfaces only the actions worth a decision: deleting files, pushing to main, sending data out.

The 14 August 2026 flip was a default change rather than an opt-in feature. Anyone who had never configured `defaultMode` silently started running under the classifier instead of per-command prompts, while anyone who had already pinned a mode was untouched, because Claude asks before changing a setting you chose. The exposure is therefore concentrated on people who never looked at the setting, which is exactly the group least likely to notice.

Superseded detail: this lesson previously said auto mode was available on team plans only. That was true when it was written (2026-04-25) and is not true now.

## How to apply

Check which mode you are actually in before an unattended run. To keep manual approval, set an explicit `defaultMode` in settings, or have an admin pin `defaultMode` (or disable auto mode entirely) in managed settings. `Shift+Tab` cycles modes at any point, and `/permissions` changes the running session's mode mid-task without restarting the work.

Auto mode is a convenience layer, not a boundary. Pair it with explicit allow and deny rules, remembering that only the deny list is a hard stop, and contain anything that ingests untrusted input at the environment layer instead of relying on the classifier.

> "Starting August 14, auto mode will be the default permission mode in Claude Code for Pro, Max, and Team users.", @ClaudeDevs (official Anthropic Claude Code account)

## Related

[[default-safe-permission-allowlist-starter-set]], [[auto-mode-broad-allow-dropped-only-deny-is-hard]], [[auto-mode-is-not-injection-containment-isolate-the-session]], [[auto-mode-pauses-after-repeated-blocks-headless-runs-skip-the-action]], [[inspect-and-scope-auto-mode-with-automode-defaults]], [[relocate-automode-config-to-user-settings]], [[change-permission-mode-mid-task-with-permissions]], [[contain-agents-at-environment-layer-not-permission-prompts]]
