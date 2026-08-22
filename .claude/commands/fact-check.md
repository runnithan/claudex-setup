---
description: "Verify claims in content by searching for sources. Use when user says /fact-check followed by content to verify."
argument-hint: "[content-to-verify]"
---

Review the following content and fact-check every factual claim:

$ARGUMENTS

For each claim:
1. Identify the specific factual assertion
2. Search the web for verification using authoritative sources
3. Classify as Verified, Unverified, or Incorrect

Output a markdown table:

| # | Claim | Status | Source / Notes |
|---|-------|--------|----------------|
| 1 | ... | Verified / Unverified / Incorrect | Link or explanation |

After the table, provide a summary: X/Y claims verified, any corrections needed.

If no arguments are provided, ask the user to paste or describe the content they want fact-checked.
