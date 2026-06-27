---
id: use-dynamic-workflows-for-high-value-complex-work
created: 2026-06-27
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code
---

# Use Dynamic Workflows (ultracode) for High-Value, Failure-Prone Work — With a Token Budget

## TL;DR

Beyond the hand-written .claude/workflows JS tool, Claude can compose its own multi-agent harness on the fly — ask it to 'create a workflow' or use the 'ultracode' keyword — but reserve it for complex, high-value work and cap cost with an explicit token budget.

## Why it matters

Dynamic workflows pour more compute into a hard task by generating a bespoke orchestration program, countering laziness, self-bias, and goal drift. But they spend far more tokens by spawning many agents, so the team's own guidance is to first ask 'does it really need more compute?' — most coding doesn't. Use width (parallel agents) for breadth and /goal for iterative depth.

## How to apply

For genuinely complex/failure-prone tasks (fan-out-and-synthesize, classify-and-act, adversarial verify with one verifier per rule), trigger a workflow by asking for one or saying 'ultracode', and set a token budget to bound spend. For everyday edits, don't — it's wasted compute. Pair with /loop for cadence and /goal for a hard finish line.

## Related

[[workflows-js-deterministic-orchestration]], [[goal-verifiable-finish-lines-with-safety-caps]], [[disable-the-workflow-keyword-trigger]]
