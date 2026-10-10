#!/usr/bin/env python3
"""
Transcript pipeline: discover new YouTube URLs, then fetch transcripts for them.

Runs the two steps back-to-back so newly discovered videos become transcripts in
the same run (no point adding URLs without fetching). Lesson extraction is left
to the user.

    1. update_urls.py      - append new uploads for tracked creators to urls.txt
    2. fetch_transcripts.py - download transcripts for any not-yet-fetched URLs
                              (idempotent: it skips videos already on disk)

Run it (needs the project's uv venv for youtube-transcript-api):
    uv run python scripts/run_pipeline.py

This is what the "YouTube URL Updater" scheduled task executes. The task fires
at every logon, but a 24h "since last actual run" gate means the work
only happens about once a day, anchored to when the machine is actually used —
not a fixed wall-clock time. Pass --force to bypass the gate (manual runs).

Combined output is appended to transcripts/.pipeline.log.
"""

import os
import socket
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))  # allow sibling imports when run by path

LOG_FILE = SCRIPT_DIR.parent / "transcripts" / ".pipeline.log"
STATE_FILE = SCRIPT_DIR.parent / "transcripts" / ".last_run"

# Minimum hours between actual runs. The scheduler wakes us at every logon,
# but we only do work once this much time has passed since the last real run, so
# the cadence is "~once a day, measured from when it last ran" rather than a
# fixed clock time. A small slack lets a logon at about the same time the next
# day count as due, instead of being a few minutes short and waiting a day more.
MIN_HOURS_BETWEEN_RUNS = float(os.environ.get("MIN_HOURS_BETWEEN_RUNS", "24"))
DUE_SLACK_HOURS = 0.5

# A logon right after the laptop wakes can start us before the network is back.
# On 2026-10-05 every lookup failed with "Temporary failure in name resolution"
# for at least 90s after resume, the run saved nothing, and it still stamped
# .last_run, which burns the day. So wait for DNS first, and if it never comes
# up, skip the run without stamping so the next logon retries. The wait has to
# fit inside the task's 15-minute ExecutionTimeLimit next to a full run.
NETWORK_PROBE_HOST = "www.youtube.com"
NETWORK_WAIT_SECONDS = float(os.environ.get("NETWORK_WAIT_SECONDS", "180"))
NETWORK_POLL_SECONDS = 5.0

import update_urls          # noqa: E402  (after sys.path tweak)
import fetch_transcripts    # noqa: E402


def _hours_since_last_run():
    """Hours since the last actual run, or None if it has never run."""
    if not STATE_FILE.exists():
        return None
    try:
        last = datetime.fromisoformat(STATE_FILE.read_text().strip())
    except Exception:
        return None  # unreadable/corrupt -> treat as never run
    return (datetime.now() - last).total_seconds() / 3600.0


def _is_due(force: bool) -> bool:
    if force:
        return True
    elapsed = _hours_since_last_run()
    if elapsed is None:
        return True
    if elapsed < MIN_HOURS_BETWEEN_RUNS - DUE_SLACK_HOURS:
        remaining = MIN_HOURS_BETWEEN_RUNS - elapsed
        print(f"Not due: last run {elapsed:.1f}h ago "
              f"(need ~{MIN_HOURS_BETWEEN_RUNS:.0f}h). ~{remaining:.1f}h to go.")
        return False
    return True


def _wait_for_network() -> bool:
    """True once NETWORK_PROBE_HOST resolves, False if it still doesn't after
    NETWORK_WAIT_SECONDS. Always tries at least once."""
    deadline = time.monotonic() + NETWORK_WAIT_SECONDS
    while True:
        try:
            socket.getaddrinfo(NETWORK_PROBE_HOST, 443)
            return True
        except OSError:  # socket.gaierror is an OSError
            if time.monotonic() >= deadline:
                return False
            time.sleep(NETWORK_POLL_SECONDS)


def _mark_ran():
    """Stamp .last_run with 'now'. Called on completion (see run()), so the
    24h gate counts from when a run finished rather than when it started."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(datetime.now().isoformat(), encoding="utf-8")


class _Tee:
    """Write to several streams at once (console + log file)."""

    def __init__(self, *streams):
        self._streams = streams

    def write(self, s):
        for st in self._streams:
            st.write(s)

    def flush(self):
        for st in self._streams:
            st.flush()


def run() -> None:
    force = "--force" in sys.argv
    # Gate BEFORE opening the log, so the many gated wake-ups (one per logon) are
    # silent no-ops that never touch YouTube or spam the log.
    if not _is_due(force):
        return

    network_ok = _wait_for_network()

    # Ensure transcripts/ exists before opening the log (fresh clone safety).
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        logf.write(f"\n===== {datetime.now():%Y-%m-%d %H:%M:%S} pipeline =====\n")
        original_out = sys.stdout
        original_err = sys.stderr
        # Tee both stdout AND stderr to the log so tracebacks / library errors
        # are captured, not just normal output.
        sys.stdout = _Tee(original_out, logf)
        sys.stderr = _Tee(original_err, logf)
        try:
            if not network_ok:
                print(f"Network not ready: {NETWORK_PROBE_HOST} did not resolve "
                      f"within {NETWORK_WAIT_SECONDS:.0f}s. Skipped without "
                      f"stamping .last_run, so the next logon retries.")
                return  # skips _mark_ran() below on purpose
            print("--- step 1: discovering new URLs ---")
            # Discovery is best-effort: a crash here must NOT abort the fetch
            # step (we can still fetch transcripts for already-known URLs).
            try:
                rc = update_urls.main()
                if rc:
                    print(f"(discovery step returned non-zero code {rc})")
            except Exception as e:
                import traceback
                print(f"(discovery step failed: {e}; continuing to fetch)")
                traceback.print_exc()
            print("\n--- step 2: fetching transcripts ---")
            try:
                fetch_transcripts.main()
            except SystemExit as e:  # fetch exits(1) when urls.txt is empty
                print(f"(fetch step exited with code {e.code})")
        finally:
            sys.stdout = original_out
            sys.stderr = original_err

    # Stamp the run only AFTER it completes (rather than at the start): the 24h
    # gate measures from a finished run, so an early crash no longer burns a full
    # day of retries. Cadence intent is preserved — it's still "~once a day,
    # measured from the last (completed) run", just anchored to completion.
    _mark_ran()


if __name__ == "__main__":
    run()
