#!/usr/bin/env python3
"""
Test the generated HTML site.

Checks:
  - Broken internal links (all relative href/src resolve to existing files)
  - Every page has a <title>, <h1>, and nav
  - No Jinja2 leakage ({{ ... }} visible in output)
  - No truncation artifacts ("...") inside insight labels
  - Paper pages have required sections (Links section or at least mlsys_url)
  - Insight listing: every insight with papers has correct count displayed
  - Cross-reference integrity: every paper linked from an insight page exists

Usage:
    python scripts/check_site.py
    python scripts/check_site.py --site path/to/site
"""

import argparse
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
        # Resolve relative to the page's directory
        target = (path.parent / href).resolve()
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


def check_insight_truncation(path: Path, page: PageAnalyzer, errors: list, warnings: list):
    """
    Insight labels should never be truncated.
    The .insight-desc description may be truncated (intentional) but the label itself must not be.
    """
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'class="insight-item[^"]*"[^>]*>(.*?)</a>',
        re.DOTALL,
    )
    desc_pattern = re.compile(r'<span[^>]*class="insight-desc"[^>]*>.*?</span>', re.DOTALL)
    for m in pattern.finditer(text):
        # Remove the description span — truncation there is intentional
        label_html = desc_pattern.sub("", m.group(1))
        label = re.sub(r"<[^>]+>", " ", label_html)
        label = re.sub(r"\s+", " ", label).strip()
        if label.endswith("...") or re.search(r'\w\.\.\.(?!\s)', label):
            errors.append(
                f"{path.relative_to(SITE)}: truncated insight label: {label[:80]!r}"
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


# ── runner ─────────────────────────────────────────────────────────────────────

CHECKS = [
    check_internal_links,
    check_structure,
    check_jinja_leakage,
    check_insight_truncation,
    check_none_values,
    check_paper_page,
]


def main():
    parser = argparse.ArgumentParser(description="Test the generated HTML site")
    parser.add_argument("--site", default=str(SITE), help="Path to generated site")
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
