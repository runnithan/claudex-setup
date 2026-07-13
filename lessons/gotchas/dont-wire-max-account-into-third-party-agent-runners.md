---
id: dont-wire-max-account-into-third-party-agent-runners
created: 2026-07-02
status: active
supersedes: null
category: gotchas
sources:
  - transcripts/edmund-yong/my-openclaw-workflows-u0026-automations-for-building-apps-solo-easy-setup-runnin_XmSxfFrkcDs_20260702.txt
---

# Never Wire Your Claude Max Account Into Third-Party Agent Runners

## TL;DR

Connecting a Claude Code Max subscription to third-party autonomous agent frameworks (e.g. OpenClaw) can get your account banned for a ToS violation.

## Why it matters

Anthropic has reportedly started banning users who route their personal Max account into external always-on agent tools. A convenience hack — reusing your subscription login instead of paying for API tokens — can cost you your whole account.

## How to apply

For OpenClaw-style or other third-party agent runners, use a separately-issued API key (e.g. from a managed gateway that bills tokens directly) rather than your Claude Code Max login. Keep personal-subscription auth isolated to first-party Claude Code usage.

## Related

[[harden-always-on-agents-least-privilege-and-capable-models]], [[avoid-the-1m-context-model-without-usage-credits]], [[vps-tmux-telegram-persistent-sessions]]
