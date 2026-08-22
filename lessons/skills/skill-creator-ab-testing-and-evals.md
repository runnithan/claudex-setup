---
id: skill-creator-ab-testing-and-evals
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-claude-code-skills-2-0_20260307.txt
  - transcripts/simon-scrapes/claude-code-2-0-has-arrived-it-s-insane_20260424.txt
  - transcripts/simon-scrapes/build-self-improving-claude-code-skills-the-results-are-crazy_20260424.txt
  - transcripts/simon-scrapes/every-level-of-claude-code-skills-in-27-mins_20260424.txt
---

# Use the Skill Creator's Eval System to Test and A/B Compare Skills

## TL;DR

Run 5 parallel agents against binary assertions to score skill output; A/B test reference files before deciding what to keep.

## Why it matters

Without evals, skill improvement is vibes-based, you have no way to know if removing a reference file hurt quality or helped it. Skills 2.0 introduced built-in evaluation that spawns parallel runs, scores each against your criteria, and generates an HTML report with pass/fail breakdowns and token benchmarks.

## How to apply

Trigger the Skill Creator skill and say: 'Run a new test optimized for [specific reference file or criterion]. Measure: [3-5 binary assertions]. Test on [this task] 5 times.' Use binary assertions only (true/false, not subjective): 'Does not contain m-dashes', 'Under 300 words', 'Final line is not a question'. To A/B test: 'Run this same task 5 times with the skill and 5 times without the copywriting skill.' Review the HTML dashboard for per-run grades and the benchmark for token/time tradeoffs.
