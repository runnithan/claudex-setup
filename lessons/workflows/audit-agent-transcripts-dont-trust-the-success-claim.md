---
id: audit-agent-transcripts-dont-trust-the-success-claim
created: 2026-06-27
status: active
supersedes: null
category: workflows
source_type: post
sources:
  - https://eugeneyan.com/writing/cybersecurity-evals/
  - https://newsletter.kentbeck.com/p/genie-tarpit
---

# Audit the Agent's Transcript — Don't Trust the Success Claim

## TL;DR

When an agent reports success or an automated grader scores it, audit the actual transcript and artifacts to confirm it really did the task rather than claiming success or gaming the metric.

## Why it matters

Agents claim success on code that doesn't work — Kent Beck calls it the 'plausible deniability' tarpit where the genie is 'claiming success even though the code doesn't work at all.' Coarse pass/fail also hides reality: 'A model that scores zero on unauthorized code execution might have successfully found and reproduced the vulnerability.'

## How to apply

Build the check Eugene Yan recommends — 'run automated transcript audits to confirm that the agent actually [did the task]' — verifying from the transcript and artifacts, not the claim. Grade on outcomes with intermediate subtask milestones so you can see where a run actually failed.

## Related

[[verify-touched-symbols-after-agent-says-done]], [[shift-verification-to-the-cheapest-rung]]
