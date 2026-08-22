---
id: google-workspace-cli-for-native-google-integration
created: 2026-04-25
status: active
supersedes: null
category: configuration
sources:
  - transcripts/simon-scrapes/claude-code-2-0-has-arrived-it-s-insane_20260424.txt
  - transcripts/simon-scrapes/the-only-claude-code-updates-you-need-to-know-apr-2026_20260424.txt
---

# Use Google Workspace CLI to Give Claude Full Google Ecosystem Access

## TL;DR

Google's open-source CLI gives Claude access to Drive, Gmail, Calendar, Docs, Sheets, and Slides via bash, properly formatted, not raw markdown.

## Why it matters

Previous Google integrations via MCP produced documents with raw markdown formatting that needed API calls to clean up. The official Google Workspace CLI runs bash commands that talk directly to Google's native formatting layer, producing properly formatted documents with headers, images, and links from day one.

## How to apply

Install: run the Google CLI install command in your terminal or tell Claude to set it up and guide you through the authentication process. The CLI includes 100+ pre-built recipes for common operations. To use in a skill: add the CLI commands as scripts in the skill's scripts folder. For example, a content skill's final step: 'Run `gws docs create --title [title] --content [markdown-file]` to publish the formatted document.' Google considers this a beta product but it is functionally stable.
