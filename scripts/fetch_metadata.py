#!/usr/bin/env python3
"""
Fetch and update paper metadata from Semantic Scholar.

Pulls: citationCount, openAccessPdf (arXiv/OA link), externalIds (arXiv ID, DOI)

Usage:
    python scripts/fetch_metadata.py              # update all papers
    python scripts/fetch_metadata.py --slug tokenweave  # update one paper
    python scripts/fetch_metadata.py --dry-run    # show what would change

Rate limits:
    Without API key: ~1 req/second (100/5min). Script enforces this automatically.
    With API key:    set env var SEMANTIC_SCHOLAR_API_KEY for higher limits.

Get a free API key at: https://www.semanticscholar.org/product/api
"""

import argparse
import json
import os
import re
import time
from datetime import date
from pathlib import Path

import frontmatter
import requests
import yaml

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
CACHE = DATA / ".metadata_cache.json"
SS_BASE = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,authors,citationCount,externalIds,openAccessPdf,year,publicationDate"


def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    return {}


def save_cache(cache):
    CACHE.write_text(json.dumps(cache, indent=2))


def ss_headers():
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    return {"x-api-key": key} if key else {}


def search_paper(title, authors, cache):
    """Search Semantic Scholar for a paper by title. Returns best match or None."""
    cache_key = f"search:{title[:80]}"
    if cache_key in cache:
        return cache[cache_key]

    query = re.sub(r"[^\w\s]", " ", title)[:100]
    url = f"{SS_BASE}/paper/search"
    params = {"query": query, "fields": FIELDS, "limit": 5}

    try:
        r = requests.get(url, params=params, headers=ss_headers(), timeout=15)
        if r.status_code == 429:
            print("  Rate limited — waiting 60s...")
            time.sleep(60)
            r = requests.get(url, params=params, headers=ss_headers(), timeout=15)
        r.raise_for_status()
        results = r.json().get("data", [])
    except Exception as e:
        print(f"  Error fetching {title[:50]}: {e}")
        return None

    # Find best match: prefer exact title match, then partial
    title_lower = title.lower()
    for result in results:
        if result.get("title", "").lower() == title_lower:
            cache[cache_key] = result
            save_cache(cache)
            return result

    # Fallback: first result if title is close enough
    if results:
        r0 = results[0]
        r0_title = r0.get("title", "").lower()
        # Accept if first 6 words match
        t_words = title_lower.split()[:6]
        r_words = r0_title.split()[:6]
        if t_words == r_words:
            cache[cache_key] = r0
            save_cache(cache)
            return r0

    cache[cache_key] = None
    save_cache(cache)
    return None


def update_paper(path, dry_run, cache, delay):
    post = frontmatter.load(path)
    meta = dict(post.metadata)
    title = meta.get("title", "")
    authors = meta.get("authors", [])

    print(f"\n  {path.name}")
    print(f"    title: {title[:60]}")

    result = search_paper(title, authors, cache)
    time.sleep(delay)

    if not result:
        print("    not found on Semantic Scholar")
        return False

    changes = {}

    # Citation count
    citations = result.get("citationCount")
    if citations is not None and meta.get("citations") != citations:
        changes["citations"] = citations
        changes["citations_updated"] = date.today().isoformat()

    # arXiv URL from openAccessPdf or externalIds
    ext = result.get("externalIds") or {}
    arxiv_id = ext.get("ArXiv")
    if arxiv_id and not meta.get("arxiv_url"):
        changes["arxiv_url"] = f"https://arxiv.org/abs/{arxiv_id}"

    oa_pdf = (result.get("openAccessPdf") or {}).get("url")
    if oa_pdf and not meta.get("arxiv_url") and not changes.get("arxiv_url"):
        if "arxiv.org" in oa_pdf:
            changes["arxiv_url"] = oa_pdf.replace("/pdf/", "/abs/").rstrip(".pdf")
        else:
            changes["arxiv_url"] = oa_pdf

    if not changes:
        print("    no updates")
        return False

    for k, v in changes.items():
        old = meta.get(k)
        print(f"    {k}: {old!r} → {v!r}")

    if dry_run:
        return False

    # Write back: update only the changed keys in the YAML frontmatter
    meta.update(changes)
    post.metadata = meta
    with open(path, "w") as f:
        frontmatter.dump(post, f)
    return True


def main():
    parser = argparse.ArgumentParser(description="Fetch paper metadata from Semantic Scholar")
    parser.add_argument("--slug", help="Update only this paper slug")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--delay", type=float, default=1.5,
                        help="Seconds between requests (default 1.5; reduce with API key)")
    args = parser.parse_args()

    cache = load_cache()
    papers_dir = DATA / "papers"

    if args.slug:
        paths = [papers_dir / f"{args.slug}.md"]
    else:
        paths = sorted(papers_dir.glob("*.md"))

    updated = 0
    for path in paths:
        if not path.exists():
            print(f"Not found: {path}")
            continue
        changed = update_paper(path, args.dry_run, cache, args.delay)
        if changed:
            updated += 1

    print(f"\n{'Would update' if args.dry_run else 'Updated'} {updated}/{len(paths)} papers.")
    if not os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        print("\nTip: set SEMANTIC_SCHOLAR_API_KEY for higher rate limits and more reliable results.")
        print("     Apply at: https://www.semanticscholar.org/product/api")


if __name__ == "__main__":
    main()
