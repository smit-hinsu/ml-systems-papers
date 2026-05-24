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
mlsys_url: "{mlsys_url}"
openreview_url: ""  # https://openreview.net/forum?id=XXXXX
arxiv_url: ""        # preprint, if posted separately
slides_url: ""
code_url: ""
project_url: ""

# MLSys metadata
mlsys_official_category: ""
presentation_type: oral  # oral | poster | spotlight
award: ""
date: ""

# User taxonomy
domain: []  # see data/domains.yaml for valid slugs
techniques: []  # see data/techniques.yaml for valid slugs
insights: []  # see data/insights.yaml for valid slugs

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
reading_status: want-to-read  # want-to-read | reading | read | understood
indexed_by: "{indexed_by}"
indexed_date: "{indexed_date}"
---

## Summary

TODO

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
        mlsys_url=args.url,
        indexed_by=args.by,
        indexed_date=date.today().isoformat(),
    )

    dest.write_text(content)
    print(f"Created: {dest}")
    print(f"Next: fill in the frontmatter and body, then run: python scripts/validate.py")


if __name__ == "__main__":
    main()
