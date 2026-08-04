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


class _Desc(str):
    """String wrapper that reverses comparison, for descending alpha tiebreaks."""
    def __lt__(self, other): return str.__gt__(self, other)
    def __gt__(self, other): return str.__lt__(self, other)
    def __le__(self, other): return str.__ge__(self, other)
    def __ge__(self, other): return str.__le__(self, other)


def sort_papers(papers):
    # `status` is deliberately NOT a sort key. It tracks human review progress and is
    # hidden from the production build, so ordering by it would rank papers by something
    # the reader cannot see — which put the one reviewed paper on top regardless of merit.
    #
    # TODO: revisit this ordering when the index includes non-MLSys venues —
    # award tiers and presentation types aren't standardized across conferences.
    def key(p):
        award_rank = 0 if p.get("award") else 1
        ptype_rank = _PRESENTATION_RANK.get(p.get("presentation_type") or "", 99)
        citations = -(p.get("citations") or 0)
        date = _Desc(p.get("arxiv_date") or "")
        return (award_rank, ptype_rank, citations, date, _Desc(p.get("title") or ""))

    return sorted(papers, key=key)


def build_index(papers, principles, domains, topics, venues):
    """Build cross-reference maps."""
    by_principle = defaultdict(list)
    by_domain = defaultdict(list)
    by_topic = defaultdict(list)
    by_opttype = defaultdict(list)
    by_status = defaultdict(list)

    for paper in papers:
        for slug in paper.get("principles") or []:
            by_principle[slug].append(paper)
        for slug in paper.get("domain") or []:
            by_domain[slug].append(paper)
        for slug in paper.get("topics") or []:
            by_topic[slug].append(paper)
        for slug in paper.get("optimization_type") or []:
            by_opttype[slug].append(paper)
        status = paper.get("reading_status") or "unread"
        by_status[status].append(paper)

    return {
        "by_principle": dict(by_principle),
        "by_domain": dict(by_domain),
        "by_topic": dict(by_topic),
        "by_opttype": dict(by_opttype),
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


def build_facets(domains, topics, index):
    """Facets shown on the Browse page: domains and techniques."""
    def facet(label, hint, param, chip, registry, paper_index):
        options = []
        for slug, item in registry.items():
            item = item or {}
            options.append({
                "value": slug,
                "label": item.get("label") or slug,
                "count": len(paper_index.get(slug, [])),
                "description": item.get("description") or "",
                "category": item.get("category") or "",
            })
        options.sort(key=lambda v: (-v["count"], v["label"]))
        return {"label": label, "hint": hint, "param": param, "chip": chip, "options": options}

    return [
        facet("Domains", "Which part of the ML stack the paper targets.",
              "domain", "domain", domains, index["by_domain"]),
        facet("Techniques", "Concrete methods and mechanisms the paper uses.",
              "topic", "topic", topics, index["by_topic"]),
    ]


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
    optimization_types = load_registry("optimization_types.yaml")
    # Every paper is rendered, in both prod and dev. `status` is the internal review
    # tracker, not a visibility switch — it must not appear anywhere in the prod output.
    papers = load_papers()
    if not args.dev:
        unreviewed = len([p for p in papers if p.get("status") != "published"])
        if unreviewed:
            print(f"Publishing all {len(papers)} papers ({unreviewed} not yet human-reviewed; "
                  f"review badges are hidden — use --dev to show them).")
    # Draft principles are still being worked out; they stay in the data (papers keep
    # their tags and observations) but are stripped from the prod build so they render
    # only under --dev. Stripping here, before the index and search index are built,
    # keeps them out of every downstream surface: cards, chips, filter pages, search.
    # `principles_review` is never published. Under --dev it is folded into the visible
    # tags so a reviewer can see what the audit set aside; in prod it does not exist.
    if args.dev:
        for paper in papers:
            extra = [s for s in (paper.get("principles_review") or [])
                     if s not in (paper.get("principles") or [])]
            if extra:
                paper["principles"] = (paper.get("principles") or []) + extra

    draft_principles = {s for s, p in principles.items() if (p or {}).get("status") == "draft"}
    if draft_principles and not args.dev:
        principles = {s: p for s, p in principles.items() if s not in draft_principles}
        for paper in papers:
            if paper.get("principles"):
                paper["principles"] = [s for s in paper["principles"] if s not in draft_principles]
            if paper.get("observations"):
                paper["observations"] = {k: v for k, v in paper["observations"].items()
                                         if k not in draft_principles}
        print(f"Hiding draft principle(s) from prod build: {', '.join(sorted(draft_principles))}")

    index = build_index(papers, principles, domains, topics, venues)

    def sorted_by_count(registry, paper_index):
        # Registry entries nothing is tagged with are dropped rather than shown as
        # empty categories — an unused slug is taxonomy bookkeeping, not something a
        # reader can browse into.
        used = {slug: item for slug, item in registry.items() if paper_index.get(slug)}
        return dict(sorted(used.items(),
                           key=lambda kv: len(paper_index.get(kv[0], [])),
                           reverse=True))

    ctx = dict(
        site=site,
        venues=venues,
        principles=sorted_by_count(principles, index["by_principle"]),
        domains=sorted_by_count(domains, index["by_domain"]),
        topics=sorted_by_count(topics, index["by_topic"]),
        optimization_types=optimization_types,
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

    render(env, "browse.html.jinja2", out / "browse" / "index.html",
           facets=build_facets(ctx["domains"], ctx["topics"], index), **ctx)

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
