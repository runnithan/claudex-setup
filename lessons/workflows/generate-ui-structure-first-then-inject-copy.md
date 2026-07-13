---
id: generate-ui-structure-first-then-inject-copy
created: 2026-07-02
status: active
supersedes: null
category: workflows
sources:
  - transcripts/sean-kochel/this-tool-makes-professional-design-look-easy_crZwPE6aEqk_20260702.txt
  - transcripts/sean-kochel/google-stitch-antigravity-never-hire-a-designer_NprG-SGd4-A_20260702.txt
  - transcripts/sean-kochel/vibe-designing-with-google-stitch-just-got-a-10x-upgrade_Seub7NNBF8g_20260702.txt
---

# Generate UI Structure First, Inject Real Copy on a Second Pass

## TL;DR

When generating designs, prompt the overall layout and style first, then add real copy in a separate pass — working screen-by-screen instead of dumping the whole spec at once.

## Why it matters

Handing an AI design tool the full spec and all copy up front reliably yields mid-tier designs. Staged, small, contained prompts produce noticeably better output; this is the documented best practice across Stitch, Polymet, and similar tools.

## How to apply

Pass 1: generate the scaffold and aesthetic (headline, subhead, CTA, section layout) with placeholder intent. Pass 2: paste the actual research-derived copy to fill it in while preserving the style. Build one screen or component per prompt rather than the entire app in a single request.

## Related

[[ux-spec-stage-between-prd-and-build]], [[design-tool-mcp-for-design-as-code-builds]], [[treat-ai-junior-dev-specific-tight-context]]
