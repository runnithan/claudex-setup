---
id: semantic-hybrid-memory-search-with-reranking
created: 2026-06-11
status: active
supersedes: null
category: memory
sources:
  - transcripts/simon-scrapes/i-built-the-best-claude-memory-system-beats-hermes_20260610.txt
---

# Build Memory as Three Jobs: Capped Injection, Auto-Capture, Hybrid Search With Citations

## TL;DR

Treat memory as three separate jobs, a small frozen snapshot injected at session start (~1.3k tokens, cacheable), automatic post-turn capture into logs, and recall via hybrid semantic+keyword search with reranking and cited answers, rather than one agent-decided memory file.

## Why it matters

Claude's default memory is leaky (the agent decides what to store), unbounded (no token cap on what gets injected), and recall is keyword-only. Splitting the jobs fixes each failure: the capped snapshot keeps injection cheap and cache-friendly, hooks make capture deterministic instead of discretionary, and hybrid search + reranking finds facts by meaning and returns them with sources you can verify.

## How to apply

Compose it from parts: (1) a post-turn/session-end hook that summarizes into a daily log (auto-capture); (2) a curated snapshot file injected at session start, hard-capped in size so it stays in prompt cache; (3) embeddings over the logs stored on disk for semantic search, combined with keyword match (hybrid), ideally reranked, with answers citing which log entry they came from. For team use, back the store with a shared DB (e.g., Supabase with row-level security per user).
