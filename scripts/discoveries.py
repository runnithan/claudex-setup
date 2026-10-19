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

merge appends each batch's "processed" list to the ledger in the same write as its
entries, so an interrupted run resumes from the ledger without re-mining.
"""

import argparse
import json
import re
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
             "new_uses": 0, "seen_again": 0, "processed": 0}
    for bf in batch_files:
        batch = json.loads(Path(bf).read_text(encoding="utf-8"))
        # A transcript already in the ledger was merged before; skipping it keeps a
        # re-run batch from inflating counts or the run's totals.
        merged_before = set(ledger["processed"])
        for cand in batch.get("discoveries", []):
            if cand.get("transcript") in merged_before:
                continue
            stats["candidates"] += 1
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
        new = [p for p in batch.get("processed", []) if p not in done]
        ledger["processed"] = sorted(done | set(new))
        stats["processed"] += len(new)
    prev = next((r for r in cat["runs"] if r["date"] == run), None)
    if prev:
        for k, v in stats.items():
            prev[k] = prev.get(k, 0) + v
    else:
        cat["runs"].append({"date": run, **stats})
    write_json(CATALOGUE, cat)
    write_json(LEDGER, ledger)
    render(cat)
    return stats, cat


def seen(e):
    return len({s["transcript"] for s in e["sources"]})


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
    return f"- {head}: {e['what']} Seen {seen(e)}x ({span}). Sources: {srcs}"


def short(e):
    name = f"[{e['name']}]({e['url']})" if e["kind"] == "tool" and e.get("verified") else e["name"]
    return f"{name} ({seen(e)}x)" if seen(e) > 1 else name


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
        order = lambda e: (-seen(e), e["name"].lower())
        added = sorted((e for e in entries if e["added"] == run), key=order)
        again = sorted((e for e in entries if e["added"] != run and run in e["seen_runs"]), key=order)
        out += [f"## Latest run ({run})", ""]
        for label, group in ((f"New ({len(added)})", added), (f"Seen again ({len(again)})", again)):
            if group:
                names = [short(e) for e in group[:LATEST_CAP]]
                more = f", and {len(group) - LATEST_CAP} more below" if len(group) > LATEST_CAP else ""
                out += [f"{label}, most seen first: " + ", ".join(names) + more + ".", ""]
        out += [f"{run}: {last['processed']} transcripts mined, {last['candidates']} candidates, "
                f"{last['new_tools_verified']} new tools verified, {last['new_tools_unconfirmed']} "
                f"unconfirmed, {last['new_uses']} new uses, {last['seen_again']} seen again.", ""]
    for kind, title in (("tool", "Tools"), ("use", "Uses")):
        group = [e for e in entries if e["kind"] == kind]
        out += [f"## {title} ({len(group)})", ""]
        for c in CATEGORIES:
            sub = sorted((e for e in group if e["category"] == c), key=lambda e: e["name"].lower())
            if sub:
                out += [f"### {TITLES.get(c, c.capitalize())}", ""] + [line(e) for e in sub] + [""]
    INDEX.write_text("\n".join(out), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pending")
    m = sub.add_parser("merge")
    m.add_argument("--run", required=True, help="run date, YYYY-MM-DD")
    m.add_argument("files", nargs="+")
    sub.add_parser("render")
    args = ap.parse_args()
    if args.cmd == "pending":
        done = set(load_json(LEDGER, {"processed": []})["processed"])
        todo = [p for p in all_transcripts() if p not in done]
        print("\n".join(todo))
        print(f"{len(todo)} pending", file=sys.stderr)
    elif args.cmd == "merge":
        stats, cat = merge(args.run, args.files)
        print(json.dumps(stats))
        top = sorted(cat["entries"], key=lambda e: (-seen(e), e["name"].lower()))[:5]
        print("most seen: " + "; ".join(f"{e['name']} ({seen(e)}x)" for e in top))
    else:
        render()


if __name__ == "__main__":
    main()
