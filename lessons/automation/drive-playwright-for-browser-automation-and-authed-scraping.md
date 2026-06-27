---
id: drive-playwright-for-browser-automation-and-authed-scraping
created: 2026-06-27
status: active
supersedes: null
category: automation
sources:
  - transcripts/nate-herk-ai-automation/claude-code-playwright-automates-literally-anything_J-6pnl5DQg8_20260626.txt
---

# Drive Playwright From Claude for Self-Healing Browser Automation and Authenticated Scraping

## TL;DR

Give Claude access to Playwright so it can drive a real browser end-to-end — fill forms, screenshot, and self-correct when the UI changes — and launch it with your existing Chrome user-profile to inherit logged-in sessions for authenticated tasks.

## Why it matters

Manual QA and authenticated scraping are slow and brittle. An agent with Playwright can run a flow, catch failures via screenshots, and iterate without you. Pointing it at your real Chrome profile means first-run manual login, then instant stateful runs after — no re-auth, no fighting 2FA/CAPTCHA each time.

## How to apply

Install Playwright and ask Claude to build and run a flow ('test this signup end-to-end, fix bugs, iterate until it passes'). For authed targets, configure Playwright to launch with your Chrome profile path; log in once headed, then run headless against persisted cookies. Distinct from /chrome live testing — this is programmatic, scriptable automation.

## Related

[[chrome-extension-for-browser-testing]], [[visual-self-validation-screenshot-grading]]
