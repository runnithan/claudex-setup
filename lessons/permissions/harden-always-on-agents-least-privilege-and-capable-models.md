---
id: harden-always-on-agents-least-privilege-and-capable-models
created: 2026-07-02
status: active
supersedes: null
category: permissions
sources:
  - transcripts/edmund-yong/my-openclaw-workflows-u0026-automations-for-building-apps-solo-easy-setup-runnin_XmSxfFrkcDs_20260702.txt
  - transcripts/sean-kochel/the-clawdbot-hype-is-lying-to-you_XwhVFO-HrPA_20260702.txt
---

# Harden Always-On Agents: Sandbox, Least-Privilege Tools, and Capable Models Only

## TL;DR

For 24/7 phone-accessible agents, run them sandboxed with tightly-scoped credentials, grant tools incrementally, only run skills you've reviewed, and avoid cheap models because they resist prompt injection less.

## Why it matters

A general agent decides its own control flow, so a bad skill definition or a prompt-injection (e.g. from an agent social feed) can drain money or exfiltrate SSH keys/secrets — people have burned hundreds-to-thousands overnight on runaway loops. The framework won't rescue a poorly-defined skill and may skip it entirely, and weaker/cheaper models have thinner defensive guardrails.

## How to apply

Put always-on agents (clawdbot-style Telegram/VPS loops) in a sandbox and don't hand them your bank, API keys, or social accounts directly. Start with minimal access and add tools (email, etc.) only when a specific automation needs them. Only install skills you've read and trust, or write your own. Run a capable model (Opus/Codex-tier) for anything touching sensitive data or untrusted web content, and invest in precise skill/tool definitions rather than expecting the agent loop to compensate.

## Related

[[contain-agents-at-environment-layer-not-permission-prompts]], [[keep-credentials-out-of-the-agent-sandbox]], [[dont-wire-max-account-into-third-party-agent-runners]]
