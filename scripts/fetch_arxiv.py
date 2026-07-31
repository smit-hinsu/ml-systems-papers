#!/usr/bin/env python3
"""Fetch missing arxiv_url fields via Semantic Scholar title search.

Reads all papers with arxiv_url: '', searches Semantic Scholar for each title,
updates the file if an arXiv ID is found. Serial with 0.75s delays to avoid 429s.

Usage:
  python scripts/fetch_arxiv.py            # process all missing
  python scripts/fetch_arxiv.py --dry-run  # show what would change, don't write
  python scripts/fetch_arxiv.py --limit 10 # process at most N papers
"""

import argparse
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parent.parent
PAPERS_DIR = ROOT / "data" / "papers"
ARXIV_API = "https://export.arxiv.org/api/query"
DELAY = 1.5  # seconds between requests (arXiv asks for ≥3s; 1.5s is safe for small batches)
NS = "http://www.w3.org/2005/Atom"


def search_arxiv_id(title: str) -> str | None:
    """Return arXiv ID string if found via arXiv title search, else None."""
    # Build a title query using key words (arXiv ti: field doesn't support phrases well)
    words = re.sub(r'[^a-zA-Z0-9 ]', ' ', title).split()
    # Use first 6 significant words to avoid over-constraining
    keywords = [w for w in words if len(w) > 2][:6]
    query = " AND ".join(f"ti:{w}" for w in keywords)
    params = urllib.parse.urlencode({"search_query": query, "max_results": 3})
    url = f"{ARXIV_API}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "mlsys26-indexer/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
    except Exception as exc:
        print(f"  ERROR fetching: {exc}")
        return None

    root = ET.fromstring(xml_data)
    for entry in root.findall(f"{{{NS}}}entry"):
        entry_title = entry.findtext(f"{{{NS}}}title") or ""
        entry_id = entry.findtext(f"{{{NS}}}id") or ""
        if _title_match(title, entry_title) and "arxiv.org/abs/" in entry_id:
            # Extract just the ID portion (e.g. "2603.05451v1" → "2603.05451")
            arxiv_id = entry_id.split("arxiv.org/abs/")[-1].split("v")[0]
            return arxiv_id
    return None


def _title_match(query: str, found: str) -> bool:
    """Loose title match: normalize and check word overlap."""
    def tokens(s):
        return set(re.sub(r'[^a-z0-9]', ' ', s.lower()).split())
    q, f = tokens(query), tokens(found)
    if not q or not f:
        return False
    overlap = len(q & f) / max(len(q), len(f))
    return overlap >= 0.6


def get_title(path: Path) -> str:
    """Extract title from YAML frontmatter without a full parse."""
    for line in path.read_text().splitlines():
        if line.startswith("title:"):
            # Handle both: title: 'Foo' and title: "Foo" and title: Foo
            val = line[6:].strip().strip("'\"")
            return val
    return path.stem


def update_arxiv_url(path: Path, arxiv_id: str) -> None:
    content = path.read_text()
    new_url = f"https://arxiv.org/abs/{arxiv_id}"
    content = content.replace("arxiv_url: ''", f"arxiv_url: '{new_url}'", 1)
    path.write_text(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    missing = [p for p in sorted(PAPERS_DIR.glob("*.md"))
               if "arxiv_url: ''" in p.read_text()]
    print(f"Found {len(missing)} papers missing arxiv_url")
    if args.limit:
        missing = missing[:args.limit]
        print(f"Processing first {args.limit}")

    found_count = 0
    for i, path in enumerate(missing):
        title = get_title(path)
        print(f"[{i+1}/{len(missing)}] {path.stem[:50]}")
        print(f"  title: {title[:70]}")

        arxiv_id = search_arxiv_id(title)
        if arxiv_id:
            url = f"https://arxiv.org/abs/{arxiv_id}"
            print(f"  FOUND: {url}")
            if not args.dry_run:
                update_arxiv_url(path, arxiv_id)
            found_count += 1
        else:
            print("  not found")

        if i < len(missing) - 1:
            time.sleep(DELAY)

    print(f"\nDone: {found_count}/{len(missing)} arxiv_urls found and {'(dry-run, not written)' if args.dry_run else 'written'}.")


if __name__ == "__main__":
    main()
