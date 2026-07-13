---
id: sast-scan-to-fix-command-loop
created: 2026-07-02
status: active
supersedes: null
category: workflows
sources:
  - transcripts/sean-kochel/the-one-ai-tool-you-need-before-you-ship-your-app_VFYrBEkEVsw_20260702.txt
---

# Pipe SAST Findings Into a Fix Command, Then Re-Scan to Verify

## TL;DR

Scan AI-generated code with a SAST tool (e.g. Semgrep against the OWASP Top 10), export the findings, feed them to a structured fix command, then re-scan to confirm zero findings.

## Why it matters

AI coding takes shortcuts that open real holes a beginner won't spot manually: hardcoded secrets, missing authorization (vs just authentication), CORS set to `*`, debug mode left on, compromised npm deps, TypeScript coerced to `any`. A deterministic scanner catches what LLM self-review misses.

## How to apply

Run the scanner locally (e.g. `semgrep ci`) and/or as a pre-push GitHub gate. Export the findings as CSV into the repo, then invoke a custom slash command or agent definition that ingests the findings file, prioritizes, and fixes each issue. Commit and re-run the scan to confirm zero findings before shipping. Many scanners also expose an MCP server for in-IDE use.

## Related

[[encode-agent-mistakes-as-lint-rules-with-the-fix-in-the-message]], [[shift-verification-to-the-cheapest-rung]], [[harden-always-on-agents-least-privilege-and-capable-models]]
