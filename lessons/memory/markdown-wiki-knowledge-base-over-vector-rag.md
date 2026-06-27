---
id: markdown-wiki-knowledge-base-over-vector-rag
created: 2026-06-27
status: active
supersedes: null
category: memory
sources:
  - transcripts/nate-herk-ai-automation/andrej-karpathy-just-10x-d-everyone-s-claude-code_sboNwYmH3AY_20260623.txt
---

# Build a Markdown Wiki Knowledge Base Instead of Vector RAG for Small Corpora

## TL;DR

For a few hundred documents, have Claude organize raw sources into a markdown wiki with an auto-maintained index and cross-links, then answer queries by reading the index and following links — no embeddings or vector database required.

## Why it matters

Vector RAG needs embedding pipelines and a vector store, and retrieval quality is opaque. At small scale, an LLM is good at maintaining a markdown index and navigating link relationships, which is cheaper to run, fully inspectable, and edits cleanly. Popularized by Andrej Karpathy's 'LLM wiki' idea.

## How to apply

Keep a /raw folder of source docs and a /wiki folder of LLM-organized notes; have Claude generate and maintain an index.md with one-line summaries and backlinks between related notes. Query by pointing Claude at the index and letting it follow links. Run periodic lint/consistency passes; browse visually in Obsidian if you like.

## Related

[[second-brain-after-session-knowledge-updates]], [[semantic-hybrid-memory-search-with-reranking]]
