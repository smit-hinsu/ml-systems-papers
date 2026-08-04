#!/usr/bin/env python3
"""Validate paper files against schema, registries, and character limits.

Severity model:
  error   — blocks publishing; applies only to papers with status: published
  warning — advisory; applies to all papers (draft + published)
Exit code 1 only when at least one error exists.
"""

import re
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


VAGUE_RESULTS_WORDS = [
    "significant", "outperforms baselines", "various", "several", "state-of-the-art",
]

FORBIDDEN_PROBLEM_PREFIXES = [
    "Large language models",
    "Recent advances",
    "Modern",
    "Existing approaches",
    "The proliferation",
]

# Stopwords for Jaccard similarity (observation vs principle description)
STOPWORDS = {
    "a", "an", "the", "is", "are", "can", "be", "to", "of", "in", "it", "that",
    "which", "by", "for", "with", "this", "these", "their", "when", "as", "and",
    "or", "not", "on", "at", "from", "has",
}

MoE_SERVING_DOMAINS = {"recs-models", "llm-serving", "llm-training", "rl-training"}


def load_registry(name):
    with open(DATA / name) as f:
        return set(yaml.safe_load(f).keys())


def load_registry_full(name):
    with open(DATA / name) as f:
        return yaml.safe_load(f)


def load_venues():
    with open(DATA / "venues.yaml") as f:
        return set(yaml.safe_load(f).keys())


def tokenize(text):
    """Lowercase, strip punctuation, remove stopwords."""
    words = re.findall(r"[a-z]+", text.lower())
    return {w for w in words if w not in STOPWORDS}


def jaccard(set_a, set_b):
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


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
    principles_full = load_registry_full("principles.yaml")
    domains = load_registry("domains.yaml")
    topics = load_registry("topics.yaml")
    optimization_types = load_registry("optimization_types.yaml")
    venues = load_venues()

    errors = []
    warnings = []
    paper_slugs = set()

    # Cross-paper data: {principle_slug: [(paper_name, obs_text), ...]}
    principle_obs_map: dict = {}

    for path in sorted((DATA / "papers").glob("*.md")):
        post = frontmatter.load(path)
        p = dict(post.metadata)
        body = post.content
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
        for s in p.get("optimization_type") or []:
            if s not in optimization_types:
                record(bucket, f"{name}: unknown optimization_type slug '{s}'")
        if p.get("venue") and p["venue"] not in venues:
            record(bucket, f"{name}: unknown venue slug '{p['venue']}'")

        # `observations` is keyed by principle slug. Nothing checked these keys, so a
        # topic slug (kv-cache) sat in one paper's observations dict undetected, and
        # observations for principles the paper no longer carries would render nowhere.
        # `principles_review` holds tags the audit judged arguable rather than clearly wrong.
        # They are kept in the data so a human can settle them, but the site never renders
        # them. Their observations stay in the same `observations` dict.
        for s in p.get("principles_review") or []:
            if s not in principles:
                record(bucket, f"{name}: unknown principle slug '{s}' in principles_review")
        both = set(p.get("principles") or []) & set(p.get("principles_review") or [])
        for s in sorted(both):
            record(bucket, f"{name}: '{s}' is in both principles and principles_review")

        obs_keys = set((p.get("observations") or {}))
        tagged = set(p.get("principles") or []) | set(p.get("principles_review") or [])
        for s in sorted(obs_keys):
            if s not in principles:
                record(bucket, f"{name}: observations key '{s}' is not a principle slug")
        for s in sorted(obs_keys - tagged):
            if s in principles:
                record(bucket, f"{name}: observations['{s}'] has no matching entry in principles")

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

        # ── Body structure checks ─────────────────────────────────────────────
        if re.search(r'^##\s+Problem\s*$', body, re.MULTILINE):
            warnings.append(f"{name}: body contains '## Problem' heading (old format)")
        if re.search(r'^##\s+Results\s*$', body, re.MULTILINE):
            warnings.append(f"{name}: body contains '## Results' heading (old format)")
        if "<!-- DRAFT" in body:
            warnings.append(f"{name}: body contains '<!-- DRAFT' scaffold placeholder")
        # Unfilled angle-bracket placeholders (e.g. "<2–3 sentences", "<named algorithm")
        # Exclude legitimate numeric comparisons like <1%, <7µs
        if re.search(r'<[a-zA-Z][^>]{2,}>', body):
            warnings.append(f"{name}: body may contain unfilled placeholder (< ... >)")
        # Key Contributions section required
        has_key_contributions = bool(re.search(r'^##\s+Key Contributions', body, re.MULTILINE))
        if not has_key_contributions:
            record(bucket, f"{name}: body is missing '## Key Contributions' section")

        # ── Content heuristics ────────────────────────────────────────────────
        key_results = p.get("key_results") or ""
        for vague in VAGUE_RESULTS_WORDS:
            if vague.lower() in key_results.lower():
                warnings.append(
                    f"{name}: key_results contains vague language: {vague!r}"
                )
        if key_results and not re.search(r'\d', key_results):
            warnings.append(f"{name}: key_results has no digit (missing concrete numbers)")

        problem = p.get("problem") or ""
        for prefix in FORBIDDEN_PROBLEM_PREFIXES:
            if problem.startswith(prefix):
                warnings.append(
                    f"{name}: problem starts with forbidden prefix: {prefix!r}"
                )

        # Observation vs. principle description similarity
        for obs_slug, obs_text in (p.get("observations") or {}).items():
            if not obs_text or obs_slug not in principles_full:
                continue
            principle_desc = principles_full[obs_slug].get("description") or ""
            obs_tokens = tokenize(str(obs_text))
            desc_tokens = tokenize(str(principle_desc))
            sim = jaccard(obs_tokens, desc_tokens)
            if sim > 0.5:
                warnings.append(
                    f"{name}: observations[{obs_slug}] may be restating the principle "
                    f"(word overlap {sim:.0%})"
                )

        # Accumulate observations for cross-paper checks
        for obs_slug, obs_text in (p.get("observations") or {}).items():
            if obs_slug not in principle_obs_map:
                principle_obs_map[obs_slug] = []
            principle_obs_map[obs_slug].append((name, str(obs_text or "").strip()))

        # ── Cross-paper consistency ────────────────────────────────────────────
        paper_topics = set(p.get("topics") or [])
        paper_domains = set(p.get("domain") or [])

        if "moe" in paper_topics and not paper_domains & MoE_SERVING_DOMAINS:
            warnings.append(
                f"{name}: has topic 'moe' but no serving/training domain "
                f"({', '.join(sorted(MoE_SERVING_DOMAINS))})"
            )

        # Removed: a "topic kernel-fusion implies principle fuse" check.
        #
        # It encoded the conflation that produced the 2026-08 audit's worst results.
        # `topics` records methods a paper *uses*; `principles` record what it
        # *contributes*. BLASST runs inside FlashAttention's fused softmax loop and
        # contributes no fusion; Spira eliminates a pre-processing pass. Both keep an
        # accurate `kernel-fusion` topic and correctly carry no `fuse` principle.
        # Warning on that pushes a reviewer toward re-adding the tag the audit removed,
        # or toward deleting true metadata to silence it — 78% of `fuse` tags were wrong.

    # Cross-paper: duplicate observation text for same principle
    for obs_slug, entries in principle_obs_map.items():
        # Group by text
        text_to_papers: dict = {}
        for paper_name, text in entries:
            if not text:
                continue
            if text not in text_to_papers:
                text_to_papers[text] = []
            text_to_papers[text].append(paper_name)
        for text, papers_with_text in text_to_papers.items():
            if len(papers_with_text) > 1:
                warnings.append(
                    f"Cross-paper: identical observations[{obs_slug}] text in "
                    f"{', '.join(papers_with_text)} — possible copy-paste"
                )

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
