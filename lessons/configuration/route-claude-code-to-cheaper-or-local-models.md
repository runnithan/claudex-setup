---
id: route-claude-code-to-cheaper-or-local-models
created: 2026-06-27
status: active
supersedes: null
category: configuration
sources:
  - transcripts/nate-herk-ai-automation/ollama-claude-code-99-cheaper_O2k_qwZA8HU_20260623.txt
  - transcripts/nate-herk-ai-automation/glm-5-2-in-claude-code-is-blowing-my-mind_2OD14-0cot4_20260627.txt
---

# Route Claude Code to Cheaper or Local Models via Base-URL Settings When It Fits

## TL;DR

You can point Claude Code at an alternate backend (OpenRouter, a local Ollama model) by setting the API base URL and token, trading some capability for much lower cost or offline operation.

## Why it matters

Subscription Opus is overkill for bulk, deterministic, or privacy-sensitive work. Routing those runs to a cheaper hosted model or a local one can cut token cost dramatically and keep data on-device — useful as a complement to, not a replacement for, the strong model on hard reasoning.

## How to apply

Set the base-URL / auth-token settings (e.g. point ANTHROPIC_BASE_URL at an OpenRouter-compatible endpoint and supply that key) and select the target model; for local, run Ollama and point Claude Code at it. Test on a small task first, and keep your strongest model for planning and tricky changes. Exact env/setting names drift — verify before relying.

## Related

[[model-selection-opus-sonnet-haiku-use-cases]]
