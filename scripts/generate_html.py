#!/usr/bin/env python3
"""Generate static HTML site from data files."""

import argparse
import re
import shutil
from collections import defaultdict
from pathlib import Path

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


def build_index(papers, insights, domains, techniques, venues):
    """Build cross-reference maps."""
    by_insight = defaultdict(list)
    by_domain = defaultdict(list)
    by_technique = defaultdict(list)
    by_status = defaultdict(list)

    for paper in papers:
        for slug in paper.get("insights") or []:
            by_insight[slug].append(paper)
        for slug in paper.get("domain") or []:
            by_domain[slug].append(paper)
        for slug in paper.get("techniques") or []:
            by_technique[slug].append(paper)
        status = paper.get("reading_status") or "unread"
        by_status[status].append(paper)

    return {
        "by_insight": dict(by_insight),
        "by_domain": dict(by_domain),
        "by_technique": dict(by_technique),
        "by_status": dict(by_status),
    }


def build_search_index(papers, insights, domains, techniques, venues):
    """Build the search index embedded in search.html."""
    records = []
    for p in papers:
        v = venues.get(p.get("venue") or "", {})
        records.append({
            "slug": p["slug"],
            "url": f"papers/{p['slug']}.html",
            "root": "",  # search.html is at site root
            "title": p.get("title") or "",
            "authors": p.get("authors") or [],
            "organizations": p.get("organizations") or [],
            "problem": p.get("problem") or "",
            "key_results": p.get("key_results") or "",
            "domain_labels": [domains[d]["label"] for d in (p.get("domain") or []) if d in domains],
            "technique_labels": [techniques[t]["label"] for t in (p.get("techniques") or []) if t in techniques],
            "insight_slugs": [i for i in (p.get("insights") or []) if i in insights],
            "insight_labels": [insights[i]["label"] for i in (p.get("insights") or []) if i in insights],
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
    # Allow tojson in templates (for search index)
    env.policies["json.dumps_kwargs"] = {"ensure_ascii": False}

    # Load data
    site = load_registry("site.yaml")
    venues = load_registry("venues.yaml")
    insights = load_registry("insights.yaml")
    domains = load_registry("domains.yaml")
    techniques = load_registry("techniques.yaml")
    papers = load_papers()
    index = build_index(papers, insights, domains, techniques, venues)

    ctx = dict(
        site=site,
        venues=venues,
        insights=insights,
        domains=domains,
        techniques=techniques,
        all_papers=papers,
        index=index,
    )

    print("Generating paper pages...")
    for paper in papers:
        render(env, "paper.html.jinja2",
               out / "papers" / f"{paper['slug']}.html",
               paper=paper, **ctx)

    print("Generating insight pages...")
    for slug, insight in insights.items():
        render(env, "tag.html.jinja2",
               out / "insights" / f"{slug}.html",
               tag_type="insight", tag_slug=slug, tag=insight,
               tag_papers=index["by_insight"].get(slug, []), **ctx)

    print("Generating domain pages...")
    for slug, domain in domains.items():
        render(env, "tag.html.jinja2",
               out / "domains" / f"{slug}.html",
               tag_type="domain", tag_slug=slug, tag=domain,
               tag_papers=index["by_domain"].get(slug, []), **ctx)

    print("Generating technique pages...")
    for slug, technique in techniques.items():
        render(env, "tag.html.jinja2",
               out / "techniques" / f"{slug}.html",
               tag_type="technique", tag_slug=slug, tag=technique,
               tag_papers=index["by_technique"].get(slug, []), **ctx)

    print("Generating category listing pages...")
    render(env, "listing.html.jinja2", out / "insights" / "index.html",
           category_type="insight", category_label="Insight",
           items=insights, paper_index=index["by_insight"], **ctx)
    render(env, "listing.html.jinja2", out / "domains" / "index.html",
           category_type="domain", category_label="Domain",
           items=domains, paper_index=index["by_domain"], **ctx)
    render(env, "listing.html.jinja2", out / "techniques" / "index.html",
           category_type="technique", category_label="Technique",
           items=techniques, paper_index=index["by_technique"], **ctx)

    print("Generating search page...")
    search_index = build_search_index(papers, insights, domains, techniques, venues)
    render(env, "search.html.jinja2", out / "search.html",
           search_index=search_index, **ctx)

    print("Generating index...")
    render(env, "index.html.jinja2", out / "index.html", **ctx)

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
