---
id: supabase-mcp-for-backend-sync
created: 2026-04-25
status: active
supersedes: null
category: configuration
sources:
  - transcripts/andrew-codesmith/how-i-code-profitable-apps-solo-beginner-step-by-step-best-tools_20260307.txt
  - transcripts/andrew-codesmith/master-95-of-claude-code-in-15-mins-as-a-beginner_20260424.txt
---

# Use the Supabase MCP Server to Sync Your Database Schema Without Manual Queries

## TL;DR

With Supabase MCP connected, Claude can query schema, inspect tables, and sync backend to code with a few prompts, read-only key recommended.

## Why it matters

Without MCP, Claude writes database queries blindly and must be told the schema explicitly in every session. With Supabase MCP, Claude can inspect the actual tables and relationships in real time. For mobile app development, this means syncing the backend data model to the app's TypeScript types happens in a few prompts instead of a manual process.

## How to apply

Add Supabase to your MCP config in settings.json with your project URL and service role key (or ideally a read-only key). For the initial sync: 'Using the Supabase MCP, can you examine my database schema and generate the TypeScript types that match my tables?' For ongoing work: Claude reads schema on demand and writes queries that match the actual structure. Always use a read-only API key unless the task explicitly requires writes, the MCP has full access to everything the key allows.
