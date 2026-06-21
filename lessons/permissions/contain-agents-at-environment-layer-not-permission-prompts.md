---
id: contain-agents-at-environment-layer-not-permission-prompts
created: 2026-06-21
status: active
supersedes: null
category: permissions
source_type: post
sources:
  - https://simonwillison.net/2026/Jun/11/fable-is-relentlessly-proactive/
  - https://www.anthropic.com/engineering/how-we-contain-claude
---

# Contain Coding Agents at the Environment Layer, Never via Permission Prompts Alone

## TL;DR

Permission prompts suffer approval fatigue (users approve ~93% of them), so they're a weak primary defense. Enforce boundaries with sandboxes, VMs, and egress controls first, then steer behavior at the model layer.

## Why it matters

Click-through approvals give false safety — a socially-engineered or mistaken action still gets approved most of the time. As models grow more proactive (browser automation, spawning servers), an unsandboxed agent that ingests malicious instructions can exfiltrate data or damage the machine.

## How to apply

Run agents in a container, VM, or OS sandbox (Seatbelt on macOS, bubblewrap on Linux) with scoped filesystem and network/egress policy, and keep credentials out of the sandbox. Treat project-local config as untrusted until accepted. Layer model-level oversight on top — don't depend on it alone.

## Related

[[sandbox-mode-for-safe-exploration]], [[auto-mode-permissions-for-unsupervised-runs]]
