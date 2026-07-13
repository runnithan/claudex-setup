---
id: automode-classify-all-shell
created: 2026-07-02
status: active
supersedes: null
category: permissions
source_type: canonical
sources:
  - https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
---

# Set autoMode.classifyAllShell to Run Every Shell Command Through the Auto-Mode Classifier

## TL;DR

By default auto mode only classifies shell commands matching arbitrary-code-execution patterns; set `autoMode.classifyAllShell` to route all Bash/PowerShell commands through the classifier for stricter unattended safety.

## Why it matters

The 2.1.193 changelog added `autoMode.classifyAllShell` "to route all Bash/PowerShell commands through the auto-mode classifier instead of only arbitrary-code-execution patterns." The default leaves a gap: shell commands that don't look like code execution are auto-approved without classification, which matters for unsupervised runs.

## How to apply

In settings.json set `autoMode.classifyAllShell: true` for autonomous/headless sessions where you want every shell invocation vetted; leave it off for interactive work where the extra classification latency isn't worth it. Pair with [[auto-mode-blocks-destructive-commands-unless-you-ask]] for defense in depth.
