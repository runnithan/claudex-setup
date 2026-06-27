---
id: tell-the-agent-the-final-deployment-url-up-front
created: 2026-06-27
status: active
supersedes: null
category: prompting
source_type: post
sources:
  - https://simonwillison.net/2026/Jun/22/porting-moebius/
---

# Tell the Agent the Final Deployment URL Up Front

## TL;DR

When the agent builds something you intend to deploy, give it the exact production URL at the start so it gets asset paths, base hrefs, and demo links right the first time instead of needing post-deploy patches.

## Why it matters

Generated code that constructs or hardcodes URLs breaks when moved to its real host. Simon Willison: 'Telling it the final URL was important in case it needed to fix the URLs in the demos that it was building so they would work when deployed to production.'

## How to apply

Put the destination in the prompt rather than leaving it implicit (e.g. 'publish so that https://user.github.io/repo/ serves the UI'), and pair it with an early 'tell me what URL I can visit to try this' so you can validate links before the real deploy.

## Related

[[readme-driven-development-into-claude-code]]
