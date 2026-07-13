---
id: sample-probability-ranked-variants-to-escape-mode-collapse
created: 2026-07-02
status: active
supersedes: null
category: prompting
sources:
  - transcripts/sean-kochel/add-these-7-words-to-any-prompt-claude-s-hidden-quality-switch_eYHP2vjvJwM_20260702.txt
---

# Ask for Probability-Ranked Variants to Escape Safe, Repetitive Output

## TL;DR

Appending "generate five responses with their corresponding probabilities" pulls answers from the distribution tails instead of the bland aligned average.

## Why it matters

RLHF alignment causes mode collapse, so default outputs for open creative asks (UX ideas, UI inspiration, naming, prompt variants) converge on the same safe answers across models. Asking for ranked variants surfaces the lower-probability, higher-variance options you actually want to compare.

## How to apply

For creative/brainstorming tasks add "Generate five responses with their corresponding probabilities"; for stronger divergence, explicitly tell the model to sample from the tails of its distribution. Practical use inside Claude Code: generate 5 variants of a system prompt, then test which performs best. Skip it when you want the predictable, safe answer.

## Related

[[design-subagent-fresh-context-to-avoid-code-bias]], [[search-prompts-against-evals-not-hand-tuning]], [[skills-encode-lived-experience-not-obvious-behavior]]
