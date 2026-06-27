---
id: give-agents-a-local-mock-dev-env-instead-of-prod-credentials
created: 2026-06-27
status: active
supersedes: null
category: permissions
source_type: post
sources:
  - https://www.latent.space/p/cognition
---

# Give Agents a Local Mock Dev Environment Instead of Production Credentials

## TL;DR

Provision a local stack — Docker Compose, a local Postgres, mock external APIs — for the agent to run against, so it never needs real production credentials.

## Why it matters

An agent with production credentials is a blast-radius problem: a compromised or wayward run can touch real data and systems. Cognition's Walden Yan: 'You probably do want a local DB setup, a local Docker Compose and Postgres... so that you don't need to give your agent any crazy product credentials.' Environment design, not permission prompts, should prevent this.

## How to apply

Before pointing an agent at a service-backed task, spin up local fakes (Compose DB, mock APIs) and feed only those connection strings; keep real secrets out of the agent's environment entirely.

## Related

[[contain-agents-at-environment-layer-not-permission-prompts]], [[keep-credentials-out-of-the-agent-sandbox]]
