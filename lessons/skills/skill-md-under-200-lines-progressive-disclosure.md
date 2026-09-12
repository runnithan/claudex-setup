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

SKILL.md is a routing table, not a knowledge dump: keep it under ~200 lines with reference files that load only when a step needs them, and run the same 200-line refactor over every marketplace skill you install (a 60% reduction is typical, and no domain knowledge is lost because it moves to references/).

## Why it matters

Developers who put 1000+ lines into a single skill.md find their context window exploding with 5,000 to 7,000 lines the moment several skills activate, because each activated skill competes for the same window as the conversation. The 200-line limit is based on how much an LLM can efficiently scan to decide what to load next.

Downloaded skills have the same problem from the other direction. Most marketplace skills are built to be comprehensive, not context-efficient, so a 400-line skill.md loads all 400 lines every time it activates. Refactoring it to 200 lines with proper references cuts context consumption by 60% or more without losing any domain knowledge, which moves into reference files.

## How to apply

Structure each skill as `skill.md` (200 lines or fewer: YAML frontmatter plus the step-by-step SOP) plus a `references/` folder (detailed knowledge, one file per topic), `scripts/` (executable code) and `assets/`. Write process steps that point at references only when needed ("at step 2, load references/api-guide.md"), so Claude can load and unload them between steps.

Give every skill you install the same treatment. Install it locally first (`claude install --local <github-url>`), then trigger the Skill Creator: "Take the [skill-name] skill and use the Skill Creator skill to refactor it. I want the skill.md to be max 200 lines and all reference information should go into the references folder." Review what changed, the Skill Creator reports the line-count reduction and the new reference files, then verify the skill still activates properly and that its description was improved as part of the refactor.

Remember the other half of the budget: the 15,000-character ceiling on all skill YAML descriptions across the system is a hard one, so install fewer, better-built skills.

## Related

[[skill-descriptions-share-a-15000-character-ceiling]], [[separate-skill-md-from-references-to-localize-debugging]], [[curate-a-bulk-skill-pack-before-installing-not-after]]
