---
id: html-as-default-artifact-not-markdown
created: 2026-07-02
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://www.lennysnewsletter.com/p/html-is-the-new-markdown-how-anthropic
  - https://x.com/trq212/status/2052809885763747935
---

# Default to HTML (Not Markdown) for Plans, Code Reviews, and Design Systems

## TL;DR

Have Claude produce plans, code reviews, reports, and design systems as interactive HTML artifacts instead of Markdown — richer visuals drive better human review and better products.

## Why it matters

Thariq Shihipar (Claude Code, Anthropic) says Anthropic switched its internal default from Markdown to HTML for planning/communication artifacts because "richer visual formats lead to better human engagement—and, ultimately, better products," arguing "99% of your AI-generated tokens should go to planning, interfaces, and communication—not production code." Markdown is the low-effort format agents fall back to; HTML lets Claude build interactive specs, throwaway micro-UIs to edit parts of a plan, and a living design system that travels with the repo. Complementary to [[convert-docs-to-markdown-before-feeding-claude]] — that lesson is about documents you feed Claude (cheaper input tokens); this is about artifacts Claude produces for you to review.

## How to apply

Ask Claude to write plans/specs, code-review summaries, and reports as a single self-contained HTML file instead of `.md`; request interactive elements (throwaway micro-UIs) to edit specific parts of a plan; keep a living design system in HTML checked into the repo so it travels with every project; then convert the HTML plan directly into the implementation. See also [[interactive-html-artifacts-for-design-decisions]] for the design-variation case.
