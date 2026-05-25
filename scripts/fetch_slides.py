#!/usr/bin/env python3
"""
Fetch slides, OpenReview, and arXiv links from conference virtual pages.

Supports any conference with a virtual site. Built-in configs for MLSys;
other venues can be added to VENUE_CONFIGS or specified via --base-url.

First run opens a headed browser for login (if the site requires it); session
is saved per-venue to data/.auth_<venue>.json for subsequent headless runs.

Usage:
    # Update existing papers' slides + OpenReview links (default: mlsys-2026):
    python scripts/fetch_slides.py

    # Different venue:
    python scripts/fetch_slides.py --venue mlsys-2025

    # Discover all papers from the conference calendar, create stubs:
    python scripts/fetch_slides.py --discover --create-stubs

    # Just print what was found without writing:
    python scripts/fetch_slides.py --discover --dry-run

    # Force re-login:
    python scripts/fetch_slides.py --relogin

    # Single paper by slug:
    python scripts/fetch_slides.py --slug vescale-fsdp

    # Specific URLs (works with any conference):
    python scripts/fetch_slides.py --urls https://mlsys.org/virtual/2026/oral/3834

    # Custom venue not in VENUE_CONFIGS:
    python scripts/fetch_slides.py --base-url https://example.org --venue myconf-2026 --urls <url>
"""

import argparse
import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import frontmatter

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
PAPERS_DIR = DATA / "papers"


# ---------------------------------------------------------------------------
# Venue configs
# ---------------------------------------------------------------------------

VENUE_CONFIGS = {
    "mlsys-2026": {
        "base_url": "https://mlsys.org",
        "login_url": "https://mlsys.org/login",
        "calendar_url": "https://mlsys.org/virtual/2026/calendar",
        "paper_url_re": re.compile(r"/virtual/2026/oral/(\d+)"),
        "venue_slug": "mlsys-2026",
        "login_required": True,
    },
    "mlsys-2025": {
        "base_url": "https://mlsys.org",
        "login_url": "https://mlsys.org/login",
        "calendar_url": "https://mlsys.org/virtual/2025/calendar",
        "paper_url_re": re.compile(r"/virtual/2025/oral/(\d+)"),
        "venue_slug": "mlsys-2025",
        "login_required": True,
    },
}


def get_venue_config(venue_slug: str, base_url: str | None = None) -> dict:
    if venue_slug in VENUE_CONFIGS:
        return VENUE_CONFIGS[venue_slug]
    if base_url:
        return {
            "base_url": base_url.rstrip("/"),
            "login_url": f"{base_url.rstrip('/')}/login",
            "calendar_url": None,
            "paper_url_re": None,
            "venue_slug": venue_slug,
            "login_required": False,
        }
    sys.exit(
        f"Unknown venue {venue_slug!r}. Add it to VENUE_CONFIGS in fetch_slides.py "
        f"or supply --base-url."
    )


# ---------------------------------------------------------------------------
# Paper stub template
# ---------------------------------------------------------------------------

STUB_TEMPLATE = '''\
---
# Identity
title: "{title}"
slug: "{slug}"
authors: {authors}
organizations: []

# Links
venue_url: "{venue_url}"
openreview_url: "{openreview_url}"
arxiv_url: "{arxiv_url}"
slides_url: "{slides_url}"
code_url: ""
project_url: ""

# Venue metadata
venue: "{venue_slug}"
official_category: ""
presentation_type: oral
award: ""
arxiv_date: ""

# User taxonomy
domain: []
topics: []
principles: []  # see data/principles.yaml for valid slugs
observations: {}  # slug: "one sentence — what the authors specifically observed"

# Evaluation
hardware: []
models_evaluated: []
agentic_models: []

# Impact
citations: null
citations_updated: ""
research_or_industry: ""

# Quick-scan fields
problem: ""
key_results: ""

# Publishing
status: draft  # draft | published — only published papers appear on the site by default

# Reading/indexing
reading_status: want-to-read
indexed_by: ""
indexed_date: "{indexed_date}"
---

<!-- DRAFT: fill in sections before publishing. See docs/summarizing.md -->

## Problem

<!-- 2–3 sentences expanding on the `problem` field. Why does this matter at scale? -->

{abstract}

## Key Contributions

<!-- 3–5 bullets. Each = concrete artifact (named algorithm, data structure, protocol)
     with a brief mechanism. Not "we show X is possible." -->

- TODO

## Results

<!-- Key numbers: metric + value + hardware + model + baseline. -->

- TODO

## Trade-offs

<!-- What does the approach give up? Leave empty if nothing notable. -->

## Nuances

<!-- Gotchas, subtle assumptions, conditions that break the approach, limitations.
     Leave empty if nothing notable. -->
'''


def slugify(title):
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")[:60]


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def load_papers(slug_filter=None):
    papers = []
    for path in sorted(PAPERS_DIR.glob("*.md")):
        post = frontmatter.load(path)
        meta = dict(post.metadata)
        meta["_path"] = path
        slug = meta.get("slug") or path.stem
        meta["slug"] = slug
        if slug_filter and slug != slug_filter:
            continue
        if meta.get("venue_url"):
            papers.append(meta)
    return papers


def known_venue_urls():
    urls = set()
    for path in PAPERS_DIR.glob("*.md"):
        post = frontmatter.load(path)
        u = post.metadata.get("venue_url", "")
        if u:
            urls.add(u.rstrip("/"))
    return urls


def save_paper(paper, updates, dry_run=False):
    path = paper["_path"]
    post = frontmatter.load(path)
    changed = []
    for key, val in updates.items():
        if post.metadata.get(key) != val:
            post.metadata[key] = val
            changed.append(f"{key}={val!r}")
    if not changed:
        print(f"  {paper['slug']}: no changes")
        return
    if dry_run:
        print(f"  {paper['slug']} [dry-run]: {', '.join(changed)}")
        return
    with open(path, "w") as f:
        frontmatter.dump(post, f)
    print(f"  {paper['slug']}: updated {', '.join(changed)}")


def create_stub(data, cfg: dict, dry_run=False):
    title = data.get("title", "")
    if not title:
        print(f"  skip (no title): {data.get('venue_url')}")
        return
    slug = slugify(title)
    dest = PAPERS_DIR / f"{slug}.md"
    if dest.exists():
        print(f"  skip (exists): {slug}.md")
        return

    authors_yaml = json.dumps(data.get("authors") or [])
    abstract = data.get("abstract") or "TODO"
    sentences = re.split(r'(?<=[.!?])\s+', abstract)
    abstract_body = " ".join(sentences[:3])

    content = STUB_TEMPLATE.format(
        title=title.replace('"', '\\"'),
        slug=slug,
        authors=authors_yaml,
        venue_url=data.get("venue_url", ""),
        openreview_url=data.get("openreview_url", ""),
        arxiv_url=data.get("arxiv_url", ""),
        slides_url=data.get("slides_url", ""),
        indexed_date=date.today().isoformat(),
        abstract=abstract_body,
        venue_slug=cfg["venue_slug"],
    )

    if dry_run:
        print(f"  [dry-run] would create: {dest.name}")
        print(f"    title: {title}")
        if data.get("slides_url"):
            print(f"    slides: {data['slides_url']}")
        if data.get("openreview_url"):
            print(f"    openreview: {data['openreview_url']}")
        return

    dest.write_text(content)
    print(f"  created: {dest.name}")


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def do_login_sync(login_url: str):
    from playwright.sync_api import sync_playwright
    domain = urlparse(login_url).netloc
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(login_url)
        print(f"\nLog in to {domain} in the browser window, then press Enter here...")
        input()
        state = ctx.storage_state()
        browser.close()
    return state


def get_storage_state(cfg: dict, relogin=False):
    if not cfg.get("login_required"):
        return None
    venue_slug = cfg["venue_slug"]
    auth_file = DATA / f".auth_{venue_slug}.json"
    if auth_file.exists() and not relogin:
        print(f"Using saved session from {auth_file.name}")
        return json.loads(auth_file.read_text())
    print(f"No saved session for {venue_slug} — opening browser for login...")
    state = do_login_sync(cfg["login_url"])
    auth_file.write_text(json.dumps(state))
    print(f"Session saved to {auth_file.name}")
    return state


# ---------------------------------------------------------------------------
# Async scraping
# ---------------------------------------------------------------------------

async def scrape_paper_page(page, url, base_url: str):
    """Visit one paper page and extract all useful data. Works with any conference site."""
    await page.goto(url, wait_until="networkidle", timeout=30_000)
    await page.wait_for_timeout(400)

    result = {"venue_url": url}

    # Title
    h1 = page.locator("h1").first
    if await h1.count():
        result["title"] = (await h1.text_content() or "").strip()

    # Authors: line with ⋅ separator
    body_text = await page.locator("body").inner_text()
    for line in body_text.split("\n"):
        line = line.strip()
        if "⋅" in line and len(line) < 400:
            authors = [a.strip() for a in line.split("⋅") if a.strip()]
            if authors:
                result["authors"] = authors
                break

    # Abstract
    abstracts = await page.locator("[class*='abstract']").all()
    for el in abstracts:
        text = (await el.text_content() or "").strip()
        if len(text) > 100:
            result["abstract"] = text
            break

    # Slides
    for a in await page.locator("a").all():
        text = (await a.text_content() or "").strip()
        href = (await a.get_attribute("href") or "").strip()
        if not href:
            continue
        if text.lower() == "slides":
            result["slides_url"] = href if href.startswith("http") else f"{base_url}{href}"
            break

    # OpenReview
    for a in await page.locator("a[href*='openreview.net']").all():
        href = (await a.get_attribute("href") or "").strip()
        if href:
            if "/pdf" in href:
                href = href.replace("/pdf", "/forum")
            result["openreview_url"] = href
            break

    # arXiv
    for a in await page.locator("a[href*='arxiv.org']").all():
        href = (await a.get_attribute("href") or "").strip()
        if href:
            href = re.sub(r"/pdf/", "/abs/", href).rstrip(".pdf")
            result["arxiv_url"] = href
            break

    return result


async def discover_paper_urls(ctx, cfg: dict):
    """Scrape the calendar/proceedings page and return {id: url} for all papers."""
    if not cfg.get("calendar_url") or not cfg.get("paper_url_re"):
        sys.exit("--discover requires a venue with calendar_url and paper_url_re configured.")
    page = await ctx.new_page()
    base_url = cfg["base_url"]
    urls = {}
    try:
        await page.goto(cfg["calendar_url"], wait_until="networkidle", timeout=30_000)
        for a in await page.locator("a[href*='/oral/']").all():
            href = await a.get_attribute("href") or ""
            m = cfg["paper_url_re"].search(href)
            if m:
                oid = m.group(1)
                full = f"{base_url}{href}" if href.startswith("/") else href
                urls[oid] = full
    finally:
        await page.close()
    return urls


async def run_async(papers, storage_state, concurrency, discover, create_stubs, dry_run, cfg, specific_urls=None):
    from playwright.async_api import async_playwright

    base_url = cfg["base_url"]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx_kwargs = {"storage_state": storage_state} if storage_state else {}
        ctx = await browser.new_context(**ctx_kwargs)
        sem = asyncio.Semaphore(concurrency)

        # ---- Discovery ----
        if discover:
            print(f"Discovering papers from {cfg['venue_slug']} ...")
            all_urls = await discover_paper_urls(ctx, cfg)
            known = known_venue_urls()
            new_urls = {oid: url for oid, url in all_urls.items()
                        if url.rstrip("/") not in known}
            print(f"Found {len(all_urls)} papers total, {len(new_urls)} not in index yet.")

            if new_urls:
                async def scrape_new(oid, url):
                    async with sem:
                        page = await ctx.new_page()
                        try:
                            print(f"  {oid} ...")
                            return await scrape_paper_page(page, url, base_url)
                        except Exception as e:
                            print(f"  {oid} error: {e}")
                            return {"venue_url": url}
                        finally:
                            await page.close()

                results = await asyncio.gather(
                    *[scrape_new(k, v) for k, v in sorted(new_urls.items())]
                )

                print(f"\n{'Creating' if create_stubs else 'Found'} {len(results)} new papers:")
                for data in results:
                    if create_stubs:
                        create_stub(data, cfg=cfg, dry_run=dry_run)
                    else:
                        title = data.get("title", "(unknown)")
                        url = data.get("venue_url", "")
                        print(f"  {title[:70]}  [{url.split('/')[-1]}]")

        # ---- Specific URLs ----
        if specific_urls:
            print(f"Scraping {len(specific_urls)} specific URLs ...")
            known = known_venue_urls()

            async def scrape_specific(url):
                async with sem:
                    page = await ctx.new_page()
                    try:
                        oid = url.rstrip("/").split("/")[-1]
                        print(f"  {oid} ...")
                        return await scrape_paper_page(page, url, base_url)
                    except Exception as e:
                        print(f"  {url}: error: {e}")
                        return {"venue_url": url}
                    finally:
                        await page.close()

            results = await asyncio.gather(*[scrape_specific(u) for u in specific_urls])
            for data in results:
                if data.get("venue_url", "").rstrip("/") in known:
                    print(f"  skipping {data.get('title', data['venue_url'])!r} — already indexed")
                else:
                    create_stub(data, cfg=cfg, dry_run=dry_run)

        # ---- Update existing papers ----
        if papers:
            print(f"\nUpdating {len(papers)} existing papers (concurrency={concurrency}) ...")

            async def update_one(paper):
                async with sem:
                    url = paper["venue_url"]
                    page = await ctx.new_page()
                    try:
                        data = await scrape_paper_page(page, url, base_url)
                    except Exception as e:
                        print(f"  {paper['slug']}: error: {e}")
                        return
                    finally:
                        await page.close()

                    updates = {}
                    for field in ("slides_url", "openreview_url", "arxiv_url"):
                        val = data.get(field)
                        if val and not paper.get(field):
                            updates[field] = val
                    save_paper(paper, updates, dry_run=dry_run)

            await asyncio.gather(*[update_one(p) for p in papers])

        await browser.close()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fetch slides and links from conference virtual pages")
    parser.add_argument("--venue", default="mlsys-2026",
                        help="Venue slug from VENUE_CONFIGS (default: mlsys-2026)")
    parser.add_argument("--base-url", metavar="URL",
                        help="Base URL for venues not in VENUE_CONFIGS")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would change without writing")
    parser.add_argument("--relogin", action="store_true",
                        help="Force new browser login (for venues that require auth)")
    parser.add_argument("--slug", help="Process only this paper slug")
    parser.add_argument("--discover", action="store_true",
                        help="Find all papers from the venue calendar and create stubs")
    parser.add_argument("--create-stubs", action="store_true",
                        help="With --discover: create stub .md files for new papers")
    parser.add_argument("--concurrency", type=int, default=4,
                        help="Parallel browser pages (default 4)")
    parser.add_argument("--urls", nargs="+", metavar="URL",
                        help="Specific paper URLs to scrape and create stubs for")
    args = parser.parse_args()

    cfg = get_venue_config(args.venue, base_url=args.base_url)
    storage_state = get_storage_state(cfg, relogin=args.relogin)
    papers = load_papers(args.slug)

    if not papers and not args.discover and not args.urls:
        print("No papers with venue_url found.")
        return

    asyncio.run(run_async(
        papers, storage_state, args.concurrency,
        args.discover, args.create_stubs, args.dry_run, cfg,
        specific_urls=args.urls or [],
    ))
    print("\nDone.")


if __name__ == "__main__":
    main()
