# Transcript fetch throttling — tuning notes & backlog

How `scripts/fetch_transcripts.py` stays under YouTube's per-IP anti-bot
throttle, and the ranked options for when it isn't enough. Researched 2026-06-20.

## Context

The fetcher uses `youtube-transcript-api`, which scrapes YouTube's **unofficial**
`timedtext` (caption) endpoint — there is **no official API key or documented
quota**. The constraint is YouTube's undocumented **per-IP throttling**, surfaced
as `RequestBlocked` / `IpBlocked`. Key facts:

- Each video ≈ **4 requests** (one watch-page GET for metadata + the library's 3
  internal calls). So an unspaced run of N videos fires ~4N requests in a tight
  burst — and **the burst is what trips the throttle**, not the daily total.
- A **residential home IP is the best case**; cloud/datacenter IPs get blocked on
  request #1 by ASN reputation. **Never route this through a cloud host.**
- The caption endpoint got **much stricter and fingerprint-sensitive in mid-2025**.
- No published threshold exists. The most reliable number is this IP's own
  observed ceiling: **~30 *unspaced* fetches before blocking**.
- Sub-daily cadence is a known trap for this IP: running every 3h kept it "warm"
  and the throttle never cleared. **Daily runs let the per-IP window reset.**

## Current settings

Applied 2026-06-20:

- `MAX_TRANSCRIPTS_PER_RUN = 40` (was 25).
- Randomised **4–8s gap before each networked fetch** (`FETCH_SLEEP_MIN/MAX`),
  jittered because a fixed cadence is itself a fingerprint. Spreads a run over
  minutes so it no longer bursts — 40 spaced is gentler than the old unspaced 25.
- Daily cadence unchanged; 3-strike circuit breaker stops a run if blocks recur
  (≈ a 24h backoff, which is the correct response to a flag).

Applied 2026-07-01 (escalation, option #2 below):

- **TLS/browser impersonation via `curl_cffi`.** The pacing above bought clean
  runs for a week (2026-06-28 pulled a full 40 with 0 blocks) but then the IP
  flagged and **three consecutive runs (06-29 → 07-01) fetched 0** — the breaker
  tripped on the first videos each time, i.e. a fingerprint flag the daily window
  no longer cleared, exactly the "≥3/run → escalate" trigger. `_TimeoutSession`
  now subclasses `curl_cffi.requests.Session` and sends every request with
  `impersonate="chrome"`, replaying a real Chrome TLS handshake. Smoke-tested on
  the still-flagged IP: two known-captioned videos fetched cleanly in ~1.6s each.
  Note: curl_cffi's request exceptions do **not** subclass `requests`', so
  `fetch_transcript` catches `curl_cffi...RequestException` explicitly (else a
  hard block would fall through to the generic skip and never trip the breaker).
- Error handling already matches the library taxonomy: `RequestBlocked`/
  `IpBlocked`/`YouTubeRequestFailed` retry next run; `TranscriptsDisabled`/
  `NoTranscriptFound`/`VideoUnavailable`/`PoTokenRequired` are permanent skips
  recorded in `no-transcript-available.md`.

## Conditional backlog — apply based on results

**Decision rule:** watch the "Blocked (throttled…)" count in `transcripts/.pipeline.log`
over a few daily runs. **~0–1/run → do nothing.** **≥3/run (breaker tripping early)
→ escalate down this list.**

1. **Measure first (default).** This IP's own behaviour beats the low-confidence
   public numbers. Don't change anything until the data says to.
2. ✅ **APPLIED 2026-07-01 — TLS/browser impersonation via `curl_cffi`** — the
   clearest firsthand throttle mitigation found (the caption endpoint fingerprints
   the TLS handshake). `_TimeoutSession` now subclasses `curl_cffi.requests.Session`
   and sets `impersonate="chrome"` per request. Added `curl-cffi>=0.15.0` to the
   dev deps + `.venv-linux`. **If blocks recur even with impersonation, try a
   different `impersonate` target (e.g. a pinned `chrome124`) before escalating to
   the proxy below.**
3. **Consent cookie on `fetch_page_metadata`** (data-quality, throttle-independent)
   — it uses bare `urllib` with no consent cookie and sometimes mislabels videos
   as `unknown-creator/`; add `Cookie: SOCS=CAI; CONSENT=YES+1` (same fix already
   in `update_urls.py`). One line, zero risk. **Do anytime.**
4. **Webshare free rotating-residential proxy** (speed escape hatch) — natively
   supported via `WebshareProxyConfig` (`retries_when_blocked` default 10); free
   1 GB tier likely covers a whole backlog (transcripts are tiny), drains in one
   run, home IP untouched. Needs a signup + a gitignored secret. **Only if daily
   cadence is too slow.**

## Explicitly skipped (with reasons)

- **Dead retry path** (`TRANSCRIPT_RETRIES=1` → the in-fetch retry never fires) —
  harmless; next-run retry already covers blocked videos.
- **Deduping the redundant watch-page fetch** — ~25% fewer requests, but only to
  the lightly-throttled *page* endpoint, not the caption endpoint. Low payoff.
- **Cookie auth** — broken upstream in the library.
- **Official YouTube Data API v3** — a dead end: `captions.download` only works
  for videos the authenticated user **owns**, useless for third-party channels.
