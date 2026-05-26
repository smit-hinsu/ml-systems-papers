#!/usr/bin/env python3
"""Generate static HTML site from data files."""

import argparse
import re
import shutil
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote_plus

import frontmatter
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"
SITE = ROOT / "site"


def load_registry(filename):
    with open(DATA / filename) as f:
        return yaml.safe_load(f)


def load_papers():
    papers = []
    for path in sorted((DATA / "papers").glob("*.md")):
        post = frontmatter.load(path)
        meta = dict(post.metadata)
        # Strip empty "## Personal Notes" heading from body so it doesn't render
        body = re.sub(r'\n## Personal Notes\s*\n<!--.*?-->\s*$', '', post.content, flags=re.DOTALL)
        body = re.sub(r'\n## Personal Notes\s*$', '', body.rstrip())
        meta["body_html"] = markdown.markdown(
            body,
            extensions=["tables", "fenced_code", "toc"],
        )
        meta["slug"] = meta.get("slug") or path.stem
        papers.append(meta)
    return papers


_PRESENTATION_RANK = {"oral": 1, "spotlight": 2, "poster": 3}
_STATUS_RANK = {"published": 0, "under-review": 1, "draft": 2}


class _Desc(str):
    """String wrapper that reverses comparison, for descending alpha tiebreaks."""
    def __lt__(self, other): return str.__gt__(self, other)
    def __gt__(self, other): return str.__lt__(self, other)
    def __le__(self, other): return str.__ge__(self, other)
    def __ge__(self, other): return str.__le__(self, other)


def sort_papers(papers):
    # TODO: revisit this ordering when the index includes non-MLSys venues —
    # award tiers and presentation types aren't standardized across conferences.
    def key(p):
        status_rank = _STATUS_RANK.get(p.get("status") or "draft", 2)
        award_rank = 0 if p.get("award") else 1
        ptype_rank = _PRESENTATION_RANK.get(p.get("presentation_type") or "", 99)
        citations = -(p.get("citations") or 0)
        date = _Desc(p.get("arxiv_date") or "")
        return (status_rank, award_rank, ptype_rank, citations, date, _Desc(p.get("title") or ""))

    return sorted(papers, key=key)


def build_index(papers, principles, domains, topics, venues):
    """Build cross-reference maps."""
    by_principle = defaultdict(list)
    by_domain = defaultdict(list)
    by_topic = defaultdict(list)
    by_status = defaultdict(list)

    for paper in papers:
        for slug in paper.get("principles") or []:
            by_principle[slug].append(paper)
        for slug in paper.get("domain") or []:
            by_domain[slug].append(paper)
        for slug in paper.get("topics") or []:
            by_topic[slug].append(paper)
        status = paper.get("reading_status") or "unread"
        by_status[status].append(paper)

    return {
        "by_principle": dict(by_principle),
        "by_domain": dict(by_domain),
        "by_topic": dict(by_topic),
        "by_status": dict(by_status),
    }


def build_search_index(papers, principles, domains, topics, venues):
    """Build the search index embedded at build time."""
    records = []
    for p in papers:
        v = venues.get(p.get("venue") or "", {})
        records.append({
            "slug": p["slug"],
            "url": f"papers/{p['slug']}.html",
            "title": p.get("title") or "",
            "authors": p.get("authors") or [],
            "organizations": p.get("organizations") or [],
            "problem": p.get("problem") or "",
            "key_results": p.get("key_results") or "",
            "domain_labels": [domains[d]["label"] for d in (p.get("domain") or []) if d in domains],
            "topic_labels": [topics[t]["label"] for t in (p.get("topics") or []) if t in topics],
            "hardware": p.get("hardware") or [],
            "principle_slugs": [o for o in (p.get("principles") or []) if o in principles],
            "principle_labels": [principles[o]["label"] for o in (p.get("principles") or []) if o in principles],
            "venue": p.get("venue") or "",
            "venue_short": v.get("short") or "",
        })
    return records


def render(env, template_name, dest, **ctx):
    tmpl = env.get_template(template_name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(tmpl.render(**ctx))
    print(f"  wrote {dest.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Generate ML Systems Papers static site")
    parser.add_argument("--output", default=str(SITE), help="Output directory")
    parser.add_argument("--clean", action="store_true", help="Remove output dir first")
    parser.add_argument("--dev", action="store_true",
                        help="Include draft papers (marked visually); off by default")
    args = parser.parse_args()

    out = Path(args.output)
    if args.clean and out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["urlencode"] = quote_plus
    env.policies["json.dumps_kwargs"] = {"ensure_ascii": False}

    # Load data
    site = load_registry("site.yaml")
    venues = load_registry("venues.yaml")
    principles = load_registry("principles.yaml")
    domains = load_registry("domains.yaml")
    topics = load_registry("topics.yaml")
    all_loaded = load_papers()
    papers = all_loaded if args.dev else [p for p in all_loaded if p.get("status") == "published"]
    if not args.dev:
        excluded = len(all_loaded) - len(papers)
        if excluded:
            print(f"Skipping {excluded} non-published paper(s). Use --dev to include them.")
    index = build_index(papers, principles, domains, topics, venues)

    def sorted_by_count(registry, paper_index):
        return dict(sorted(registry.items(),
                           key=lambda kv: len(paper_index.get(kv[0], [])),
                           reverse=True))

    ctx = dict(
        site=site,
        venues=venues,
        principles=sorted_by_count(principles, index["by_principle"]),
        domains=sorted_by_count(domains, index["by_domain"]),
        topics=sorted_by_count(topics, index["by_topic"]),
        all_papers=sort_papers(papers),
        index=index,
        dev_mode=args.dev,
    )

    print("Generating paper pages...")
    for paper in papers:
        render(env, "paper.html.jinja2",
               out / "papers" / f"{paper['slug']}.html",
               paper=paper, **ctx)

    print("Generating category listing pages...")
    render(env, "listing.html.jinja2", out / "principles" / "index.html",
           category_type="principle", category_label="Principle",
           items=ctx["principles"], paper_index=index["by_principle"], **ctx)
    render(env, "listing.html.jinja2", out / "domains" / "index.html",
           category_type="domain", category_label="Domain",
           items=ctx["domains"], paper_index=index["by_domain"], **ctx)
    render(env, "listing.html.jinja2", out / "topics" / "index.html",
           category_type="topic", category_label="Technique",
           items=ctx["topics"], paper_index=index["by_topic"], **ctx)

    print("Generating search page...")
    search_index = build_search_index(papers, principles, domains, topics, venues)
    render(env, "search.html.jinja2", out / "search.html",
           search_index=search_index, **ctx)

    print("Generating index...")
    render(env, "index.html.jinja2", out / "index.html",
           search_index=search_index, **ctx)

    # Copy static assets if present
    static_src = ROOT / "static"
    if static_src.exists():
        shutil.copytree(static_src, out / "static", dirs_exist_ok=True)

    total = len(papers)
    indexed = len([p for p in papers if p.get("reading_status") in ("read", "understood")])
    print(f"\nDone. {indexed}/{total} papers indexed, {total} pages generated.")
    print(f"Site at: {out}/index.html")


if __name__ == "__main__":
    main()
