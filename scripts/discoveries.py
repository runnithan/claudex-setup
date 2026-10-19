#!/usr/bin/env python3
"""
Discoveries catalogue: merge /discover miner output and render discoveries/INDEX.md
====================================================================================
/discover's miners read transcripts and return JSON candidates (tools and uses).
This script owns the deterministic half: dedupe against the catalogue, count how
many transcripts mention each entry, ledger the mined transcripts, and render the
readable index. Keeping it out of the model matters on a backfill of a thousand
transcripts, where hand-merged markdown drifts into duplicates and wrong counts.

Files (all under discoveries/):
    catalogue.json    source of truth: every entry with its sources and quotes
    INDEX.md          rendered from catalogue.json, never edited by hand
    .processed.json   {"processed": [...]} transcripts already mined

Usage (stdlib only, run from anywhere):
    python3 scripts/discoveries.py pending                # transcripts not yet mined
    python3 scripts/discoveries.py merge --run 2026-10-19 batch1.json [batch2.json ...]
    python3 scripts/discoveries.py render                 # re-render INDEX.md only
    python3 scripts/discoveries.py fold <from> <into>     # merge one entry into another
    python3 scripts/discoveries.py forget <transcript>... # un-ledger, so they are re-mined

merge appends each batch's "processed" list to the ledger in the same write as its
entries, so an interrupted run resumes from the ledger without re-mining. --run is a
label: the date, with a suffix (2026-10-19b) for a second run on the same day.

A transcript a batch reports with no discoveries is ledgered only with proof it was
read: an "empty" record quoting its final words, which must come from the end of the
text. Miners that skimmed reported real transcripts as empty; an unproven one
stays pending and is re-mined.
"""

import argparse
import json
import re
import signal
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "discoveries"
CATALOGUE = DIR / "catalogue.json"
INDEX = DIR / "INDEX.md"
LEDGER = DIR / ".processed.json"

CATEGORIES = [
    "agent tooling", "mcp servers", "dev tools", "design and media",
    "data and research", "business and marketing", "personal and productivity",
]
TITLES = {"mcp servers": "MCP servers"}
LATEST_CAP = 30  # a backfill adds thousands; the full entries live in the sections below


def load_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path, data):
    # Write a temp file and rename it, so a kill mid-write leaves the old file whole.
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def norm_name(name):
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def norm_url(url):
    url = (url or "").strip().lower()
    url = re.sub(r"^https?://(www\.)?", "", url)
    return re.sub(r"(\.git)?/*$", "", url)


def transcript_date(rel):
    """YYYY-MM-DD for a transcript: its filename stamp, else its `# Fetched:` header."""
    m = re.search(r"_(\d{4})(\d{2})(\d{2})\.txt$", rel)
    if m:
        return "-".join(m.groups())
    path = ROOT / rel
    if path.exists():
        with path.open(encoding="utf-8", errors="replace") as fh:
            for _, line in zip(range(15), fh):
                m = re.match(r"# Fetched:\s*(\d{4}-\d{2}-\d{2})", line)
                if m:
                    return m.group(1)
    return "unknown"


_creators = {}


def creator(rel):
    """Who made a transcript: its `# Creator:` header, else its top-level folder."""
    if rel not in _creators:
        found = None
        path = ROOT / rel
        if path.exists():
            with path.open(encoding="utf-8", errors="replace") as fh:
                for _, line in zip(range(15), fh):
                    m = re.match(r"# Creator:\s*(\S+)", line)
                    if m:
                        found = m.group(1)
                        break
        _creators[rel] = found or Path(rel).parts[1]
    return _creators[rel]


def read_to_end(rel, last_line):
    """True when last_line comes from the transcript's final 1,500 characters.

    Most transcripts are one long line, so checking the last few lines would accept a
    quote from anywhere in the file; only the end of the text proves it was read through.
    """
    squash = lambda s: re.sub(r"\s+", " ", s).strip().lower()
    want = squash(last_line or "")
    path = ROOT / rel
    if len(want) < 12 or not path.exists():
        return False
    return want in squash(path.read_text(encoding="utf-8", errors="replace"))[-1500:]


_texts = {}


def quoted(rel, quote):
    """True when the quote appears in the transcript, ignoring case and punctuation."""
    squash = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    if rel not in _texts:
        path = ROOT / rel
        _texts[rel] = squash(path.read_text(encoding="utf-8", errors="replace")) if path.exists() else ""
    return squash(quote) in _texts[rel]


def all_transcripts():
    return sorted(str(p.relative_to(ROOT)) for p in (ROOT / "transcripts").glob("*/**/*.txt"))


def find(entries, cand):
    """The existing entry this candidate describes, or None."""
    name = norm_name(cand.get("name"))
    if cand.get("kind") == "tool":
        url = norm_url(cand.get("url")) if cand.get("verified") else ""
        for e in entries:
            if e["kind"] != "tool":
                continue
            if url and e.get("url") and norm_url(e["url"]) == url:
                return e
            # An unconfirmed name matches a tool of the same name either way round.
            if name and norm_name(e["name"]) == name and not (url and e.get("url")):
                return e
            # One project is often verified as its repo in one video and its site in another
            # (github.com/n8n-io/n8n and n8n.io): same name, one link on GitHub, is one tool.
            if (name and url and e.get("url") and norm_name(e["name"]) == name
                    and ("github.com/" in url) != ("github.com/" in norm_url(e["url"]))):
                return e
        return None
    for e in entries:
        if e["kind"] == "use" and norm_name(e["name"]) == name:
            return e
    return None


def merge(run, batch_files):
    DIR.mkdir(exist_ok=True)
    cat = load_json(CATALOGUE, {"entries": [], "runs": []})
    ledger = load_json(LEDGER, {"processed": []})
    entries = cat["entries"]
    stats = {"candidates": 0, "new_tools_verified": 0, "new_tools_unconfirmed": 0,
             "new_uses": 0, "seen_again": 0, "processed": 0, "unproven": 0, "quotes_not_found": 0}
    unproven, misquoted = [], []
    for bf in batch_files:
        batch = json.loads(Path(bf).read_text(encoding="utf-8"))
        # A transcript already in the ledger was merged before; skipping it keeps a
        # re-run batch from inflating counts or the run's totals.
        merged_before = set(ledger["processed"])
        for cand in batch.get("discoveries", []):
            if cand.get("transcript") in merged_before:
                continue
            stats["candidates"] += 1
            # The quote is the evidence an entry rests on: one a miner paraphrased or
            # invented is reported so the batch can be corrected, not silently kept.
            if cand.get("quote") and not quoted(cand["transcript"], cand["quote"]):
                misquoted.append(f"{cand['name']} in {cand['transcript']}")
            # Sponsorship belongs to the video, not the tool: one sponsor read must not
            # label every later, unpaid mention.
            src = {"transcript": cand["transcript"], "quote": cand.get("quote", ""),
                   "date": transcript_date(cand["transcript"]),
                   "sponsored": bool(cand.get("sponsored"))}
            e = find(entries, cand)
            if e is None:
                e = {"kind": cand["kind"], "name": cand["name"], "what": cand.get("what", ""),
                     "category": cand.get("category") if cand.get("category") in CATEGORIES else "agent tooling",
                     "added": run, "seen_runs": [run], "sources": [src]}
                if cand["kind"] == "tool":
                    e.update(url=cand.get("url") if cand.get("verified") else None,
                             verified=bool(cand.get("verified") and cand.get("url")),
                             as_heard=cand.get("as_heard"))
                    stats["new_tools_verified" if e["verified"] else "new_tools_unconfirmed"] += 1
                else:
                    e["tools"] = cand.get("tools", [])
                    stats["new_uses"] += 1
                entries.append(e)
                continue
            if e["kind"] == "tool" and not e.get("verified") and cand.get("verified") and cand.get("url"):
                e.update(url=cand["url"], verified=True, name=cand["name"])
            if all(s["transcript"] != src["transcript"] for s in e["sources"]):
                e["sources"].append(src)
                if e["added"] != run:
                    if run not in e["seen_runs"]:
                        e["seen_runs"].append(run)
                    stats["seen_again"] += 1
        done = set(ledger["processed"])
        yielded = {c.get("transcript") for c in batch.get("discoveries", [])}
        empty = batch.get("empty", {})
        new = []
        for p in batch.get("processed", []):
            if p in done:
                continue
            if p not in yielded and not read_to_end(p, (empty.get(p) or {}).get("last_line")):
                unproven.append(p)  # left pending, so the next pass re-mines it
                continue
            new.append(p)
        ledger["processed"] = sorted(done | set(new))
        stats["processed"] += len(new)
    stats["unproven"] = len(unproven)
    stats["quotes_not_found"] = len(misquoted)
    prev = next((r for r in cat["runs"] if r["date"] == run), None)
    if prev:
        for k, v in stats.items():
            prev[k] = prev.get(k, 0) + v
    else:
        cat["runs"].append({"date": run, **stats})
    write_json(CATALOGUE, cat)
    write_json(LEDGER, ledger)
    render(cat)
    return stats, cat, unproven, misquoted


def seen(e):
    return len({s["transcript"] for s in e["sources"]})


def creators(e):
    return len({creator(s["transcript"]) for s in e["sources"]})


def rank(e):
    # Distinct creators first: one creator plugging their own product in every video
    # is not the same signal as several creators showing it.
    return (-creators(e), -seen(e), e["name"].lower())


def fold(src, dst):
    """Merge the entry matching src (a URL or name) into the one matching dst."""
    cat = load_json(CATALOGUE, {"entries": [], "runs": []})
    pick = lambda key: [e for e in cat["entries"] if norm_url(e.get("url")) == norm_url(key) and e.get("url")
                        or norm_name(e["name"]) == norm_name(key)]
    a, b = pick(src), pick(dst)
    if len(a) != 1 or len(b) != 1 or a[0] is b[0]:
        sys.exit(f"fold needs exactly one entry each: {len(a)} match {src!r}, {len(b)} match {dst!r}")
    a, b = a[0], b[0]
    have = {s["transcript"] for s in b["sources"]}
    b["sources"] += [s for s in a["sources"] if s["transcript"] not in have]
    b["seen_runs"] = sorted(set(b["seen_runs"]) | set(a["seen_runs"]))
    b["added"] = min(a["added"], b["added"])
    cat["entries"].remove(a)
    write_json(CATALOGUE, cat)
    render(cat)
    print(f"folded {a['name']} ({a.get('url')}) into {b['name']} ({b.get('url')}): now {seen(b)} videos")


def forget(paths):
    ledger = load_json(LEDGER, {"processed": []})
    drop = set(paths)
    before = len(ledger["processed"])
    ledger["processed"] = [p for p in ledger["processed"] if p not in drop]
    write_json(LEDGER, ledger)
    print(f"un-ledgered {before - len(ledger['processed'])} of {len(drop)}")


def line(e):
    dates = sorted(s["date"] for s in e["sources"] if s["date"] != "unknown")
    span = f"{dates[0]} to {dates[-1]}" if len(set(dates)) > 1 else (dates[0] if dates else "date unknown")
    srcs = ", ".join(f"[{Path(s['transcript']).parent.relative_to('transcripts')}, {s['date']}](../{s['transcript']})"
                     for s in e["sources"])
    if e["kind"] == "tool":
        head = f"**[{e['name']}]({e['url']})**" if e.get("verified") else \
               f"**{e['name']}** (unconfirmed, heard as \"{e.get('as_heard') or e['name']}\")"
        paid = sum(1 for s in e["sources"] if s.get("sponsored"))
        if paid:
            head += " (sponsored)" if paid == len(e["sources"]) else f" (sponsored in {paid} of {len(e['sources'])})"
    else:
        built = f" (built with {', '.join(e['tools'])})" if e.get("tools") else ""
        head = f"**{e['name']}**{built}"
    by = f"{creators(e)} creators" if creators(e) > 1 else "1 creator"
    return f"- {head}: {e['what']} Seen in {seen(e)} videos by {by} ({span}). Sources: {srcs}"


def short(e):
    name = f"[{e['name']}]({e['url']})" if e["kind"] == "tool" and e.get("verified") else e["name"]
    if creators(e) > 1:
        return f"{name} ({creators(e)} creators)"
    return f"{name} ({seen(e)} videos)" if seen(e) > 1 else name


def render(cat=None):
    cat = cat or load_json(CATALOGUE, {"entries": [], "runs": []})
    entries = cat["entries"]
    out = ["# Discoveries", "",
           "Tools, repos and uses that people show alongside Claude Code and Codex, mined from "
           "transcripts by `/discover` whether or not they fit this setup. Each tool was checked "
           "against GitHub or its own site; `unconfirmed` means the name could not be verified. "
           "Generated by `scripts/discoveries.py` from `catalogue.json`: do not edit by hand.", ""]
    if cat["runs"]:
        last = cat["runs"][-1]
        run = last["date"]
        added = sorted((e for e in entries if e["added"] == run), key=rank)
        again = sorted((e for e in entries if e["added"] != run and run in e["seen_runs"]), key=rank)
        out += [f"## Latest run ({run})", ""]
        for label, group in ((f"New ({len(added)})", added), (f"Seen again ({len(again)})", again)):
            if group:
                names = [short(e) for e in group[:LATEST_CAP]]
                more = f", and {len(group) - LATEST_CAP} more below" if len(group) > LATEST_CAP else ""
                out += [f"{label}, shown by the most creators first: " + ", ".join(names) + more + ".", ""]
        out += [f"{run}: {last['processed']} transcripts mined, {last['candidates']} candidates, "
                f"{last['new_tools_verified']} new tools verified, {last['new_tools_unconfirmed']} "
                f"unconfirmed, {last['new_uses']} new uses, {last['seen_again']} seen again.", ""]
        top = sorted(entries, key=rank)[:10]
        out += ["Shown by the most creators overall: " + ", ".join(short(e) for e in top) + ".", ""]
    for kind, title in (("tool", "Tools"), ("use", "Uses")):
        group = [e for e in entries if e["kind"] == kind]
        out += [f"## {title} ({len(group)})", ""]
        for c in CATEGORIES:
            sub = sorted((e for e in group if e["category"] == c), key=rank)
            if sub:
                out += [f"### {TITLES.get(c, c.capitalize())}", ""] + [line(e) for e in sub] + [""]
    INDEX.write_text("\n".join(out), encoding="utf-8")


def main():
    # `pending | head` closes the pipe early; exit quietly instead of a BrokenPipeError
    # traceback. Windows has no SIGPIPE.
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pending")
    m = sub.add_parser("merge")
    m.add_argument("--run", required=True, help="run label: the date, plus a suffix for a second run that day")
    m.add_argument("files", nargs="+")
    sub.add_parser("render")
    f = sub.add_parser("fold")
    f.add_argument("src", help="URL or name of the entry to fold away")
    f.add_argument("dst", help="URL or name of the entry to keep")
    g = sub.add_parser("forget")
    g.add_argument("transcripts", nargs="+")
    args = ap.parse_args()
    if args.cmd == "pending":
        done = set(load_json(LEDGER, {"processed": []})["processed"])
        todo = [p for p in all_transcripts() if p not in done]
        print(f"{len(todo)} pending", file=sys.stderr)
        print("\n".join(todo))
    elif args.cmd == "merge":
        stats, cat, unproven, misquoted = merge(args.run, args.files)
        print(json.dumps(stats))
        if unproven:
            print("unproven empty (left pending, re-mine): " + " ".join(unproven))
        for m in misquoted:
            print("quote not found in transcript (correct the batch and re-merge): " + m)
        top = sorted(cat["entries"], key=rank)[:5]
        print("shown by the most creators: " + "; ".join(
            f"{e['name']} ({creators(e)} creators, {seen(e)} videos)" for e in top))
    elif args.cmd == "fold":
        fold(args.src, args.dst)
    elif args.cmd == "forget":
        forget(args.transcripts)
    else:
        render()


if __name__ == "__main__":
    main()
