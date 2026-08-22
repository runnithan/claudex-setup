---
id: shared-brand-context-folder-for-all-skills
created: 2026-04-25
status: active
supersedes: null
category: configuration
sources:
  - transcripts/simon-scrapes/how-smart-people-are-using-claude-code-skills-to-automate-anything_20260424.txt
  - transcripts/simon-scrapes/the-easiest-way-to-get-ahead-with-claude-code_20260424.txt
  - transcripts/simon-scrapes/every-level-of-claude-code-skills-in-27-mins_20260424.txt
  - transcripts/simon-scrapes/the-claude-code-setup-nobody-shows-you-replaces-openclaw-hermes_20260424.txt
---

# Create One Shared Brand Context Folder That Every Skill References

## TL;DR

One source of truth for voice, ICP, and positioning means all skills sound like you, without pasting brand context into every prompt.

## Why it matters

Without shared context, every skill starts from zero. Your copywriting skill doesn't know what your research skill found. Update your brand positioning once and every skill that references the shared folder benefits immediately. This is the difference between a collection of isolated tools and a system that sounds like you.

## How to apply

Create `.claude/brand-context/` with lean files: `voice-profile.md` (50-100 lines max), `icp.md`, `positioning.md`, `samples.md` (examples of your best outputs), `assets.md` (links, handles, visual references). In each skill.md, add a context-needs section that specifies which brand context files to load at which steps: 'At step 3 (drafting), load brand-context/voice-profile.md for tone guidance.' Update brand-context files in one place; all skills inherit the update automatically.
