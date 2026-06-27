---
id: give-agents-index-backed-code-search-in-large-codebases
created: 2026-06-27
status: active
supersedes: null
category: mcp
source_type: post
sources:
  - https://sourcegraph.com/blog/why-coding-agents-fail-large-codebases
  - https://sourcegraph.com/blog/sourcegraph-mcp-and-a-cheaper-model-beat-a-mythos-class-model-alone
---

# Give Agents Index-Backed Code Search in Large Codebases — and Reach for Retrieval Before a Pricier Model

## TL;DR

In a large codebase, back the agent with index-backed code search (semantic + find-references + go-to-definition) and have it extract only relevant sections — and when it struggles to locate code, add retrieval before upgrading to a pricier model.

## Why it matters

Sourcegraph found text search 'produces many results with no way to rank them by structural relevance,' and agents 'often read [files] in their entirety, resulting in hundreds of lines of irrelevant code diluting the signal.' They also found 'a cheaper, faster model with good code retrieval beats a more expensive frontier model without it' — about half the cost per quality point, concentrated on cross-repo 'find where a symbol is used' tasks.

## How to apply

Expose a code-search MCP with keyword + semantic search and compiler-aware navigation (definitions, references, type hierarchy), and instruct the agent to pull only the relevant sections, not whole files. Before swapping in a pricier model, measure on discovery-heavy tasks and add the index; reserve upgrades for genuinely reasoning-bound work.

## Related

[[mcp-servers-as-usb-ports-choose-selectively]], [[triage-with-a-cheap-model-before-expensive-work]]
