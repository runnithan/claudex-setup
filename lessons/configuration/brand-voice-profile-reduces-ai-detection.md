---
id: brand-voice-profile-reduces-ai-detection
created: 2026-06-07
status: active
supersedes: null
category: configuration
sources:
  - transcripts/simon-scrapes/i-taught-claude-code-to-build-you-a-personal-brand-watch-this_20260607.txt
---

# Build a Brand Voice Profile From Real Examples So Output Sounds Like You, Not AI

## TL;DR

Extract your actual voice through personality/stance questions plus 3–5 real writing samples; Claude generates content that sounds authentically yours and reads less like AI slop.

## Why it matters

Generic AI content is instantly recognizable. When Claude knows your actual voice, personality-driven style, word choices, real examples, outputs feel personal and score lower on AI detection. This is the construction recipe behind `shared-brand-context-folder-for-all-skills`: that lesson says *have* one voice source of truth; this one says *how to build it*.

## How to apply

(1) Answer personality questions (do you have an anti-corporate stance? how do you naturally respond to problems?). (2) Describe your strategic framework (ICP, tone, values). (3) Collect 3–5 real examples: podcast transcripts of you, LinkedIn posts, blog posts or emails you actually sent. (4) Have Claude extract patterns into a `voice-profile.md`. (5) Reference this file whenever asking Claude to write content.
