---
id: convert-docs-to-markdown-before-feeding-claude
created: 2026-06-27
status: active
supersedes: null
category: context-management
sources:
  - transcripts/nate-herk-ai-automation/how-to-never-hit-your-claude-session-limit-again__qZvORxGqI0_20260624.txt
---

# Convert HTML/PDF/DOCX to Markdown Before Feeding Documents to Claude

## TL;DR

Markdown carries none of the layout, metadata, and formatting noise of HTML/PDF/DOCX, so the same document costs dramatically fewer tokens — convert documents to markdown before pasting them into context.

## Why it matters

HTML tags, PDF layout streams, and DOCX XML all tokenize into large amounts of noise that crowd out the actual content and shorten effective session life. Plain markdown is mostly signal, so a document fed as markdown leaves far more window for the work itself.

## How to apply

Run source files through a converter (Docling, markitdown, pandoc, or an equivalent) to produce clean markdown before handing them to Claude. Reserve OCR for genuinely scanned material; if the source is already digital text, straight conversion is enough.

## Related

[[context-auditing-slash-context]]
