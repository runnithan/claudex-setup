---
id: self-interview-skill-to-extract-tacit-knowledge
created: 2026-06-27
status: active
supersedes: null
category: skills
sources:
  - transcripts/nate-herk-ai-automation/the-skill-that-10x-d-my-claude-code-projects_c0kaKxM2pHg_20260627.txt
  - transcripts/nate-herk-ai-automation/turn-claude-code-into-your-executive-assistant-in-27-mins_20260620.txt
  - transcripts/nate-herk-ai-automation/i-turned-claude-into-the-ultimate-second-brain_8QQ_INxAhRs_20260627.txt
---

# Build a Self-Interview ('Grill Me') Skill to Extract Tacit Knowledge Into Context

## TL;DR

Create a skill that interrogates you about a process — asking pointed follow-ups until it stops learning anything new — and writes the captured decisions and nuance into context or skill files.

## Why it matters

The knowledge that makes a workflow good usually lives in your head and never reaches your config. A structured self-interview forces it out, and feeding that back into skills/context noticeably raises first-try success because the agent now shares your assumptions.

## How to apply

Write a skill that asks one question at a time about a target process, keeps asking follow-ups until ~20-30 questions in and two rounds yield nothing new, then saves a Q&A log plus the key decisions to a brainstorm/context file. Re-run it whenever the process changes, and use its output to update related skills.

## Related

[[skills-encode-lived-experience-not-obvious-behavior]], [[spec-developer-workflow-with-clarifying-questions]]
