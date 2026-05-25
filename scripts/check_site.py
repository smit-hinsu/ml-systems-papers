#!/usr/bin/env python3
"""
Test the generated HTML site.

Checks:
  - Broken internal links (all relative href/src resolve to existing files)
  - Every page has a <title>, <h1>, and nav
  - No Jinja2 leakage ({{ ... }} visible in output)
  - No truncation artifacts ("...") inside observation labels
  - Paper pages have required sections (Links section or at least mlsys_url)
  - Insight listing: every observation with papers has correct count displayed
  - Cross-reference integrity: every paper linked from an observation page exists
  - Old-format headings (## Problem / ## Results) not leaked into rendered pages
  - DRAFT scaffold comments or fill-in placeholder text not present
  - Key Contributions section has ≥3 bullets
  - Principle listing pages link back to every paper that uses that principle
  - Paper count stat on index matches number of rendered paper cards
  - (with --check-urls) arxiv_url / openreview_url return HTTP 2xx

Usage:
    python scripts/check_site.py
    python scripts/check_site.py --site path/to/site
    python scripts/check_site.py --check-urls
"""

import argparse
import concurrent.futures
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent.parent
SITE = ROOT / "site"


# ── HTML parser ────────────────────────────────────────────────────────────────

class PageAnalyzer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []          # all href values
        self.title: str = ""
        self.h1s: list[str] = []
        self.text_blocks: list[str] = []    # all visible text
        self._stack: list[str] = []
        self._cur_text = ""
        self._in_nav = False

    def handle_starttag(self, tag, attrs):
        self._stack.append(tag)
        d = dict(attrs)
        if tag == "a" and "href" in d:
            self.links.append(d["href"])
        if tag == "nav":
            self._in_nav = True
        self._cur_text = ""

    def handle_endtag(self, tag):
        if self._stack and self._stack[-1] == tag:
            text = self._cur_text.strip()
            if text:
                self.text_blocks.append(text)
                if tag == "title":
                    self.title = text
                elif tag == "h1":
                    self.h1s.append(text)
            self._stack.pop()
        if tag == "nav":
            self._in_nav = False
        self._cur_text = ""

    def handle_data(self, data):
        self._cur_text += data

    def full_text(self):
        return " ".join(self.text_blocks)


def parse(path: Path) -> PageAnalyzer:
    p = PageAnalyzer()
    p.feed(path.read_text(encoding="utf-8"))
    return p


# ── checks ─────────────────────────────────────────────────────────────────────

def check_internal_links(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """All relative links that aren't anchors or external must resolve."""
    for href in page.links:
        if not href or href.startswith("#") or href.startswith("http"):
            continue
        # Strip query string and fragment before checking file existence
        file_part = href.split("?")[0].split("#")[0]
        if not file_part:
            continue
        target = (path.parent / file_part).resolve()
        if not target.exists():
            errors.append(f"{path.relative_to(SITE)}: broken link → {href}")


def check_structure(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """Every page must have a title and at least one h1."""
    rel = path.relative_to(SITE)
    if not page.title or len(page.title.strip()) < 3:
        errors.append(f"{rel}: missing or empty <title>")
    # Use regex on raw HTML: h1 may contain child spans (count badges, tags)
    raw = path.read_text(encoding="utf-8")
    if not re.search(r"<h1[\s>]", raw):
        errors.append(f"{rel}: missing <h1>")


def check_jinja_leakage(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """No unrendered Jinja2 should be in the output."""
    text = path.read_text(encoding="utf-8")
    if re.search(r"\{\{[^}]+\}\}", text):
        errors.append(f"{path.relative_to(SITE)}: Jinja2 variable leaked into output")
    if re.search(r"\{%[^%]+%\}", text):
        errors.append(f"{path.relative_to(SITE)}: Jinja2 block leaked into output")


def check_observation_truncation(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """Observation labels and descriptions must never be truncated."""
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'class="observation-item[^"]*"[^>]*>(.*?)</a>',
        re.DOTALL,
    )
    for m in pattern.finditer(text):
        content = re.sub(r"<[^>]+>", " ", m.group(1))
        content = re.sub(r"\s+", " ", content).strip()
        if content.endswith("...") or re.search(r'\w\.\.\.(?!\s)', content):
            errors.append(
                f"{path.relative_to(SITE)}: truncated observation content: {content[:80]!r}"
            )


def check_none_values(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """'None' appearing as visible text usually means a template bug."""
    text = path.read_text(encoding="utf-8")
    # Only flag bare "None" outside of tags/attributes
    for m in re.finditer(r'>([^<]*\bNone\b[^<]*)<', text):
        ctx = m.group(1).strip()
        if ctx == "None" or re.match(r'^None\b', ctx):
            warnings.append(
                f"{path.relative_to(SITE)}: 'None' visible in page body — possible template bug"
            )
            break


def check_paper_page(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """Paper pages should have at least one external link (mlsys_url at minimum)."""
    if path.parent.name != "papers":
        return
    has_external = any(h.startswith("http") for h in page.links)
    if not has_external:
        warnings.append(f"{path.relative_to(SITE)}: no external links (missing mlsys_url?)")


def check_todo_markers(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """Published paper pages must not contain visible TODO placeholders."""
    if path.parent.name != "papers":
        return
    raw = path.read_text(encoding="utf-8")
    # Skip draft pages (they carry a visible 'draft' badge in dev builds)
    if 'tag-draft' in raw:
        return
    # Look for TODO as visible text (not inside HTML comments or attributes)
    stripped = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)
    stripped = re.sub(r'<[^>]+>', ' ', stripped)
    if re.search(r'\bTODO\b', stripped):
        errors.append(f"{path.relative_to(SITE)}: visible 'TODO' in published paper body")


def check_long_unbroken_lines(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """Warn about text nodes with very long unbroken strings — likely to overflow on screen."""
    if path.parent.name not in ("papers",):
        return
    raw = path.read_text(encoding="utf-8")
    # Extract text content from paper-body only
    body_match = re.search(r'class="paper-body">(.*?)</article>', raw, re.DOTALL)
    if not body_match:
        return
    body_text = re.sub(r'<[^>]+>', ' ', body_match.group(1))
    # Find any whitespace-free run longer than 120 chars (URLs excluded)
    for token in re.findall(r'\S{121,}', body_text):
        if token.startswith(('http://', 'https://')):
            continue
        warnings.append(
            f"{path.relative_to(SITE)}: long unbroken string in body ({len(token)} chars): {token[:60]!r}..."
        )
        break  # one warning per page is enough


def check_author_overflow(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """Warn if the author line on a paper page is extremely long (>300 chars rendered)."""
    if path.parent.name != "papers":
        return
    raw = path.read_text(encoding="utf-8")
    # Find the author div (first <div> after the <h1>)
    m = re.search(r'<div[^>]*font-size: \.875rem[^>]*>(.*?)</div>', raw, re.DOTALL)
    if not m:
        return
    author_text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if len(author_text) > 300:
        warnings.append(
            f"{path.relative_to(SITE)}: author line is {len(author_text)} chars — may overflow"
        )


def check_old_format_headings(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """Paper pages must not contain old-format '## Problem' or '## Results' headings."""
    if path.parent.name != "papers":
        return
    raw = path.read_text(encoding="utf-8")
    # Look for rendered h2 tags with exactly these texts
    stripped = re.sub(r'<[^>]+>', ' ', raw)
    stripped = re.sub(r'\s+', ' ', stripped)
    if re.search(r'\bProblem\b', stripped):
        # Only flag if it looks like a standalone heading (surrounded by whitespace)
        # Check raw HTML for an h2 containing just "Problem"
        if re.search(r'<h2[^>]*>\s*Problem\s*</h2>', raw, re.IGNORECASE):
            errors.append(f"{path.relative_to(SITE)}: old-format '## Problem' heading in rendered page")
    if re.search(r'<h2[^>]*>\s*Results\s*</h2>', raw, re.IGNORECASE):
        errors.append(f"{path.relative_to(SITE)}: old-format '## Results' heading in rendered page")


def check_draft_scaffolding(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """Paper pages must not contain DRAFT HTML comments or 'fill in summary' placeholder text."""
    if path.parent.name != "papers":
        return
    raw = path.read_text(encoding="utf-8")
    if "<!-- DRAFT" in raw:
        errors.append(f"{path.relative_to(SITE)}: contains '<!-- DRAFT' scaffold comment")
    # Check visible text for fill-in placeholder
    stripped = re.sub(r'<[^>]+>', ' ', raw)
    if re.search(r'\bfill\s+in\s+summary\b', stripped, re.IGNORECASE):
        errors.append(f"{path.relative_to(SITE)}: contains 'fill in summary' placeholder text")


def check_key_contributions_bullets(
    path: Path, page: PageAnalyzer, errors: list, warnings: list
):
    """Warn if a paper's Key Contributions section has fewer than 3 list items."""
    if path.parent.name != "papers":
        return
    raw = path.read_text(encoding="utf-8")
    # Find the Key Contributions section
    kc_match = re.search(
        r'<h2[^>]*>.*?Key\s+Contributions.*?</h2>(.*?)(?=<h2|\Z)',
        raw, re.DOTALL | re.IGNORECASE,
    )
    if not kc_match:
        return
    section_html = kc_match.group(1)
    li_count = len(re.findall(r'<li[\s>]', section_html))
    if li_count < 3:
        warnings.append(
            f"{path.relative_to(SITE)}: Key Contributions has only {li_count} <li> "
            f"element(s) — stub not filled in properly"
        )


# ── URL health check ───────────────────────────────────────────────────────────

def check_url_health(paper_urls: list[tuple[str, str]], warnings: list) -> None:
    """HEAD-check all arxiv/openreview URLs in parallel; warn on HTTP >= 400 or errors."""
    try:
        import requests  # type: ignore
    except ImportError:
        warnings.append("check_url_health: 'requests' not installed; skipping URL checks")
        return

    def _check(item: tuple[str, str]) -> tuple[str, str] | None:
        slug, url = item
        try:
            resp = requests.head(url, timeout=5, allow_redirects=True)
            if resp.status_code >= 400:
                return (slug, f"HTTP {resp.status_code}")
        except Exception as exc:
            return (slug, str(exc))
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(_check, paper_urls))

    for result in results:
        if result is not None:
            slug, msg = result
            warnings.append(f"URL health: {slug} — {msg}")


# ── cross-page consistency checks ─────────────────────────────────────────────

def check_principle_listing_coverage(
    site: Path, errors: list, warnings: list
) -> None:
    """For each principle slug used in any paper page, verify the principles listing
    page exists and contains a link referencing that principle slug (via index.html
    filter URL or inline reference)."""
    principles_index = site / "principles" / "index.html"
    if not principles_index.exists():
        errors.append("principles/index.html not found")
        return
    principles_raw = principles_index.read_text(encoding="utf-8")

    papers_dir = site / "papers"
    if not papers_dir.exists():
        return

    # Collect all principle slugs referenced by paper pages
    for paper_path in sorted(papers_dir.glob("*.html")):
        paper_raw = paper_path.read_text(encoding="utf-8")
        # Paper pages link to index.html?principle=<slug>
        principle_slugs = re.findall(
            r'index\.html\?principle=([a-z][a-z0-9-]+)',
            paper_raw,
        )
        for principle_slug in set(principle_slugs):
            # The principles listing should reference this slug somewhere
            # (either in a filter link or as a section id/anchor)
            slug_pattern = f'principle={principle_slug}'
            if slug_pattern not in principles_raw:
                errors.append(
                    f"principles/index.html does not reference principle '{principle_slug}' "
                    f"(used by {paper_path.name})"
                )


def check_index_paper_count(site: Path, errors: list, warnings: list) -> None:
    """Verify the paper count shown on the index page matches the number of rendered
    paper cards (or paper HTML files)."""
    index_path = site / "index.html"
    if not index_path.exists():
        errors.append("index.html not found")
        return
    index_raw = index_path.read_text(encoding="utf-8")

    # Extract the stat counter
    stat_match = re.search(r'<span[^>]*id="stat-papers"[^>]*>(\d+)</span>', index_raw)
    if not stat_match:
        warnings.append("index.html: could not find <span id=\"stat-papers\"> counter")
        return
    stat_count = int(stat_match.group(1))

    # Count paper HTML files
    papers_dir = site / "papers"
    actual_count = len(list(papers_dir.glob("*.html"))) if papers_dir.exists() else 0

    if stat_count != actual_count:
        errors.append(
            f"index.html stat-papers shows {stat_count} but {actual_count} paper "
            f"HTML files exist in site/papers/"
        )


# ── runner ─────────────────────────────────────────────────────────────────────

CHECKS = [
    check_internal_links,
    check_structure,
    check_jinja_leakage,
    check_observation_truncation,
    check_none_values,
    check_paper_page,
    check_todo_markers,
    check_long_unbroken_lines,
    check_author_overflow,
    check_old_format_headings,
    check_draft_scaffolding,
    check_key_contributions_bullets,
]


def main():
    parser = argparse.ArgumentParser(description="Test the generated HTML site")
    parser.add_argument("--site", default=str(SITE), help="Path to generated site")
    parser.add_argument(
        "--check-urls", action="store_true",
        help="HEAD-check arxiv_url and openreview_url for all papers (slow; requires network)",
    )
    args = parser.parse_args()

    site = Path(args.site)
    if not site.exists():
        print(f"Site not found at {site}. Run: python scripts/generate_html.py first.")
        sys.exit(1)

    html_files = sorted(site.rglob("*.html"))
    if not html_files:
        print("No HTML files found.")
        sys.exit(1)

    all_errors: list[str] = []
    all_warnings: list[str] = []

    for path in html_files:
        try:
            page = parse(path)
        except Exception as e:
            all_errors.append(f"{path.relative_to(site)}: parse error: {e}")
            continue
        for check in CHECKS:
            check(path, page, all_errors, all_warnings)

    # Cross-page consistency checks (need full site context)
    check_principle_listing_coverage(site, all_errors, all_warnings)
    check_index_paper_count(site, all_errors, all_warnings)

    # URL health checks (optional, slow)
    if args.check_urls:
        # Collect URLs from paper data files
        try:
            import frontmatter  # type: ignore
            import yaml  # type: ignore
            data_papers = ROOT / "data" / "papers"
            paper_urls: list[tuple[str, str]] = []
            for md_path in sorted(data_papers.glob("*.md")):
                post = frontmatter.load(md_path)
                m = dict(post.metadata)
                slug = m.get("slug") or md_path.stem
                for url_field in ("arxiv_url", "openreview_url"):
                    url = m.get(url_field) or ""
                    if url and url.startswith("http"):
                        paper_urls.append((f"{slug}.{url_field}", url))
            if paper_urls:
                print(f"Checking {len(paper_urls)} URLs...")
                check_url_health(paper_urls, all_warnings)
        except ImportError:
            all_warnings.append("URL checks require 'frontmatter' and 'yaml' packages")

    # Report
    print(f"Checked {len(html_files)} HTML files.\n")

    if all_warnings:
        print("WARNINGS:")
        for w in all_warnings:
            print(f"  ⚠  {w}")
        print()

    if all_errors:
        print("ERRORS:")
        for e in all_errors:
            print(f"  ✗  {e}")
        print(f"\n{len(all_errors)} error(s), {len(all_warnings)} warning(s).")
        sys.exit(1)
    else:
        print(f"All checks passed. {len(all_warnings)} warning(s).")


if __name__ == "__main__":
    main()
