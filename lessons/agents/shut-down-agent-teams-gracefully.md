---
id: shut-down-agent-teams-gracefully
created: 2026-06-27
status: active
supersedes: null
category: agents
sources:
  - transcripts/nate-herk-ai-automation/how-to-build-claude-agent-teams-better-than-99-of-people_vDVSGVpB2vc_20260621.txt
---

# Shut Down Agent Teams Gracefully — Ask Teammates to Save First, Don't Force-Kill

## TL;DR

When ending an agent-team session, send each teammate a 'save your work and confirm when ready' message and wait for the confirmation, rather than force-killing them mid-task.

## Why it matters

Force-closing teammates while they're working can strand uncommitted changes, partial files, and unsaved state. A graceful shutdown request lets each agent reach a clean stopping point and commit, preventing lost or orphaned work.

## How to apply

Before closing the team, have the coordinator broadcast a shutdown request ('You're done — save and commit your work, confirm when ready'), then close only after every teammate confirms. Treat this as the standard end-of-session ritual for any multi-agent run.

## Related

[[agent-teams-for-cross-domain-collaboration]], [[agent-teams-agent-should-not-touch-same-files]]
