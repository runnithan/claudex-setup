---
id: teleport-sessions-between-cloud-web-and-terminal
created: 2026-06-21
status: active
supersedes: null
category: remote-access
source_type: post
sources:
  - https://x.com/bcherny/status/2038454339933548804
  - https://www.threads.com/@boris_cherny/post/DWfjo22FKJ4
---

# Use `/teleport` to Move a Running Session Between Cloud/Web and Your Terminal

## TL;DR

Run `claude --teleport` or `/teleport` to continue an already-running cloud/web session on your local machine (and push the other way) — start work on your phone in the morning and pick it up at your desk.

## Why it matters

This is distinct from the environment selector (which only chooses where a NEW task runs) and from remote-control (a phone window into a session that still runs locally). `/teleport` migrates a LIVE session bidirectionally between cloud/web and the terminal, enabling cross-device continuity without restarting context.

## How to apply

To continue a cloud/web session locally, run `claude --teleport` or `/teleport`. To drive a local session from your phone/web, use `/remote-control` (keep 'Enable Remote Control for all sessions' set in `/config`).

## Related

[[environment-switching-local-cloud-ssh]], [[remote-control-channels-for-phone-access]]
