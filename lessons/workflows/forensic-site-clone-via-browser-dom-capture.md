---
id: forensic-site-clone-via-browser-dom-capture
created: 2026-07-02
status: active
supersedes: null
category: workflows
sources:
  - transcripts/sean-kochel/steal-my-skill-for-making-pro-websites_dmwDN6Vsy-w_20260702.txt
---

# Clone a Site's Feel Forensically Via Browser Control, Not Screenshots

## TL;DR

To clone a site's feel, drive a real browser to capture per-scroll screenshots *plus* the downloaded DOM, loaded scripts, and animation libraries — screenshots alone leave the clone flat.

## Why it matters

Shallow top-level screenshots get a clone only ~70% there, missing the micro-interactions and animations that make a site feel special. Capturing the DOM and detecting which animation libraries load is what recovers the last 30%.

## How to apply

With Claude connected to Chrome (or any browser-control tool), run a multi-phase cloner: (1) scroll-by-scroll audit downloading DOM + scripts + animation libs + screenshots, (2) interview about your brand, (3) merge site-DNA + brand answers into a reusable *build prompt* (not direct code, so it stays tool-portable), (4) quality check, then a separate iterator that diffs reference vs implementation screenshots to close the final 20%.

## Related

[[chrome-extension-for-browser-testing]], [[visual-self-validation-screenshot-grading]], [[steal-designs-from-mobbin-with-color-constraint]]
