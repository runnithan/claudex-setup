#!/usr/bin/env python3
"""
YouTube Transcript Fetcher for Claude Code
==========================================
Pulls transcripts from YouTube videos and saves them as .txt files
organised by creator, so Claude Code can ingest them as knowledge.

Usage:
    1. Add URLs to .claude/transcripts/urls.txt (one per line)
    2. Run from backend/: cd backend && uv run python ../.claude/scripts/fetch_transcripts.py

Output:
    .claude/transcripts/<creator_name>/<title-slug>_<date>.txt
    .claude/transcripts/index.md  (auto-updated manifest of all transcripts)

Dependency:
    youtube-transcript-api (add to pyproject.toml dev dependencies, then uv sync)
"""

import json
import os
import random
import re
import sys
import urllib.request
import threading
import time
from datetime import datetime
from html import unescape
from pathlib import Path

try:
    # curl_cffi replaces plain `requests` for the transport so we can replay a
    # real browser's TLS handshake (see _TimeoutSession). Its request exceptions
    # do NOT subclass requests', so we import the base to catch them explicitly.
    from curl_cffi import requests as cffi_requests
    from curl_cffi.requests.exceptions import RequestException as CurlRequestException
    from youtube_transcript_api import (
        YouTubeTranscriptApi,
        # Permanent: the video genuinely has no fetchable transcript. Recording
        # these lets us skip them forever instead of re-attempting every run.
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
        VideoUnplayable,
        AgeRestricted,
        InvalidVideoId,
        PoTokenRequired,
        # Transient: YouTube is throttling/blocking this IP. Worth retrying, so
        # these are treated like a timeout (never recorded as "no transcript").
        RequestBlocked,  # IpBlocked subclasses this
        YouTubeRequestFailed,
    )
except ImportError as e:
    print(f"Missing dependency: {e.name}")
    print("Install into the runtime venv with:")
    print("  uv pip install --python .venv-linux/bin/python curl_cffi youtube-transcript-api")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
TRANSCRIPTS_DIR = SCRIPT_DIR.parent / "transcripts"
URLS_FILE = TRANSCRIPTS_DIR / "urls.txt"
# Markdown ledger of videos that have no fetchable transcript (subtitles
# disabled, none found, unavailable, ...). Read on every run to skip them, and
# appended to when a new permanent failure is seen. Tracked in git as a record;
# titles are clickable so you can watch them manually if you want.
NO_TRANSCRIPT_FILE = TRANSCRIPTS_DIR / "no-transcript-available.md"

# A permanent "no transcript" result — record and never retry.
PERMANENT_ERRORS = (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    VideoUnplayable,
    AgeRestricted,
    InvalidVideoId,
    PoTokenRequired,
)
# A transient block (IP throttling). Retry next run; counts toward the breaker.
TRANSIENT_ERRORS = (RequestBlocked, YouTubeRequestFailed)

# Rough token estimate: ~1 token per 0.75 words for English text
TOKEN_RATIO = 1 / 0.75

# Network safety: YouTube throttles the transcript endpoint for IPs that pull
# many transcripts. A throttled response can trickle bytes slowly, so requests'
# socket timeout (which only bounds time *between* bytes) won't break out. We
# therefore put a hard WALL-CLOCK deadline around the whole fetch, plus a socket
# timeout as a first line of defence, and treat overruns/connection errors as
# "blocked" so the caller can stop early instead of grinding.
TRANSCRIPT_TIMEOUT = 12   # socket timeout, seconds per HTTP request
TRANSCRIPT_DEADLINE = 20  # hard wall-clock cap on a whole fetch attempt
TRANSCRIPT_RETRIES = 1    # attempts per video (failures retry next run anyway)

# Rate limiting: fetch at most this many NEW transcripts per run, then stop, so
# we stay under YouTube's per-IP transcript limit. See
# references/transcript-fetch-throttling.md for the full rationale and the
# conditional backlog of mitigations (impersonation, proxy) to apply if blocks
# recur. The job runs once a day, so
# the rate-limit window fully resets between runs (running more often — e.g.
# every 3h — kept the IP "warm" and the throttle never cleared). Fetches within
# a run are spaced by a randomised gap (see FETCH_SLEEP_* below), so a run no
# longer fires its ~4-requests-per-video in one tight burst — that burst was the
# throttle trigger (observed ~30 *unspaced* fetches before IP-blocking). With
# spacing, 40 spread over several minutes is gentler than the old unspaced 25.
# The block-counter breaker still stops early if throttling starts sooner.
# Override with env var MAX_TRANSCRIPTS_PER_RUN.
def _env_int(name: str, default: int) -> int:
    """Parse an int env var, falling back to default on any invalid value so a
    bad override can't crash the whole pipeline at import time."""
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _env_float(name: str, default: float) -> float:
    """Parse a float env var, falling back to default on any invalid value."""
    try:
        return float(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


MAX_PER_RUN = _env_int("MAX_TRANSCRIPTS_PER_RUN", 40)

# Inter-fetch spacing: sleep a randomised gap before each networked fetch so a
# run is spread over minutes instead of one burst. The gap is *randomised* on
# purpose — a fixed cadence is itself a bot fingerprint. Skipped videos (already
# fetched / known no-transcript) don't reach this, so they cost no time. Tune or
# disable via env (set FETCH_SLEEP_MAX=0 to turn spacing off).
FETCH_SLEEP_MIN = _env_float("FETCH_SLEEP_MIN", 4)
FETCH_SLEEP_MAX = _env_float("FETCH_SLEEP_MAX", 8)


class TranscriptBlocked(Exception):
    """Raised when a transcript request times out / is refused (vs. a video
    that simply has no transcript). Signals likely IP throttling."""


# The caption endpoint fingerprints the TLS/JA3 handshake (much stricter since
# mid-2025): a plain-`requests` handshake reads as a bot no matter how gently we
# pace, and once the IP is flagged the daily window stops clearing it. curl_cffi
# replays a real Chrome's handshake + default headers so the request looks
# browser-originated. See references/transcript-fetch-throttling.md.
_IMPERSONATE = "chrome"


class _TimeoutSession(cffi_requests.Session):
    """curl_cffi Session that (a) impersonates a real Chrome so the caption
    endpoint's TLS-fingerprint check passes and (b) applies a default timeout so
    a stalled endpoint raises instead of hanging forever. Both defaults are set
    per-request (not on the constructor) so they hold whichever verb the library
    calls and stay robust across curl_cffi versions."""

    def __init__(self, timeout=TRANSCRIPT_TIMEOUT):
        super().__init__()
        self._timeout = timeout

    def request(self, *args, **kwargs):
        kwargs.setdefault("timeout", self._timeout)
        kwargs.setdefault("impersonate", _IMPERSONATE)
        return super().request(*args, **kwargs)


def _with_deadline(fn, seconds):
    """Run fn() but give up after `seconds` of wall-clock time, regardless of
    what the network layer does. The worker is a daemon thread, so if it's stuck
    in a hung socket we abandon it (it dies when the process exits) and raise
    TimeoutError. At most BLOCK_LIMIT such threads can pile up before the caller
    stops, so the leak is bounded."""
    box = {}

    def worker():
        try:
            box["value"] = fn()
        except BaseException as e:  # capture so .join can re-raise
            box["error"] = e

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    t.join(seconds)
    if t.is_alive():
        raise TimeoutError(f"exceeded {seconds}s wall-clock deadline")
    if "error" in box:
        raise box["error"]
    return box["value"]


def extract_video_id(url: str) -> str:
    """Extract video ID from a YouTube URL."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def get_existing_video_ids() -> set[str]:
    """Scan transcript file headers for already-fetched video IDs."""
    ids = set()
    for txt_file in TRANSCRIPTS_DIR.rglob("*.txt"):
        if txt_file.name == "urls.txt":
            continue
        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("# URL: "):
                        url = line.replace("# URL: ", "").strip()
                        match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
                        if match:
                            ids.add(match.group(1))
                        break
                    if not line.startswith("#"):
                        break
        except Exception:
            continue
    return ids


def load_urls() -> list[str]:
    """Load URLs from the urls.txt file."""
    if not URLS_FILE.exists():
        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
        with open(URLS_FILE, "w") as f:
            f.write("# Add YouTube URLs here — one per line\n")
            f.write("# Lines starting with # are ignored\n\n")
        print(f"Created {URLS_FILE} — add your URLs there and re-run.")
        sys.exit(0)

    urls = []
    with open(URLS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)

    return urls


_NO_TRANSCRIPT_HEADER = (
    "# Videos With No Transcript Available\n\n"
    "Auto-maintained by `fetch_transcripts.py`. These videos returned a "
    "*permanent* \"no transcript\" result (subtitles disabled, none found, or "
    "the video is unavailable), so the fetcher skips them on future runs instead "
    "of re-attempting them every time.\n\n"
    "Throttled / IP-blocked videos are **not** listed here — those stay pending "
    "and retry automatically. Click a title to watch it yourself; delete a row "
    "to force a re-attempt on the next run.\n\n"
    "| Date | Creator | Title (click to watch) | Reason |\n"
    "|------|---------|------------------------|--------|\n"
)


def md_escape(text: str) -> str:
    """Escape a title so it can't break a markdown table cell or a link label.

    Handles pipes (column separators), the `]`/`)` that would close a link
    `[label](url)`, and newlines (which would split the row). Other markdown is
    left as-is — these are the characters that actually corrupt the index/ledger.
    """
    return (
        text.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("]", "\\]")
        .replace(")", "\\)")
        .replace("\r", " ")
        .replace("\n", " ")
    )


def load_skipped_ids() -> set[str]:
    """Video IDs recorded in no-transcript-available.md — skipped on every run."""
    if not NO_TRANSCRIPT_FILE.exists():
        return set()
    text = NO_TRANSCRIPT_FILE.read_text(encoding="utf-8")
    return set(re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", text))


def record_no_transcript(video_id: str, creator: str, title: str, reason: str):
    """Append a video to the no-transcript ledger (creating it with a header)."""
    if not NO_TRANSCRIPT_FILE.exists():
        NO_TRANSCRIPT_FILE.write_text(_NO_TRANSCRIPT_HEADER, encoding="utf-8")
    date = datetime.now().strftime("%Y-%m-%d")
    url = f"https://www.youtube.com/watch?v={video_id}"
    # Escape markdown so a title with "|", "]", ")" or a newline can't break the
    # table row or the link label.
    safe_title = md_escape(title)
    row = f"| {date} | {creator} | [{safe_title}]({url}) | {reason} |\n"
    with open(NO_TRANSCRIPT_FILE, "a", encoding="utf-8") as f:
        f.write(row)


def _decode_page_meta(raw: str) -> str:
    """Decode a title/creator scraped from the watch page.

    Values pulled from YouTube's embedded JSON arrive with JSON string escapes
    still literal (a backslash-u sequence for '&', backslash-slash for '/'); the
    <title> fallback instead carries HTML entities (&amp; for '&'). Run both
    decoders so filenames and the index show the real characters, not the escape.
    """
    try:
        # Wrap in quotes and let json decode the backslash escapes in one shot.
        raw = json.loads(f'"{raw}"')
    except ValueError:
        pass  # not a clean JSON string body (e.g. a stray trailing backslash)
    return unescape(raw).strip()


def fetch_page_metadata(video_id: str) -> tuple[str, str]:
    """Fetch the YouTube page and extract creator name and video title."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    creator = "unknown-creator"
    title = "Unknown Title"

    try:
        # SOCS/CONSENT cookie skips YouTube's EU consent interstitial; without
        # it the watch page 302s to consent.youtube.com and metadata extraction
        # fails, mislabeling the video into the unknown-creator/ dir. Matches the
        # opener headers in update_urls.py.
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Cookie": "SOCS=CAI; CONSENT=YES+1",
            },
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # Creator name
        creator_patterns = [
            r'"ownerChannelName"\s*:\s*"([^"]+)"',
            r'"author"\s*:\s*"([^"]+)"',
            r'"channelName"\s*:\s*"([^"]+)"',
        ]
        for pattern in creator_patterns:
            match = re.search(pattern, html)
            if match:
                name = _decode_page_meta(match.group(1))
                creator = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
                break

        # Video title
        title_patterns = [
            r'"title"\s*:\s*"([^"]+)"',
            r"<title>(.+?)(?:\s*-\s*YouTube)?</title>",
        ]
        for pattern in title_patterns:
            match = re.search(pattern, html)
            if match:
                title = _decode_page_meta(match.group(1))
                break

    except Exception as e:
        print(f"  Warning: Could not fetch page metadata ({e})")

    return creator, title


def slugify_title(title: str) -> str:
    """Convert a video title to a filename-safe slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    # Truncate to keep filenames reasonable
    return slug[:80]


def fetch_transcript(video_id: str) -> str:
    """Fetch and join transcript text, with a per-request timeout and retries.

    Raises TranscriptBlocked if every attempt times out / the connection is
    refused (likely IP throttling). Other exceptions (e.g. transcripts disabled
    for this specific video) propagate unchanged so the caller can skip it.
    """
    def _fetch():
        ytt = YouTubeTranscriptApi(http_client=_TimeoutSession())
        transcript = ytt.fetch(video_id)
        return " ".join(snippet.text for snippet in transcript)

    last_network_err = None
    for attempt in range(1, TRANSCRIPT_RETRIES + 1):
        try:
            return _with_deadline(_fetch, TRANSCRIPT_DEADLINE)
        except (TimeoutError, CurlRequestException) as e:
            # CurlRequestException is curl_cffi's base for timeout / refused /
            # SSL-EOF transport failures; those don't subclass requests' errors,
            # so the library re-raises them raw. Treat any as a transient block.
            last_network_err = e
            if attempt < TRANSCRIPT_RETRIES:
                wait = 3 * attempt
                print(f"    blocked (attempt {attempt}/{TRANSCRIPT_RETRIES}); "
                      f"retrying in {wait}s...")
                time.sleep(wait)
    raise TranscriptBlocked(str(last_network_err))


def estimate_tokens(word_count: int) -> int:
    """Estimate token count from word count."""
    return int(word_count * TOKEN_RATIO)


def rebuild_index():
    """Scan all transcript files and rebuild index.md from scratch."""
    entries = []

    for txt_file in sorted(TRANSCRIPTS_DIR.rglob("*.txt")):
        if txt_file.name == "urls.txt":
            continue

        creator_dir = txt_file.parent.name
        title = "Unknown"
        date = "Unknown"
        url = ""
        word_count = 0

        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read()
            for line in content.splitlines():
                if line.startswith("# Title: "):
                    title = line.replace("# Title: ", "").strip()
                elif line.startswith("# Fetched: "):
                    raw = line.replace("# Fetched: ", "").strip()
                    date = raw[:10]
                elif line.startswith("# URL: "):
                    url = line.replace("# URL: ", "").strip()

            # Word count excludes header lines
            body = re.sub(r"^#.*\n", "", content, flags=re.MULTILINE).strip()
            word_count = len(body.split())

        tokens = estimate_tokens(word_count)
        rel_path = txt_file.relative_to(TRANSCRIPTS_DIR)
        entries.append((creator_dir, title, date, url, str(rel_path), word_count, tokens))

    total_tokens = sum(e[6] for e in entries)

    index_path = TRANSCRIPTS_DIR / "index.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# Transcript Library\n\n")
        f.write(f"{len(entries)} transcript(s) — ~{total_tokens:,} tokens total.\n\n")
        f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("| Creator | Title | Date | ~Tokens | File |\n")
        f.write("|---------|-------|------|---------|------|\n")
        for creator, title, date, url, rel_path, wc, tokens in entries:
            safe_title = md_escape(title)
            title_display = f"[{safe_title}]({url})" if url else safe_title
            f.write(f"| {creator} | {title_display} | {date} | {tokens:,} | `{rel_path}` |\n")

    print(f"\nIndex updated: {index_path} ({len(entries)} entries, ~{total_tokens:,} tokens total)")


def process_video(url: str, index: int, total: int,
                  existing_ids: set[str], skipped_ids: set[str]) -> str:
    """Process a single video.

    Returns a status: "saved", "skip", or "recorded" (a permanent no-transcript
    video just added to the ledger). Raises TranscriptBlocked for a transient IP
    block so main() can trip the circuit breaker; blocked videos write nothing
    and so retry automatically on the next run.
    """
    print(f"\n[{index}/{total}] {url}")

    try:
        video_id = extract_video_id(url)
    except ValueError as e:
        print(f"  Skipping — {e}")
        return "skip"

    if video_id in existing_ids:
        print(f"  Skipping — already fetched ({video_id})")
        return "skip"
    if video_id in skipped_ids:
        print(f"  Skipping — known to have no transcript ({video_id})")
        return "skip"

    # Space network calls with a randomised gap so the run doesn't burst (see
    # FETCH_SLEEP_* above). Only reached for videos we actually fetch.
    if FETCH_SLEEP_MAX > 0:
        gap = random.uniform(FETCH_SLEEP_MIN, FETCH_SLEEP_MAX)
        print(f"  Spacing {gap:.1f}s before fetch...")
        time.sleep(gap)

    print(f"  Video ID: {video_id}")
    print(f"  Fetching metadata...")
    creator, title = fetch_page_metadata(video_id)
    print(f"  Creator: {creator}")
    print(f"  Title: {title}")

    print(f"  Fetching transcript...")
    try:
        text = fetch_transcript(video_id)
    except TranscriptBlocked as e:
        # Our wall-clock deadline tripped (stalled/refused connection). Re-raise
        # so main() can trip the breaker; not written, so it retries next run.
        print(f"  BLOCKED — transcript request timed out ({e}); will retry next run")
        raise
    except TRANSIENT_ERRORS as e:
        # YouTube is throttling/blocking this IP. Treat like a block (retry next
        # run) and surface it to the breaker — do NOT record as "no transcript".
        print(f"  BLOCKED — {type(e).__name__}: YouTube is throttling this IP; "
              f"will retry next run")
        raise TranscriptBlocked(str(e))
    except PERMANENT_ERRORS as e:
        # The video genuinely has no fetchable transcript. Record it so we never
        # waste another attempt on it.
        reason = type(e).__name__
        print(f"  No transcript ({reason}) — recording so it won't be retried")
        record_no_transcript(video_id, creator, title, reason)
        return "recorded"
    except Exception as e:
        # Unknown failure — be conservative: don't record, just retry next run.
        print(f"  Skipping — could not fetch ({e}); will retry next run")
        return "skip"

    output_dir = TRANSCRIPTS_DIR / creator
    os.makedirs(output_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d")
    title_slug = slugify_title(title)
    # Include video_id so two videos with the same (or empty) slug on the same
    # day get distinct filenames instead of overwriting each other.
    prefix = f"{title_slug}_" if title_slug else ""
    filename = f"{prefix}{video_id}_{ts}.txt"
    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Title: {title}\n")
        f.write(f"# Creator: {creator}\n")
        f.write(f"# Fetched: {datetime.now().isoformat()}\n")
        f.write(f"# URL: https://www.youtube.com/watch?v={video_id}\n\n")
        f.write(text)

    # Mark as fetched in-memory so a duplicate URL later in this same run is
    # skipped rather than refetched/overwritten (existing_ids is rescanned from
    # disk only at the start of a run).
    existing_ids.add(video_id)

    word_count = len(text.split())
    tokens = estimate_tokens(word_count)
    print(f"  Saved: {filepath} ({word_count:,} words, ~{tokens:,} tokens)")
    return "saved"


def main():
    urls = load_urls()

    if not urls:
        print(f"No URLs found in {URLS_FILE}")
        sys.exit(1)

    existing_ids = get_existing_video_ids()
    skipped_ids = load_skipped_ids()
    print(f"Processing {len(urls)} URL(s) ({len(existing_ids)} already fetched, "
          f"{len(skipped_ids)} known no-transcript)...")

    # Circuit breaker: a connection-level block (timeout / SSL EOF / refused) or
    # a RequestBlocked/IpBlocked from YouTube is a global signal that this IP is
    # being throttled, so once a few add up we stop instead of grinding through
    # every remaining video. Skipped videos retry automatically next run (nothing
    # is written). Permanent "no transcript" cases don't count — they're recorded.
    BLOCK_LIMIT = 3
    blocked = 0

    success = 0
    recorded = 0
    for i, url in enumerate(urls, 1):
        try:
            status = process_video(url, i, len(urls), existing_ids, skipped_ids)
        except TranscriptBlocked:
            blocked += 1
            if blocked >= BLOCK_LIMIT:
                print(f"\n!! {BLOCK_LIMIT} transcript requests blocked — "
                      f"YouTube is throttling this IP.")
                print("   Stopping fetch early; remaining videos retry on the next run.")
                break
            continue

        if status == "saved":
            success += 1
            if success >= MAX_PER_RUN:
                print(f"\nReached per-run cap ({MAX_PER_RUN}); stopping. "
                      f"Remaining new videos fetch on the next run.")
                break
        elif status == "recorded":
            recorded += 1

    rebuild_index()

    print(f"\n{'='*40}")
    print(f"Done: {success} new transcript(s) saved")
    if recorded:
        print(f"No transcript (recorded, won't retry): {recorded} "
              f"— see {NO_TRANSCRIPT_FILE.name}")
    if blocked:
        print(f"Blocked (throttled, will retry next run): {blocked}")
    print(f"Location: {TRANSCRIPTS_DIR}")
    print(f"\nTell Claude Code:")
    print(f'  "Read .claude/transcripts/index.md to see what knowledge is')
    print(f'   available, then extract actionable improvements and update CLAUDE.md"')


if __name__ == "__main__":
    main()