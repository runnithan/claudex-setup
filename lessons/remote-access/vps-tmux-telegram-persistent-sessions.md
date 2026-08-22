---
id: vps-tmux-telegram-persistent-sessions
created: 2026-06-11
status: active
supersedes: null
category: remote-access
sources:
  - transcripts/simon-scrapes/how-to-use-claude-code-anywhere-vps-u0026-mobile-setup_20260610.txt
---

# Run Claude Code on a VPS in tmux With a Telegram Bridge for Always-On Access

## TL;DR

Put Claude Code on a cheap Ubuntu VPS, keep the session alive in `tmux`, and pair the Telegram plugin so you can dispatch tasks from your phone while the work runs 24/7, independent of your laptop being awake.

## Why it matters

Local Claude Code dies when the machine sleeps. A VPS session in tmux persists across disconnects, and the Telegram pairing turns it into an always-on agent you can message from anywhere, a self-hosted alternative to `claude rc`/Channels that you fully control (~$17-20/mo).

## How to apply

1. Provision an Ubuntu VPS and connect via SSH (VS Code Remote works well).
2. Install Claude Code and clone your repo(s).
3. `tmux new-session -s agent`, then `cd ~/<project> && claude` inside it, detach freely; the session survives.
4. Install/configure the Telegram plugin (`/telegram configure <bot token>`), message the bot to pair, then lock pairing (`/telegram lock`) so no one else can pair with your bot.
5. Message the bot from your phone to queue tasks; reattach with `tmux attach -t agent` when you want the full terminal.
