#!/usr/bin/env python3
"""Generate a new paper template from a MLSys URL."""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
PAPERS = ROOT / "data" / "papers"

TEMPLATE = '''\
---
# Identity
title: "{title}"
slug: "{slug}"
authors: []
organizations: []

# Links
venue_url: "{venue_url}"
openreview_url: ""  # https://openreview.net/forum?id=XXXXX
arxiv_url: ""        # preprint, if posted separately
slides_url: ""
code_url: ""
project_url: ""

# Venue metadata
official_category: ""
presentation_type: oral  # oral | poster | spotlight
award: ""
arxiv_date: ""  # auto-derived from arXiv ID (YYYY-MM)

# User taxonomy
domain: []  # see data/domains.yaml for valid slugs
topics: []  # see data/topics.yaml for valid slugs
principles: []  # see data/principles.yaml for valid slugs
observations: {}  # slug: "one sentence — what the authors specifically observed in this paper"

# Evaluation
hardware: []
models_evaluated: []
agentic_models: []

# Impact
citations: null
citations_updated: ""
research_or_industry: ""  # research | industry | mixed

# Quick-scan fields
problem: ""
key_results: ""

# Reading/indexing
# Publishing
status: draft  # draft | published — only published papers appear on the site by default

# Reading/indexing
reading_status: want-to-read  # want-to-read | reading | read | understood
indexed_by: "{indexed_by}"
indexed_date: "{indexed_date}"
---

## Problem

<!-- 2–3 sentences expanding on the `problem` frontmatter field. Why does this matter
     at scale? What breaks or costs too much today? -->

## Key Contributions

<!-- 3–5 bullets. Each should be a concrete artifact (named algorithm, data structure,
     protocol, measurement) with a brief mechanism. Not "we show X is possible." -->

- TODO

## Results

<!-- Key numbers: metric + value + hardware + model + baseline. If hardware or baselines
     are not specified in the paper, say so. -->

- TODO

## Trade-offs

<!-- What does the approach give up to achieve its gains?
     E.g. "higher throughput at the cost of 2–3% accuracy degradation"
          "reduces memory but increases kernel launch overhead at small batch sizes"
     Leave empty if nothing notable. -->

## Nuances

<!-- Implementation gotchas, subtle assumptions, conditions that break the approach,
     and limitations — things a practitioner would only discover by reading carefully.
     E.g. "requires contiguous KV blocks — incompatible with PagedAttention out of the box"
     Leave empty if nothing notable. -->
'''


def slugify(title):
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")[:60]


def main():
    parser = argparse.ArgumentParser(description="Create a new paper template")
    parser.add_argument("--url", required=True, help="MLSys virtual URL for the paper")
    parser.add_argument("--title", required=True, help="Paper title")
    parser.add_argument("--slug", help="URL slug (default: derived from title)")
    parser.add_argument("--by", default="", help="Your GitHub username")
    args = parser.parse_args()

    slug = args.slug or slugify(args.title)
    dest = PAPERS / f"{slug}.md"

    if dest.exists():
        print(f"Error: {dest} already exists. Edit it directly or choose a different slug.")
        sys.exit(1)

    content = TEMPLATE.format(
        title=args.title,
        slug=slug,
        venue_url=args.url,
        indexed_by=args.by,
        indexed_date=date.today().isoformat(),
    )

    dest.write_text(content)
    print(f"Created: {dest}")
    print(f"Next: fill in the frontmatter and body, then run: python scripts/validate.py")


if __name__ == "__main__":
    main()
