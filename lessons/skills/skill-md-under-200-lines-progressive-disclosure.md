---
id: skill-md-under-200-lines-progressive-disclosure
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/simon-scrapes/how-to-use-claude-code-skills-like-the-1-it-s-easy-actually_20260307.txt
  - transcripts/simon-scrapes/the-claude-code-skills-trap-most-people-fall-for-this_20260307.txt
  - transcripts/simon-scrapes/every-level-of-claude-code-skills-in-27-mins_20260424.txt
  - transcripts/ray-amjad/anthropic-just-dropped-their-internal-skills-strategy_20260424.txt
  - transcripts/simon-scrapes/the-easiest-way-to-get-ahead-with-claude-code_20260424.txt
  - transcripts/ray-amjad/better-than-mcps-claude-code-s-new-skills-feature_20260307.txt
---

# Keep skill.md Under 200 Lines and Use Progressive Disclosure

## TL;DR

skill.md is a routing table, not a knowledge dump. Reference files load only when a step needs them, keeping context lean.

## Why it matters

Developers who put 1000+ lines into a single skill.md file find their context window exploding with 5,000-7,000 lines the moment multiple skills activate. Each activated skill competes for the same context window as the conversation. The 200-line limit is based on how much an LLM can efficiently scan to decide what to load next.

## How to apply

Structure each skill as: `skill.md` (≤200 lines: YAML frontmatter + step-by-step SOP) + `references/` folder (detailed knowledge, one file per topic) + `scripts/` (executable code) + `assets/`. In skill.md, write process steps that explicitly point to references only when needed (e.g., 'At step 2, load references/api-guide.md'). Claude can load and unload reference files between steps. The 15,000-character limit on all skill YAML descriptions across the entire system is a hard ceiling, install fewer, better-built skills.
