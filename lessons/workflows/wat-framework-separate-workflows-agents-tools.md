---
id: wat-framework-separate-workflows-agents-tools
created: 2026-06-27
status: active
supersedes: null
category: workflows
sources:
  - transcripts/nate-herk-ai-automation/master-95-of-claude-code-in-36-mins-as-a-beginner_20260620.txt
---

# Structure Agentic Systems as Workflows, Agents, and Tools (Separate Reasoning From Execution)

## TL;DR

Architect agentic systems in three layers — markdown workflow SOPs (the plan), an agent (the coordinator), and code tools (deterministic execution) — so the LLM reasons and routes while real code does the deterministic work.

## Why it matters

Mixing reasoning and execution makes systems brittle: the model hallucinates steps and you can't tell why a run failed. Separating a plain-language workflow file, a coordinating agent, and tested tool scripts makes the system self-healing — when a tool breaks, the agent can fix the tool and update the workflow to prevent recurrence.

## How to apply

Keep a workflows/ folder of markdown SOPs (inputs, outputs, edge cases), a tools/ folder of small scripts (API calls, transforms, file ops), and let the agent read a workflow and call tools in sequence with error handling. Put secrets in env, not in the workflow/tool files.

## Related

[[skill-systems-over-monolithic-skills]], [[cli-tools-over-mcp-for-tokens]]
