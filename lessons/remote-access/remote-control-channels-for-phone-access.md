---
id: remote-control-channels-for-phone-access
created: 2026-04-25
status: active
supersedes: null
category: remote-access
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-that-kills-openclaw_20260307.txt
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-everyone-asked-for_20260307.txt
  - transcripts/simon-scrapes/claude-code-just-went-mobile-remote-control-vs-openclaw_20260307.txt
  - transcripts/simon-scrapes/the-only-claude-code-updates-you-need-to-know-apr-2026_20260424.txt
  - transcripts/john-kim/new-claude-code-updates-are-so-cool_20260424.txt
---

# Use Remote Control or Channels to Send Tasks from Phone

## TL;DR

`claude rc` gives browser/phone access to your running session; Channels connects Telegram/iMessage/Discord as two-way interfaces.

## Why it matters

Remote control lets you review outputs, send prompts, and check session status without sitting at the terminal, critical for long-running autonomous sessions. Channels enables bidirectional communication through apps you already use, including receiving events from external tools (payment failures, form submissions) that trigger Claude automatically.

## How to apply

For remote control: type `/remote control` or `claude rc` in your session. Scan the QR code or visit the URL on your phone. The session runs locally on your machine; the phone is just a window into it. One remote connection per instance; session persists ~10 minutes if laptop sleeps. For channels: go to `/config`, enable channels, then connect Telegram, iMessage, or Discord following the 5-minute setup. For security: use with sandbox mode or on a VPS for always-on deployments. External tools can push events into Claude via the same channels infrastructure.
