#!/usr/bin/env python3
"""Validate paper files against schema and registries."""

import sys
from pathlib import Path

import frontmatter
import yaml

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"

REQUIRED_FIELDS = ["title", "slug", "mlsys_url", "presentation_type", "domain",
                   "research_or_industry", "problem", "reading_status", "indexed_by"]
VALID_STATUSES = {"want-to-read", "reading", "read", "understood"}
VALID_TYPES = {"oral", "poster", "spotlight"}
VALID_R_OR_I = {"research", "industry", "mixed"}


def load_registry(name):
    with open(DATA / name) as f:
        return set(yaml.safe_load(f).keys())


def load_venues():
    with open(DATA / "venues.yaml") as f:
        return set(yaml.safe_load(f).keys())


def main():
    insights = load_registry("insights.yaml")
    domains = load_registry("domains.yaml")
    techniques = load_registry("techniques.yaml")
    venues = load_venues()

    errors = []
    warnings = []
    paper_slugs = set()

    for path in sorted((DATA / "papers").glob("*.md")):
        post = frontmatter.load(path)
        p = dict(post.metadata)
        name = path.name

        # Required fields
        for field in REQUIRED_FIELDS:
            if not p.get(field):
                errors.append(f"{name}: missing required field '{field}'")

        # Slug uniqueness
        slug = p.get("slug", path.stem)
        if slug in paper_slugs:
            errors.append(f"{name}: duplicate slug '{slug}'")
        paper_slugs.add(slug)

        # Slug matches filename
        if slug != path.stem:
            warnings.append(f"{name}: slug '{slug}' doesn't match filename '{path.stem}'")

        # Enum validation
        if p.get("reading_status") and p["reading_status"] not in VALID_STATUSES:
            errors.append(f"{name}: invalid reading_status '{p['reading_status']}'")
        if p.get("presentation_type") and p["presentation_type"] not in VALID_TYPES:
            errors.append(f"{name}: invalid presentation_type '{p['presentation_type']}'")
        if p.get("research_or_industry") and p["research_or_industry"] not in VALID_R_OR_I:
            errors.append(f"{name}: invalid research_or_industry '{p['research_or_industry']}'")

        # Registry cross-references
        for slug in p.get("insights") or []:
            if slug not in insights:
                errors.append(f"{name}: unknown insight slug '{slug}'")
        for slug in p.get("domain") or []:
            if slug not in domains:
                errors.append(f"{name}: unknown domain slug '{slug}'")
        for slug in p.get("techniques") or []:
            if slug not in techniques:
                errors.append(f"{name}: unknown technique slug '{slug}'")
        if p.get("venue") and p["venue"] not in venues:
            errors.append(f"{name}: unknown venue slug '{p['venue']}'")

        # Warn on empty optional fields
        for field in ["organizations", "openreview_url", "key_results"]:
            if not p.get(field):
                warnings.append(f"{name}: empty field '{field}' (fill in when known)")

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  {w}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print(f"\nAll {len(paper_slugs)} papers valid.")


if __name__ == "__main__":
    main()
