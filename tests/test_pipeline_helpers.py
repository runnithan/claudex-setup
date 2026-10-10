"""Lean, network-free tests for the pure helpers in the transcript pipeline.

This is a config repo, not a library, so these tests deliberately cover only the
parsing / slugifying / due-gating logic that's easy to break and annoying to
debug in production. Anything that touches the network is out of scope.

Run: uv run pytest tests/  (or: python -m pytest tests/)
"""

import socket
import sys
from pathlib import Path

import pytest

# The pipeline scripts live in scripts/ and import each other by bare name, so
# put that dir on sys.path before importing them.
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import fetch_transcripts  # noqa: E402
import run_pipeline  # noqa: E402


# --- fetch_transcripts.extract_video_id ------------------------------------

@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s", "dQw4w9WgXcQ"),
        ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),  # bare 11-char id
    ],
)
def test_extract_video_id_valid(url, expected):
    assert fetch_transcripts.extract_video_id(url) == expected


def test_extract_video_id_invalid_raises():
    with pytest.raises(ValueError):
        fetch_transcripts.extract_video_id("https://example.com/not-a-video")


# --- fetch_transcripts.slugify_title ---------------------------------------

def test_slugify_basic():
    assert fetch_transcripts.slugify_title("Hello World!") == "hello-world"


def test_slugify_collapses_and_trims_separators():
    assert fetch_transcripts.slugify_title("  A  --  B  ") == "a-b"


def test_slugify_truncates_to_80_chars():
    slug = fetch_transcripts.slugify_title("word " * 100)
    assert len(slug) <= 80


def test_slugify_empty_when_no_alnum():
    assert fetch_transcripts.slugify_title("!!!???") == ""


# --- fetch_transcripts.md_escape (guards the index/ledger) -----------------

def test_md_escape_handles_breaking_chars():
    out = fetch_transcripts.md_escape("a|b]c)d")
    assert "|" not in out.replace("\\|", "")
    assert "\\|" in out and "\\]" in out and "\\)" in out


def test_md_escape_flattens_newlines():
    assert "\n" not in fetch_transcripts.md_escape("line1\nline2")


# --- run_pipeline due-gating -----------------------------------------------

def test_is_due_when_never_run(monkeypatch):
    monkeypatch.setattr(run_pipeline, "_hours_since_last_run", lambda: None)
    assert run_pipeline._is_due(force=False) is True


def test_is_due_force_bypasses_gate(monkeypatch):
    # Even if it ran 1 minute ago, --force runs.
    monkeypatch.setattr(run_pipeline, "_hours_since_last_run", lambda: 0.02)
    assert run_pipeline._is_due(force=True) is True


def test_not_due_when_recent(monkeypatch):
    monkeypatch.setattr(run_pipeline, "_hours_since_last_run", lambda: 1.0)
    monkeypatch.setattr(run_pipeline, "MIN_HOURS_BETWEEN_RUNS", 24.0)
    assert run_pipeline._is_due(force=False) is False


def test_due_when_past_window(monkeypatch):
    monkeypatch.setattr(run_pipeline, "_hours_since_last_run", lambda: 25.0)
    monkeypatch.setattr(run_pipeline, "MIN_HOURS_BETWEEN_RUNS", 24.0)
    assert run_pipeline._is_due(force=False) is True


def test_hours_since_last_run_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(run_pipeline, "STATE_FILE", tmp_path / "nope")
    assert run_pipeline._hours_since_last_run() is None


def test_hours_since_last_run_reads_timestamp(tmp_path, monkeypatch):
    from datetime import datetime, timedelta

    state = tmp_path / ".last_run"
    state.write_text((datetime.now() - timedelta(hours=5)).isoformat())
    monkeypatch.setattr(run_pipeline, "STATE_FILE", state)
    elapsed = run_pipeline._hours_since_last_run()
    assert elapsed is not None
    assert 4.5 < elapsed < 5.5


def test_hours_since_last_run_corrupt_file(tmp_path, monkeypatch):
    state = tmp_path / ".last_run"
    state.write_text("not-a-timestamp")
    monkeypatch.setattr(run_pipeline, "STATE_FILE", state)
    assert run_pipeline._hours_since_last_run() is None


# --- run_pipeline network wait ---------------------------------------------
# DNS is simulated by patching socket.getaddrinfo, so nothing here touches the
# network. A run that starts offline must not stamp .last_run, or it burns the
# day's slot having fetched nothing (seen 2026-10-05 after a wake from sleep).

def _offline(*args, **kwargs):
    raise socket.gaierror(-3, "Temporary failure in name resolution")


@pytest.fixture
def pipeline_sandbox(tmp_path, monkeypatch):
    """Point run() at temp state/log files, stub both steps, shorten the wait."""
    calls = []
    monkeypatch.setattr(run_pipeline, "STATE_FILE", tmp_path / ".last_run")
    monkeypatch.setattr(run_pipeline, "LOG_FILE", tmp_path / ".pipeline.log")
    monkeypatch.setattr(run_pipeline.update_urls, "main",
                        lambda: calls.append("discover"))
    monkeypatch.setattr(run_pipeline.fetch_transcripts, "main",
                        lambda: calls.append("fetch"))
    monkeypatch.setattr(run_pipeline, "NETWORK_WAIT_SECONDS", 0.3)
    monkeypatch.setattr(run_pipeline, "NETWORK_POLL_SECONDS", 0.05)
    monkeypatch.setattr(sys, "argv", ["run_pipeline.py"])
    return calls


def test_offline_run_skips_steps_and_does_not_stamp(pipeline_sandbox, monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", _offline)
    run_pipeline.run()
    assert pipeline_sandbox == []
    assert not run_pipeline.STATE_FILE.exists()
    assert "Network not ready" in run_pipeline.LOG_FILE.read_text()


def test_online_run_does_both_steps_and_stamps(pipeline_sandbox, monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", lambda *a, **k: [("ok",)])
    run_pipeline.run()
    assert pipeline_sandbox == ["discover", "fetch"]
    assert run_pipeline.STATE_FILE.exists()


def test_network_that_comes_back_during_the_wait_runs(pipeline_sandbox, monkeypatch):
    attempts = []

    def flaky(*args, **kwargs):
        attempts.append(1)
        if len(attempts) < 3:
            _offline()
        return [("ok",)]

    monkeypatch.setattr(socket, "getaddrinfo", flaky)
    monkeypatch.setattr(run_pipeline, "NETWORK_WAIT_SECONDS", 5.0)
    run_pipeline.run()
    assert len(attempts) == 3
    assert pipeline_sandbox == ["discover", "fetch"]
    assert run_pipeline.STATE_FILE.exists()


def test_wait_for_network_tries_once_even_with_zero_wait(monkeypatch):
    attempts = []
    monkeypatch.setattr(socket, "getaddrinfo",
                        lambda *a, **k: attempts.append(1) or [("ok",)])
    monkeypatch.setattr(run_pipeline, "NETWORK_WAIT_SECONDS", 0.0)
    assert run_pipeline._wait_for_network() is True
    assert attempts == [1]


# --- fetch_transcripts unreadable watch page --------------------------------
# A watch page that can't be read gave fetch_page_metadata's fallbacks, and the
# transcript was still saved under unknown-creator/ with a junk title (seen
# 2026-07-04; the same page read fine later). It must retry instead.

VID = "B95cu7seTm8"


@pytest.fixture
def fetch_sandbox(tmp_path, monkeypatch):
    """Write transcripts to a temp dir, skip the spacing sleep, stub the
    transcript download and record whether it was called."""
    downloads = []
    monkeypatch.setattr(fetch_transcripts, "TRANSCRIPTS_DIR", tmp_path)
    monkeypatch.setattr(fetch_transcripts, "FETCH_SLEEP_MAX", 0)
    monkeypatch.setattr(fetch_transcripts, "fetch_transcript",
                        lambda vid: downloads.append(vid) or "some words")
    return tmp_path, downloads


@pytest.mark.parametrize("meta", [
    ("unknown-creator", "Unknown Title"),  # page fetch failed outright
    ("unknown-creator", "816"),            # page read, creator missing
    ("mark-kashef", "Unknown Title"),      # page read, title missing
])
def test_unreadable_metadata_retries_instead_of_saving(fetch_sandbox, monkeypatch, meta):
    out_dir, downloads = fetch_sandbox
    monkeypatch.setattr(fetch_transcripts, "fetch_page_metadata", lambda vid: meta)
    with pytest.raises(fetch_transcripts.TranscriptBlocked):
        fetch_transcripts.process_video(f"https://www.youtube.com/watch?v={VID}",
                                        1, 1, set(), set())
    assert list(out_dir.rglob("*.txt")) == []
    assert downloads == []


def test_readable_metadata_saves_under_creator(fetch_sandbox, monkeypatch):
    out_dir, downloads = fetch_sandbox
    monkeypatch.setattr(fetch_transcripts, "fetch_page_metadata",
                        lambda vid: ("mark-kashef", "Real Title"))
    status = fetch_transcripts.process_video(
        f"https://www.youtube.com/watch?v={VID}", 1, 1, set(), set())
    assert status == "saved"
    assert downloads == [VID]
    [saved] = out_dir.rglob("*.txt")
    assert saved.parent.name == "mark-kashef"
    assert saved.name.startswith(f"real-title_{VID}_")


def test_repeated_unreadable_pages_trip_the_breaker(fetch_sandbox, monkeypatch):
    pages = []
    ids = [f"vid{n:08d}" for n in range(6)]  # 11-char ids
    monkeypatch.setattr(fetch_transcripts, "load_urls",
                        lambda: [f"https://www.youtube.com/watch?v={v}" for v in ids])
    monkeypatch.setattr(fetch_transcripts, "get_existing_video_ids", set)
    monkeypatch.setattr(fetch_transcripts, "load_skipped_ids", set)
    monkeypatch.setattr(fetch_transcripts, "rebuild_index", lambda: None)
    monkeypatch.setattr(fetch_transcripts, "fetch_page_metadata",
                        lambda vid: pages.append(vid) or ("unknown-creator", "Unknown Title"))
    fetch_transcripts.main()
    assert len(pages) == 3  # stops at BLOCK_LIMIT instead of hitting every page
