#!/usr/bin/env python3
"""Validate paper files against schema, registries, and character limits.

Severity model:
  error   — blocks publishing; applies only to papers with status: published
  warning — advisory; applies to all papers (draft + published)
Exit code 1 only when at least one error exists.
"""

import sys
from pathlib import Path

import frontmatter
import yaml

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"

# Fields required before a paper may be published.
REQUIRED_FOR_PUBLISH = [
    "title", "slug", "venue_url", "presentation_type", "domain",
    "research_or_industry", "problem", "key_results", "reading_status", "indexed_by",
]
VALID_STATUSES = {"want-to-read", "reading", "read", "understood"}
VALID_TYPES = {"oral", "poster", "spotlight"}
VALID_R_OR_I = {"research", "industry", "mixed"}

# Character limits for UI-visible fields.
# Sentence fields are shown in cards and paper-page headers — keep them tight.
CHAR_LIMITS = {
    "problem":               160,   # one sentence, index card + paper header
    "key_results":           160,   # one sentence with numbers, result box
    "observations_value":    200,   # one sentence, index card + paper header
    "award":                  80,
    "official_category":      60,
    "authors_item":           80,
    "organizations_item":     80,
    "hardware_item":          40,
    "models_evaluated_item":  60,
    "agentic_models_item":    60,
}


def load_registry(name):
    with open(DATA / name) as f:
        return set(yaml.safe_load(f).keys())


def load_venues():
    with open(DATA / "venues.yaml") as f:
        return set(yaml.safe_load(f).keys())


def record(bucket, msg):
    bucket.append(msg)


def check_len(value, limit, label, name, is_published, errors, warnings):
    """Append an error (published) or warning (draft) if value exceeds limit."""
    if not isinstance(value, str) or not value:
        return
    if len(value) > limit:
        msg = (f"{name}: {label} is {len(value)} chars (limit {limit}): "
               f"{value[:60]!r}…")
        record(errors if is_published else warnings, msg)


def main():
    principles = load_registry("principles.yaml")
    domains = load_registry("domains.yaml")
    topics = load_registry("topics.yaml")
    venues = load_venues()

    errors = []
    warnings = []
    paper_slugs = set()

    for path in sorted((DATA / "papers").glob("*.md")):
        post = frontmatter.load(path)
        p = dict(post.metadata)
        name = path.name
        is_published = p.get("status") == "published"
        bucket = errors if is_published else warnings

        # Slug uniqueness (always an error regardless of status)
        slug = p.get("slug", path.stem)
        if slug in paper_slugs:
            errors.append(f"{name}: duplicate slug '{slug}'")
        paper_slugs.add(slug)
        if slug != path.stem:
            warnings.append(f"{name}: slug '{slug}' doesn't match filename '{path.stem}'")

        # Enum validation (always an error if the field is set to a bad value)
        if p.get("reading_status") and p["reading_status"] not in VALID_STATUSES:
            errors.append(f"{name}: invalid reading_status '{p['reading_status']}'")
        if p.get("presentation_type") and p["presentation_type"] not in VALID_TYPES:
            errors.append(f"{name}: invalid presentation_type '{p['presentation_type']}'")
        if p.get("research_or_industry") and p["research_or_industry"] not in VALID_R_OR_I:
            errors.append(f"{name}: invalid research_or_industry '{p['research_or_industry']}'")

        # Required fields — error for published, warning for draft
        for field in REQUIRED_FOR_PUBLISH:
            if not p.get(field):
                record(bucket, f"{name}: missing required field '{field}'")

        # Registry cross-references — error for published, warning for draft
        for s in p.get("principles") or []:
            if s not in principles:
                record(bucket, f"{name}: unknown principle slug '{s}'")
        for s in p.get("domain") or []:
            if s not in domains:
                record(bucket, f"{name}: unknown domain slug '{s}'")
        for s in p.get("topics") or []:
            if s not in topics:
                record(bucket, f"{name}: unknown topic slug '{s}'")
        if p.get("venue") and p["venue"] not in venues:
            record(bucket, f"{name}: unknown venue slug '{p['venue']}'")

        # Character limits — error for published, warning for draft
        check_len(p.get("problem") or "", CHAR_LIMITS["problem"],
                  "problem", name, is_published, errors, warnings)
        check_len(p.get("key_results") or "", CHAR_LIMITS["key_results"],
                  "key_results", name, is_published, errors, warnings)
        check_len(p.get("award") or "", CHAR_LIMITS["award"],
                  "award", name, is_published, errors, warnings)
        check_len(p.get("official_category") or "", CHAR_LIMITS["official_category"],
                  "official_category", name, is_published, errors, warnings)

        for obs_slug, obs_text in (p.get("observations") or {}).items():
            check_len(obs_text or "", CHAR_LIMITS["observations_value"],
                      f"observations[{obs_slug}]", name, is_published, errors, warnings)

        for item in p.get("authors") or []:
            check_len(item, CHAR_LIMITS["authors_item"],
                      "authors item", name, is_published, errors, warnings)
        for item in p.get("organizations") or []:
            check_len(item, CHAR_LIMITS["organizations_item"],
                      "organizations item", name, is_published, errors, warnings)
        for item in p.get("hardware") or []:
            check_len(item, CHAR_LIMITS["hardware_item"],
                      "hardware item", name, is_published, errors, warnings)
        for item in p.get("models_evaluated") or []:
            check_len(item, CHAR_LIMITS["models_evaluated_item"],
                      "models_evaluated item", name, is_published, errors, warnings)
        for item in p.get("agentic_models") or []:
            check_len(item, CHAR_LIMITS["agentic_models_item"],
                      "agentic_models item", name, is_published, errors, warnings)

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")

    if errors:
        print(f"\nERRORS ({len(errors)}) — fix before publishing:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        pub = sum(1 for p in paper_slugs if True)  # placeholder
        print(f"\nAll {len(paper_slugs)} papers valid ({len(warnings)} warnings on drafts).")


if __name__ == "__main__":
    main()
