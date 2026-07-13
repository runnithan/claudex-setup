---
id: yagni-cost-persists-when-agents-generate-code
created: 2026-07-02
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://newsletter.kentbeck.com/p/the-cost-yagni-was-never-about
---

# Free Generation Doesn't Weaken YAGNI — It Makes Speculative Code Cheaper to Commit, Which Is Worse

## TL;DR

When a coding agent can generate speculative structure instantly, YAGNI matters more, not less: the typing cost drops to zero but the optionality and timing costs remain.

## Why it matters

Kent Beck: "Free generation doesn't weaken YAGNI. It makes the violation cheaper to commit, which is worse." Because the agent produces a polished framework you didn't have to write, you casually accept speculative caches/abstractions/config systems — still paying the optionality cost (you've foreclosed designing differently once real requirements arrive) and the timing/NPV cost (infrastructure built early delays real value), while making the code harder to comprehend.

## How to apply

Before accepting agent-generated code, ask "does this feature actually exist yet, or am I building for a prediction?" Constrain the prompt to the current requirement and reject/delete speculative structure the agent adds "for later" (caching, extra abstraction layers, pluggable config, generic frameworks). Build it when you need it — the agent's speed changes the economics of production, not of timing.
