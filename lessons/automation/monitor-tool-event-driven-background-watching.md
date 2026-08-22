---
id: monitor-tool-event-driven-background-watching
created: 2026-04-25
status: active
supersedes: null
category: automation
sources:
  - transcripts/ray-amjad/claude-code-just-shipped-the-monitor-tool_20260424.txt
---

# Use the Monitor Tool for Event-Driven Background Process Watching

## TL;DR

Monitor streams events from background processes to Claude; tokens are used only when filtered events fire, not continuously.

## Why it matters

/loop is time-driven (full API call every N minutes even if nothing happened). The Monitor tool is event-driven: a filter script only emits when something relevant occurs, consuming zero tokens between events. For a running test suite, Monitor notifies Claude of each failing test as it fails, enabling immediate diagnosis rather than waiting for all 47 tests to finish.

## How to apply

Tell Claude: 'Start the development server and watch for errors while I work on the auth feature.' Claude sets up a monitor that runs `npm run dev` and filters for error/warn/failed events. Each matched line is one event delivered to the main session. For persistent watches: specify `persistent: true`. Two types: (1) stream filter, log tailing for real-time events (dev server, test runner); (2) poll & diff filter, check an API endpoint at intervals, deliver only when threshold is met (e.g., stock price drops below X). Use for: Vercel deploy monitoring, production error rate spikes, file-drop watchers, test suites.
