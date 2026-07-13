---
id: otel-logs-assistant-responses-on-upgrade
created: 2026-07-02
status: active
supersedes: null
category: settings
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# After Upgrading, Set OTEL_LOG_ASSISTANT_RESPONSES=0 or Telemetry Starts Logging Response Text

## TL;DR

The new `claude_code.assistant_response` OTEL log event contains the model's full response text and, if you already log user prompts, it turns on automatically after upgrading — set `OTEL_LOG_ASSISTANT_RESPONSES=0` to keep telemetry prompts-only.

## Why it matters

The 2.1.193 changelog warns this event "follows `OTEL_LOG_USER_PROMPTS`, so deployments that already log prompt content will start receiving response content on upgrade." Teams with OTEL pipelines can silently begin shipping generated code / response text to their logging backend — a real data-governance leak.

## How to apply

If you run Claude Code with OpenTelemetry logging and have `OTEL_LOG_USER_PROMPTS` enabled, explicitly set `OTEL_LOG_ASSISTANT_RESPONSES=0` before/at upgrade to stay prompts-only; set `=1` only if you intend to capture response text and your log store is cleared for it.
