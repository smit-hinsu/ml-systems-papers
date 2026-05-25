#!/usr/bin/env python3
"""
Fetch slides/PDF links from MLSys virtual pages, with optional discovery
of all oral papers on the conference site.

First run opens a headed browser for login; session is saved to
data/.mlsys_auth.json for subsequent headless runs.

Usage:
    # Update existing papers with slides + OpenReview links (default year: 2026):
    python scripts/fetch_mlsys_slides.py

    # Different year:
    python scripts/fetch_mlsys_slides.py --year 2025

    # Discover all orals, create stub .md files:
    python scripts/fetch_mlsys_slides.py --discover --create-stubs

    # Just print what was found without writing:
    python scripts/fetch_mlsys_slides.py --discover --dry-run

    # Force re-login:
    python scripts/fetch_mlsys_slides.py --relogin

    # Single paper:
    python scripts/fetch_mlsys_slides.py --slug vescale-fsdp

    # More parallel pages:
    python scripts/fetch_mlsys_slides.py --discover --concurrency 8
"""

import argparse
import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path

import frontmatter

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
PAPERS_DIR = DATA / "papers"
AUTH_FILE = DATA / ".mlsys_auth.json"
MLSYS_LOGIN = "https://mlsys.org/login"


def mlsys_urls(year: int):
    base = f"https://mlsys.org/virtual/{year}"
    return {
        "calendar": f"{base}/calendar",
        "oral_re": re.compile(rf"/virtual/{year}/oral/(\d+)"),
        "venue_slug": f"mlsys-{year}",
    }


# ---------------------------------------------------------------------------
# Paper stub template (mirrors new_paper.py)
# ---------------------------------------------------------------------------

STUB_TEMPLATE = '''\
---
# Identity
title: "{title}"
slug: "{slug}"
authors: {authors}
organizations: []

# Links
mlsys_url: "{mlsys_url}"
openreview_url: "{openreview_url}"
arxiv_url: "{arxiv_url}"
slides_url: "{slides_url}"
code_url: ""
project_url: ""

# MLSys metadata
venue: "{venue_slug}"
mlsys_official_category: ""
presentation_type: oral
award: ""
date: "{year}-05"

# User taxonomy
domain: []
topics: []
observations: []

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

# Reading/indexing
reading_status: want-to-read
indexed_by: ""
indexed_date: "{indexed_date}"
---

## Summary

{abstract}

## Key Contributions

- TODO

## Method

TODO

## Results

TODO

## Limitations

TODO

## Personal Notes

<!-- Add your own observations, questions, and connections to other work here -->
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
        if meta.get("mlsys_url"):
            papers.append(meta)
    return papers


def known_mlsys_urls():
    urls = set()
    for path in PAPERS_DIR.glob("*.md"):
        post = frontmatter.load(path)
        u = post.metadata.get("mlsys_url", "")
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


def create_stub(data, venue_slug, year, dry_run=False):
    title = data.get("title", "")
    if not title:
        print(f"  skip (no title): {data.get('mlsys_url')}")
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
        mlsys_url=data.get("mlsys_url", ""),
        openreview_url=data.get("openreview_url", ""),
        arxiv_url=data.get("arxiv_url", ""),
        slides_url=data.get("slides_url", ""),
        indexed_date=date.today().isoformat(),
        abstract=abstract_body,
        venue_slug=venue_slug,
        year=year,
    )

    if dry_run:
        print(f"  [dry-run] would create: {dest.name}")
        print(f"    title: {title}")
        print(f"    authors: {authors_yaml}")
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

def do_login_sync():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(MLSYS_LOGIN)
        print("\nLog in to mlsys.org in the browser window, then press Enter here...")
        input()
        state = ctx.storage_state()
        browser.close()
    return state


def get_storage_state(relogin=False):
    if AUTH_FILE.exists() and not relogin:
        print(f"Using saved session from {AUTH_FILE.name}")
        return json.loads(AUTH_FILE.read_text())
    print("No saved session — opening browser for login...")
    state = do_login_sync()
    AUTH_FILE.write_text(json.dumps(state))
    print(f"Session saved to {AUTH_FILE.name}")
    return state


# ---------------------------------------------------------------------------
# Async scraping
# ---------------------------------------------------------------------------

async def scrape_oral_page(page, url):
    """Visit one oral page and extract all useful data."""
    await page.goto(url, wait_until="networkidle", timeout=30_000)
    await page.wait_for_timeout(400)

    result = {"mlsys_url": url}

    # Title
    h1 = page.locator("h1").first
    if await h1.count():
        result["title"] = (await h1.text_content() or "").strip()

    # Authors: look for a line with ⋅ separator in body text
    body_text = await page.locator("body").inner_text()
    for line in body_text.split("\n"):
        line = line.strip()
        if "⋅" in line and len(line) < 400:
            authors = [a.strip() for a in line.split("⋅") if a.strip()]
            if authors:
                result["authors"] = authors
                break

    # Abstract: third [class*='abstract'] element is the full text
    abstracts = await page.locator("[class*='abstract']").all()
    for el in abstracts:
        text = (await el.text_content() or "").strip()
        if len(text) > 100:
            result["abstract"] = text
            break

    # Slides: link with text "Slides"
    for a in await page.locator("a").all():
        text = (await a.text_content() or "").strip()
        href = (await a.get_attribute("href") or "").strip()
        if not href:
            continue
        if text.lower() == "slides":
            result["slides_url"] = href if href.startswith("http") else f"https://mlsys.org{href}"
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


async def get_all_oral_urls(ctx, url_cfg):
    """Scrape the calendar page and return {id: url} for all oral papers."""
    page = await ctx.new_page()
    urls = {}
    try:
        await page.goto(url_cfg["calendar"], wait_until="networkidle", timeout=30_000)
        for a in await page.locator("a[href*='/oral/']").all():
            href = await a.get_attribute("href") or ""
            m = url_cfg["oral_re"].search(href)
            if m:
                oid = m.group(1)
                full = f"https://mlsys.org{href}" if href.startswith("/") else href
                urls[oid] = full
    finally:
        await page.close()
    return urls


async def run_async(papers, storage_state, concurrency, discover, create_stubs, dry_run, url_cfg):
    from playwright.async_api import async_playwright

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(storage_state=storage_state)
        sem = asyncio.Semaphore(concurrency)

        venue_slug = url_cfg["venue_slug"]
        year = int(venue_slug.split("-")[1])

        # ---- Discovery: all orals from calendar ----
        if discover:
            print(f"Scraping {venue_slug} calendar for oral URLs ...")
            all_urls = await get_all_oral_urls(ctx, url_cfg)
            known = known_mlsys_urls()
            new_urls = {oid: url for oid, url in all_urls.items()
                        if url.rstrip("/") not in known}
            print(f"Found {len(all_urls)} orals total, {len(new_urls)} not in index yet.")

            if new_urls:
                async def scrape_new(oid, url):
                    async with sem:
                        page = await ctx.new_page()
                        try:
                            print(f"  oral/{oid} ...")
                            return await scrape_oral_page(page, url)
                        except Exception as e:
                            print(f"  oral/{oid} error: {e}")
                            return {"mlsys_url": url}
                        finally:
                            await page.close()

                results = await asyncio.gather(
                    *[scrape_new(k, v) for k, v in sorted(new_urls.items())]
                )

                print(f"\n{'Creating' if create_stubs else 'Found'} {len(results)} new oral papers:")
                for data in results:
                    if create_stubs:
                        create_stub(data, venue_slug=venue_slug, year=year, dry_run=dry_run)
                    else:
                        title = data.get("title", "(unknown)")
                        url = data.get("mlsys_url", "")
                        print(f"  {title[:70]}  [{url.split('/')[-1]}]")

        # ---- Update existing papers ----
        if papers:
            print(f"\nUpdating {len(papers)} existing papers (concurrency={concurrency}) ...")

            async def update_one(paper):
                async with sem:
                    url = paper["mlsys_url"]
                    page = await ctx.new_page()
                    try:
                        data = await scrape_oral_page(page, url)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2026,
                        help="MLSys conference year (default 2026)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would change without writing")
    parser.add_argument("--relogin", action="store_true",
                        help="Force new browser login")
    parser.add_argument("--slug", help="Process only this paper slug")
    parser.add_argument("--discover", action="store_true",
                        help="Find all oral papers on the MLSys calendar")
    parser.add_argument("--create-stubs", action="store_true",
                        help="With --discover: create stub .md files for new papers")
    parser.add_argument("--concurrency", type=int, default=4,
                        help="Parallel browser pages (default 4)")
    args = parser.parse_args()

    url_cfg = mlsys_urls(args.year)
    storage_state = get_storage_state(relogin=args.relogin)
    papers = load_papers(args.slug)

    if not papers and not args.discover:
        print("No papers with mlsys_url found.")
        return

    asyncio.run(run_async(
        papers, storage_state, args.concurrency,
        args.discover, args.create_stubs, args.dry_run, url_cfg,
    ))
    print("\nDone.")


if __name__ == "__main__":
    main()
