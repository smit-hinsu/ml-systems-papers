#!/usr/bin/env python3
"""
Fetch citation counts from Semantic Scholar.

Why not OpenAlex (`fetch_metadata.py`): OpenAlex builds its citation graph from
parsed reference lists of indexed works, so it badly undercounts recent arXiv
preprints — the papers citing them are mostly preprints it hasn't parsed. Measured
2026-07-31: TokenWeave (arXiv 2505.11329) reads 0 on OpenAlex and 17 on Semantic
Scholar. For a corpus of papers that were preprints months before the conference,
OpenAlex counts are not usable.

Semantic Scholar rate-limits hard (429) under any concurrency, so every request
here is serial. Papers with an `arxiv_url` are resolved through the batch endpoint
(one request per chunk, exact ID match, no title ambiguity); the rest fall back to
serial title search.

Usage:
    python scripts/fetch_citations.py                # all papers
    python scripts/fetch_citations.py --dry-run
    python scripts/fetch_citations.py --delay 5      # slower if you see 429s
"""

import argparse
import re
import sys
import time
from datetime import date
from pathlib import Path

import frontmatter
import requests

ROOT = Path(__file__).parent.parent
PAPERS = ROOT / "data" / "papers"
S2 = "https://api.semanticscholar.org/graph/v1"
BATCH_SIZE = 100
FIELDS = "title,citationCount,externalIds"


def arxiv_id(url):
    m = re.search(r"arxiv\.org/abs/([\d.]+(?:v\d+)?)", url or "")
    if m:
        return m.group(1).split("v")[0]
    # Some entries carry a bare ID rather than a URL.
    m = re.fullmatch(r"\s*(\d{4}\.\d{4,5})\s*", url or "")
    return m.group(1) if m else None


def get(url, delay, retries=4, **kwargs):
    """Serial GET/POST with backoff on 429."""
    for attempt in range(retries):
        try:
            r = (requests.post if "json" in kwargs else requests.get)(
                url, timeout=30, **kwargs)
            if r.status_code == 429:
                wait = delay * (2 ** attempt)
                print(f"    429 — backing off {wait:.0f}s", flush=True)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return None
            print(f"    error: {e}", flush=True)
            return None
        except Exception as e:
            print(f"    error: {e}", flush=True)
            return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--delay", type=float, default=3.0,
                    help="Seconds between requests (default 3.0)")
    args = ap.parse_args()

    posts = {}
    for path in sorted(PAPERS.glob("*.md")):
        posts[path] = frontmatter.load(path)

    by_arxiv, no_arxiv = {}, []
    for path, post in posts.items():
        aid = arxiv_id(str(post.metadata.get("arxiv_url") or ""))
        if aid:
            by_arxiv.setdefault(f"ARXIV:{aid}", []).append(path)
        else:
            no_arxiv.append(path)

    print(f"{len(by_arxiv)} papers with an arXiv ID, {len(no_arxiv)} without\n")
    found = {}

    # --- batch lookups by arXiv ID (serial, one chunk at a time) ---
    ids = list(by_arxiv)
    for i in range(0, len(ids), BATCH_SIZE):
        chunk = ids[i:i + BATCH_SIZE]
        print(f"batch {i // BATCH_SIZE + 1}: {len(chunk)} ids", flush=True)
        data = get(f"{S2}/paper/batch", args.delay,
                   params={"fields": FIELDS}, json={"ids": chunk})
        if data:
            for key, rec in zip(chunk, data):
                if rec and rec.get("citationCount") is not None:
                    for path in by_arxiv[key]:
                        found[path] = (rec["citationCount"], rec.get("title") or "")
        time.sleep(args.delay)

    # --- serial title search for the rest ---
    for n, path in enumerate(no_arxiv, 1):
        title = str(posts[path].metadata.get("title") or "")
        print(f"[{n}/{len(no_arxiv)}] {title[:62]}", flush=True)
        data = get(f"{S2}/paper/search", args.delay,
                   params={"query": title, "fields": FIELDS, "limit": 3})
        for rec in (data or {}).get("data", []) or []:
            a = re.sub(r"[^a-z0-9]", "", title.lower())
            b = re.sub(r"[^a-z0-9]", "", (rec.get("title") or "").lower())
            if a and b and (a == b or a.startswith(b[:40]) or b.startswith(a[:40])):
                if rec.get("citationCount") is not None:
                    found[path] = (rec["citationCount"], rec.get("title") or "")
                break
        time.sleep(args.delay)

    today = date.today().isoformat()
    changed = 0
    for path, (count, matched) in sorted(found.items()):
        post = posts[path]
        if post.metadata.get("citations") == count:
            continue
        changed += 1
        print(f"  {path.stem[:52]:<52} {post.metadata.get('citations')} -> {count}")
        if not args.dry_run:
            post.metadata["citations"] = count
            post.metadata["citations_updated"] = today
            path.write_text(frontmatter.dumps(post) + "\n")

    total = sum(c for c, _ in found.values())
    print(f"\nResolved {len(found)}/{len(posts)} papers"
          f"{' (dry run)' if args.dry_run else f'; updated {changed}'}")
    print(f"Total citations across resolved papers: {total}")
    if len(found) < len(posts):
        print(f"Unresolved: {len(posts) - len(found)} — rerun with a larger --delay")
    return 0


if __name__ == "__main__":
    sys.exit(main())
