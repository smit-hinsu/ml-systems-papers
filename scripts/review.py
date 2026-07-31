#!/usr/bin/env python3
"""Per-paper review brief: data gaps, validation, heuristic + LLM quality checks.

Usage:
  python scripts/review.py <slug>
  python scripts/review.py flashagents
  python scripts/review.py --no-llm flashagents   # skip LLM call
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import frontmatter  # type: ignore
import yaml  # type: ignore

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"

# ── helpers ────────────────────────────────────────────────────────────────────

def load_yaml(name: str) -> dict:
    with open(DATA / name) as f:
        return yaml.safe_load(f)


def tick(ok: bool) -> str:
    return "✓" if ok else "✗"


def hr(label: str = "", width: int = 62) -> str:
    if label:
        return f"── {label} " + "─" * max(0, width - len(label) - 4)
    return "─" * width


# ── data gap check ─────────────────────────────────────────────────────────────

def data_gaps(p: dict) -> list[tuple[bool, str, str]]:
    """Return list of (ok, field, note) tuples for the pre-review data check."""
    rows = []
    # Links
    rows.append((bool(p.get("arxiv_url")), "arxiv_url",
                 p.get("arxiv_url") or "missing"))
    rows.append((bool(p.get("openreview_url")), "openreview_url",
                 p.get("openreview_url") or "missing"))
    rows.append((bool(p.get("code_url")), "code_url",
                 p.get("code_url") or "missing — check OpenReview / arXiv abstract"))
    rows.append((bool(p.get("slides_url")), "slides_url",
                 p.get("slides_url") or "missing"))
    # Organizations
    orgs = p.get("organizations") or []
    rows.append((bool(orgs), "organizations",
                 ", ".join(orgs) if orgs else "empty — fill from OpenReview affiliations"))
    # Optimization type (new field — expected empty on drafts, but flag if status > draft)
    ot = p.get("optimization_type") or []
    status = p.get("status") or "draft"
    if status in ("under-review", "published"):
        rows.append((bool(ot), "optimization_type",
                     ", ".join(ot) if ot else "NOT TAGGED — required before publishing"))
    else:
        rows.append((bool(ot), "optimization_type",
                     ", ".join(ot) if ot else "not tagged yet (fill during review)"))
    return rows


# ── validation ─────────────────────────────────────────────────────────────────

def run_validate(slug: str) -> list[str]:
    """Run validate.py and return lines that mention this slug."""
    result = subprocess.run(
        [sys.executable, "scripts/validate.py"],
        cwd=ROOT, capture_output=True, text=True,
    )
    output = result.stdout + result.stderr
    slug_stem = slug.replace("-", "").replace("_", "")  # fuzzy match
    lines = []
    for line in output.splitlines():
        # Match by slug in filename (filenames are slug + .md)
        if slug in line or slug_stem in line.lower():
            lines.append(line.strip())
    return lines


# ── heuristic checks ──────────────────────────────────────────────────────────

HARDWARE_TOKENS = {
    "h100", "a100", "tpu", "b200", "gpu", "groqchip", "h200", "mi300x",
    "v100", "a10", "a30", "l4", "l40", "t4", "a6000", "rtx", "nvlink",
}
MODEL_TOKENS = {
    "llama", "qwen", "mixtral", "gpt", "gemma", "mistral", "deepseek",
    "falcon", "yi", "phi", "bloom", "opt", "bert", "t5", "palm", "claude",
}
FORBIDDEN_PROBLEM_PREFIXES = [
    "Large language models", "Recent advances", "Modern", "Existing approaches",
    "The proliferation", "LLMs are", "Training frontier", "Efficient inference",
    "Large language model",
]


def heuristic_checks(p: dict, body: str) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    key_results = p.get("key_results") or ""
    problem = p.get("problem") or ""

    if key_results and not re.search(r'[\d×]', key_results):
        findings.append(("FAIL", "key_results has no number"))
    if key_results:
        kr_lower = key_results.lower()
        if not any(hw in kr_lower for hw in HARDWARE_TOKENS) and \
           not any(m in kr_lower for m in MODEL_TOKENS):
            findings.append(("WARN", "key_results names neither hardware nor a model"))
    if not problem:
        findings.append(("FAIL", "problem field is empty"))
    elif len(problem) > 160:
        findings.append(("FAIL", f"problem is {len(problem)} chars (limit 160)"))
    for prefix in FORBIDDEN_PROBLEM_PREFIXES:
        if problem.startswith(prefix):
            findings.append(("WARN", f"problem starts with forbidden prefix: {prefix!r}"))
            break

    kc_match = re.search(r'^##\s+Key Contributions\s*\n(.*?)(?=^##|\Z)',
                         body, re.MULTILINE | re.DOTALL)
    if kc_match:
        bullets = [l for l in kc_match.group(1).splitlines()
                   if l.strip().startswith("- ")]
        vague = [b for b in bullets if not re.search(r'\*\*[^*]+\*\*', b)]
        if vague:
            findings.append(("WARN",
                f"{len(vague)} Key Contributions bullet(s) missing bold **Artifact**: name"))
    else:
        findings.append(("FAIL", "## Key Contributions section missing"))

    return findings


# ── LLM check ─────────────────────────────────────────────────────────────────

LLM_PROMPT = """\
You are reviewing a paper entry in an ML systems paper index before it is published.
Audience: senior ML systems engineers deciding whether to read a paper.

Evaluate on these 6 dimensions:

1. PROBLEM VOICE: Does `problem` read like a practitioner describing a real cost or
   breakage at scale (specific, concrete) or like an academic abstract (vague, generic)?

2. KEY CONTRIBUTIONS: Do the bullets each name a specific artifact (algorithm/protocol/
   data structure) with a concrete mechanism? They should assume the reader already knows
   the principle and the motivating problem — skip re-explaining those. Flag any bullet
   that could be replaced by just reading the principle label + observation.

3. OBSERVATIONS: Each observation should capture the *motivating problem insight* that
   makes the principle applicable — i.e., what the paper noticed about the problem
   situation, NOT the solution. Bad example: "we overlap prefill and decode" (describes
   the solution). Good example: "downstream agents idle waiting for upstream output despite
   having spare GPU capacity" (describes the problem). Flag any observation framed as a
   solution description or that restates the principle.

4. MISSING NUANCES: What obvious limitations or gotchas are likely present but missing
   from `## Nuances`? (One sentence only; skip if nuances look complete.)

5. OPTIMIZATION TYPE: Based on the paper content, which of these apply? Pick all that fit:
   - algorithm  — new mathematical method, formula, or computation strategy
   - system     — engineering change: batching, scheduling, memory, disaggregation
   - hardware   — hardware design, ISA, or deep hardware-software co-design
   - workflow   — training recipe, eval methodology, or operational process change
   - application — domain-specific trick exploiting application-layer properties
   Current value: {optimization_type}

6. TAXONOMY: Do domain and topic tags look correct? Flag anything obviously wrong or missing.
   Current domain: {domain}
   Current topics: {topics}

For each dimension: ONE sentence if there is a real issue, or "OK" if fine.
Be concise. Do not repeat content back to me.

--- PAPER ---
slug: {slug}
status: {status}
research_or_industry: {research_or_industry}
problem: {problem}
key_results: {key_results}
principles: {principles}
observations:
{observations}

{body}
--- END ---

Respond in exactly this format:
PROBLEM VOICE: <one sentence or OK>
KEY CONTRIBUTIONS: <one sentence or OK>
OBSERVATIONS: <one sentence or OK>
MISSING NUANCES: <one sentence or OK>
OPTIMIZATION TYPE: <comma-separated slugs from the 5 options above, e.g. "algorithm, system">
TAXONOMY: <one sentence or OK>
"""


def llm_check(p: dict, body: str) -> str:
    try:
        import anthropic  # type: ignore
    except ImportError:
        return "ERROR: 'anthropic' package not installed"

    prompt = LLM_PROMPT.format(
        slug=p.get("slug") or "",
        status=p.get("status") or "draft",
        research_or_industry=p.get("research_or_industry") or "",
        domain=", ".join(p.get("domain") or []),
        topics=", ".join(p.get("topics") or []),
        principles=", ".join(p.get("principles") or []),
        optimization_type=", ".join(p.get("optimization_type") or []) or "not tagged",
        problem=p.get("problem") or "",
        key_results=p.get("key_results") or "",
        observations="\n".join(
            f"  {k}: {v}" for k, v in (p.get("observations") or {}).items()
        ) or "  (none)",
        body=body[:6000],
    )
    try:
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text.strip()
    except Exception as exc:
        return f"ERROR: {exc}"


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Per-paper review brief")
    parser.add_argument("slug", help="Paper slug (matches filename in data/papers/)")
    parser.add_argument("--no-llm", action="store_true",
                        help="Skip the LLM quality check")
    args = parser.parse_args()

    # Find the paper file
    path = DATA / "papers" / f"{args.slug}.md"
    if not path.exists():
        # Try prefix match
        matches = list((DATA / "papers").glob(f"{args.slug}*.md"))
        if len(matches) == 1:
            path = matches[0]
        elif len(matches) > 1:
            print(f"Ambiguous slug — matches: {[m.stem for m in matches]}")
            sys.exit(1)
        else:
            print(f"No paper found for slug: {args.slug!r}")
            sys.exit(1)

    post = frontmatter.load(path)
    p = dict(post.metadata)
    body = post.content
    slug = p.get("slug") or path.stem

    # ── header ────────────────────────────────────────────────────────────────
    print()
    print(f"{'═' * 64}")
    print(f"  Review Brief: {slug}")
    status = p.get("status") or "draft"
    paper_url = p.get("arxiv_url") or p.get("openreview_url") or ""
    if paper_url:
        print(f"  {paper_url}")
    print(f"  status: {status}  ·  {p.get('research_or_industry', '')}")
    print(f"{'═' * 64}")

    # ── data gaps ──────────────────────────────────────────────────────────────
    print(f"\n{hr('Data gaps')}")
    gaps = data_gaps(p)
    for ok, field, note in gaps:
        print(f"  {tick(ok)}  {field:<20} {note}")

    # ── validation ─────────────────────────────────────────────────────────────
    print(f"\n{hr('Validation')}")
    val_lines = run_validate(slug)
    if val_lines:
        for line in val_lines:
            print(f"  {line}")
    else:
        print("  ✓ No warnings")

    # ── heuristic checks ───────────────────────────────────────────────────────
    print(f"\n{hr('Heuristic checks')}")
    findings = heuristic_checks(p, body)
    if findings:
        for level, msg in findings:
            print(f"  {level}: {msg}")
    else:
        print("  ✓ No issues")

    # ── LLM quality check ──────────────────────────────────────────────────────
    if not args.no_llm:
        print(f"\n{hr('LLM quality check')}")
        print("  (running…)", end="\r", flush=True)
        critique = llm_check(p, body)
        print(" " * 14, end="\r")
        for line in critique.splitlines():
            print(f"  {line}")

    # ── review checklist ───────────────────────────────────────────────────────
    print(f"\n{hr('Checklist')}")
    checks = [
        "Read the paper (link above)",
        "Background: remove if domain obvious from title+key_results; keep ≤80 words only when non-obvious",
        "Verify key_results: hardware + model + metric + named baseline ≤160 chars",
        "Verify principles: core mechanism only, not tangential",
        "Verify observations: motivating problem insight, not solution description",
        "Verify Key Contributions: concrete artifact+mechanism; assumes reader knows principles",
        "Verify domain and topics: correct and complete",
        "Add optimization_type (algorithm / system / hardware / workflow / application)",
        "Fill code_url if findable (check OpenReview / arXiv abstract)",
        "Run: python scripts/validate.py",
        "Set status: under-review  →  published after confident sign-off",
    ]
    for c in checks:
        print(f"  [ ] {c}")
    print()


if __name__ == "__main__":
    main()
