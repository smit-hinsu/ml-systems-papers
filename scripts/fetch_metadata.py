#!/usr/bin/env python3
"""
Fetch and update paper metadata from OpenAlex (https://openalex.org).

Pulls: citationCount, arxiv_url (from open-access PDF or external IDs)

No API key required. Rate limit: 10 req/sec unauthenticated.
Set OA_EMAIL env var to get into the polite pool (higher limits):
    export OA_EMAIL=you@example.com

Usage:
    python scripts/fetch_metadata.py              # update all papers
    python scripts/fetch_metadata.py --slug tokenweave
    python scripts/fetch_metadata.py --dry-run
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

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
CACHE = DATA / ".metadata_cache.json"
OA_BASE = "https://api.openalex.org"


def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    return {}


def save_cache(cache):
    CACHE.write_text(json.dumps(cache, indent=2))


def oa_headers():
    email = os.environ.get("OA_EMAIL", "")
    return {"User-Agent": f"ml-systems-papers/1.0 (mailto:{email})"} if email else {}


def search_paper(title, cache):
    cache_key = f"oa:{title[:80]}"
    if cache_key in cache:
        return cache[cache_key]

    query = re.sub(r"[^\w\s]", " ", title)[:100]
    url = f"{OA_BASE}/works"
    params = {
        "search": query,
        "select": "id,title,cited_by_count,ids,open_access,publication_year",
        "per_page": 5,
    }

    try:
        r = requests.get(url, params=params, headers=oa_headers(), timeout=15)
        r.raise_for_status()
        results = r.json().get("results", [])
    except Exception as e:
        print(f"  Error: {e}")
        return None

    title_lower = title.lower()
    for result in results:
        if (result.get("title") or "").lower() == title_lower:
            cache[cache_key] = result
            save_cache(cache)
            return result

    # Accept first result if first 6 words match
    if results:
        r0 = results[0]
        t_words = title_lower.split()[:6]
        r_words = (r0.get("title") or "").lower().split()[:6]
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

    print(f"\n  {path.name}")
    print(f"    title: {title[:60]}")

    result = search_paper(title, cache)
    time.sleep(delay)

    if not result:
        print("    not found on OpenAlex")
        return False

    changes = {}

    citations = result.get("cited_by_count")
    if citations is not None and meta.get("citations") != citations:
        changes["citations"] = citations
        changes["citations_updated"] = date.today().isoformat()

    # arXiv ID from external IDs
    ids = result.get("ids") or {}
    arxiv_id = ids.get("arxiv", "")
    if arxiv_id and not meta.get("arxiv_url"):
        # OpenAlex returns full URL like https://arxiv.org/abs/2301.12345
        arxiv_url = arxiv_id if arxiv_id.startswith("http") else f"https://arxiv.org/abs/{arxiv_id}"
        changes["arxiv_url"] = arxiv_url

    # Fallback: open-access PDF URL
    if not changes.get("arxiv_url") and not meta.get("arxiv_url"):
        oa_url = (result.get("open_access") or {}).get("oa_url", "")
        if oa_url and "arxiv.org" in oa_url:
            changes["arxiv_url"] = re.sub(r"/pdf/", "/abs/", oa_url).rstrip(".pdf")

    if not changes:
        print("    no updates")
        return False

    for k, v in changes.items():
        print(f"    {k}: {meta.get(k)!r} → {v!r}")

    if dry_run:
        return False

    meta.update(changes)
    post.metadata = meta
    with open(path, "w") as f:
        frontmatter.dump(post, f)
    return True


def main():
    parser = argparse.ArgumentParser(description="Fetch paper metadata from OpenAlex")
    parser.add_argument("--slug", help="Update only this paper slug")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Seconds between requests (default 0.5)")
    args = parser.parse_args()

    cache = load_cache()
    papers_dir = DATA / "papers"
    paths = [papers_dir / f"{args.slug}.md"] if args.slug else sorted(papers_dir.glob("*.md"))

    updated = 0
    for path in paths:
        if not path.exists():
            print(f"Not found: {path}")
            continue
        if update_paper(path, args.dry_run, cache, args.delay):
            updated += 1

    print(f"\n{'Would update' if args.dry_run else 'Updated'} {updated}/{len(paths)} papers.")
    if not os.environ.get("OA_EMAIL"):
        print("\nTip: set OA_EMAIL=you@email.com for higher rate limits (polite pool).")


if __name__ == "__main__":
    main()
