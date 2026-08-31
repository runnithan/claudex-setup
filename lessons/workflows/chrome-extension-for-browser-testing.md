---
id: chrome-extension-for-browser-testing
created: 2026-04-25
status: active
supersedes: null
category: workflows
sources:
  - transcripts/ray-amjad/anthropic-just-connected-claude-code-to-your-browser_20260307.txt
  - transcripts/john-kim/his-claude-code-workflow-is-insane_20260307.txt
  - transcripts/john-kim/new-claude-code-updates-are-so-cool_20260424.txt
  - transcripts/john-kim/how-i-use-claude-code-meta-staff-engineer-tips_20260307.txt
---

# Use /chrome to Give Claude Live Browser Access for End-to-End Testing

## TL;DR

/chrome connects Claude to your Chrome browser, it sees console logs, takes screenshots, and can navigate pages for real UI verification.

## Why it matters

Asking Claude to verify UI changes without browser access forces it to guess or write tests it cannot run visually. With /chrome, Claude sees exactly what's happening in the browser including JavaScript errors, network failures, and rendering issues. Boris Cherniy's workflow uses Chrome extension verification as the final step before marking work complete.

## How to apply

Install the Claude Code Chrome extension from the official plugin marketplace. Type `/chrome` in your session to activate the connection. Claude can then: take screenshots, read console.log output, navigate URLs, click elements, and fill forms. Use after making UI changes: 'Can you open localhost:3000, click through the auth flow, and verify the error message appears correctly?' For thinking mode toggle: set 'left option key is meta' in terminal preferences, then use `alt+T` to toggle thinking mid-session.

## Related

[[set-option-as-meta-so-alt-t-toggles-thinking]]
