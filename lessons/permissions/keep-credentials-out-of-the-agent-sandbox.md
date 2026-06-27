---
id: keep-credentials-out-of-the-agent-sandbox
created: 2026-06-27
status: active
supersedes: null
category: permissions
source_type: canonical
sources:
  - https://www.anthropic.com/engineering/managed-agents
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Keep Credentials Out of the Sandbox Where Generated Code Runs — Enforce With sandbox.credentials

## TL;DR

Ensure credentials are never reachable from the sandbox where Claude's generated code executes — mediate access through a proxy/broker outside the boundary — and in Claude Code enable the sandbox.credentials setting to block sandboxed commands from reading credential files and secret env vars.

## Why it matters

If generated code runs where your auth tokens live, a buggy or adversarial generation can read or exfiltrate them — a structural leak permission prompts won't catch. Anthropic's guidance: 'make sure the tokens are never reachable from the sandbox where Claude's generated code runs.' The sandbox.credentials setting (changelog 2.1.187) closes the credential-read hole inside the sandbox itself.

## How to apply

Architect agent execution so the sandbox has no path to secrets — put tokens behind a proxy/credential broker — and turn on sandbox.credentials in settings.json when running untrusted code or autonomous agents under /sandbox so secret files and env vars are unreadable to sandboxed commands.

## Related

[[contain-agents-at-environment-layer-not-permission-prompts]], [[sandbox-mode-for-safe-exploration]], [[give-agents-a-local-mock-dev-env-instead-of-prod-credentials]]
