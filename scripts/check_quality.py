#!/usr/bin/env python3
"""Heuristic content-quality checks for paper entries.

Usage:
  python scripts/check_quality.py                   # heuristic checks only
  python scripts/check_quality.py --llm             # also run LLM quality checks
  python scripts/check_quality.py --slug flashagents  # single paper
  python scripts/check_quality.py --llm --slug flashagents

Exit code: 0 if no failures; 1 if at least one FAIL is reported.
"""

import argparse
import concurrent.futures
import re
import sys
from pathlib import Path

import frontmatter  # type: ignore
import yaml  # type: ignore

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"

# ── constants ─────────────────────────────────────────────────────────────────

HARDWARE_TOKENS = {
    "h100", "a100", "tpu", "b200", "gpu", "groqchip", "h200", "mi300x", "mi300",
    "v100", "a10", "a30", "l4", "l40", "t4", "a6000", "rtx", "nvlink",
}

MODEL_TOKENS = {
    "llama", "qwen", "mixtral", "gpt", "gemma", "mistral", "deepseek", "falcon",
    "yi", "phi", "bloom", "opt", "bert", "t5", "palm", "claude", "granite",
}

VAGUE_WORDS = {
    "significant", "outperforms", "various", "several", "state-of-the-art",
}

FORBIDDEN_PROBLEM_PREFIXES = [
    "Large language models",
    "Recent advances",
    "Modern",
    "Existing approaches",
    "The proliferation",
    "LLMs are",
    "Training frontier",
    "Efficient inference",
    "Large language model",
]

# Stopwords for Jaccard similarity
STOPWORDS = {
    "a", "an", "the", "is", "are", "can", "be", "to", "of", "in", "it", "that",
    "which", "by", "for", "with", "this", "these", "their", "when", "as", "and",
    "or", "not", "on", "at", "from", "has",
}

BASELINE_WORDS = {
    "vllm", "flashattention", "megatron", "pytorch", "triton", "cuda",
    "tensorflow", "jax", "xla", "megablocks", "fcfs", "orca", "sarathi",
    "tensorrt", "tgi", "sglang",
}


def load_principles() -> dict:
    with open(DATA / "principles.yaml") as f:
        return yaml.safe_load(f)


def tokenize(text: str) -> set:
    words = re.findall(r"[a-z]+", text.lower())
    return {w for w in words if w not in STOPWORDS}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ── heuristic checks ─────────────────────────────────────────────────────────

def heuristic_checks(slug: str, p: dict, body: str, principles: dict) -> list[tuple[str, str]]:
    """Return list of (level, message) tuples. level is 'FAIL' or 'WARN'."""
    findings: list[tuple[str, str]] = []
    key_results = p.get("key_results") or ""
    problem = p.get("problem") or ""
    observations = p.get("observations") or {}

    # 1. key_results must contain a digit or multiplication symbol
    if key_results and not re.search(r'[\d×]', key_results):
        findings.append(("FAIL", "key_results has no number (digit or ×)"))

    # 2. key_results should name hardware OR model
    if key_results:
        kr_lower = key_results.lower()
        has_hardware = any(hw in kr_lower for hw in HARDWARE_TOKENS)
        has_model = any(m in kr_lower for m in MODEL_TOKENS)
        if not has_hardware and not has_model:
            findings.append(("WARN", "key_results names neither hardware nor a model"))

    # 3. key_results vague language check
    kr_lower = key_results.lower()
    for vague in VAGUE_WORDS:
        if vague in kr_lower:
            if vague == "outperforms":
                # Flag if "outperforms" appears without a specific named baseline nearby
                # Look for a known baseline token within 5 words
                words = kr_lower.split()
                for i, w in enumerate(words):
                    if "outperforms" in w:
                        window = " ".join(words[max(0, i-3):i+6])
                        if not any(b in window for b in BASELINE_WORDS):
                            findings.append((
                                "WARN",
                                f"key_results: 'outperforms' without a specific named baseline",
                            ))
            else:
                findings.append(("WARN", f"key_results contains vague language: {vague!r}"))

    # 4. problem length and non-empty
    if not problem:
        findings.append(("FAIL", "problem field is empty"))
    elif len(problem) > 160:
        findings.append(("FAIL", f"problem is {len(problem)} chars (limit 160)"))

    # 5. problem forbidden prefixes
    for prefix in FORBIDDEN_PROBLEM_PREFIXES:
        if problem.startswith(prefix):
            findings.append(("WARN", f"problem starts with forbidden prefix: {prefix!r}"))
            break

    # 6. Key Contributions bullets: each should have a bold-named artifact **Name**:
    kc_match = re.search(r'^##\s+Key Contributions\s*\n(.*?)(?=^##|\Z)', body,
                         re.MULTILINE | re.DOTALL)
    if kc_match:
        kc_section = kc_match.group(1)
        bullets = [line for line in kc_section.splitlines() if line.strip().startswith("- ")]
        vague_bullets = []
        for bullet in bullets:
            if not re.search(r'\*\*[^*]+\*\*', bullet):
                vague_bullets.append(bullet.strip()[:80])
        if vague_bullets:
            findings.append((
                "WARN",
                f"Key Contributions has {len(vague_bullets)} bullet(s) without a bold artifact "
                f"**Name**: — first: {vague_bullets[0]!r}",
            ))

        # 7. Key Contributions: numbers without baseline context
        for bullet in bullets:
            # Look for a number followed by × or % that isn't qualified with "vs."
            if re.search(r'\d+[\.\d]*\s*[×%]', bullet):
                if not re.search(r'\bvs\.?\b|\bover\b|\bcompared\b|\bbaseline\b', bullet,
                                 re.IGNORECASE):
                    findings.append((
                        "WARN",
                        f"Key Contributions bullet has number with × or % but no baseline context: "
                        f"{bullet.strip()[:80]!r}",
                    ))
                    break  # one per paper

    # 8. Observation cross-paper duplicate detection is done at batch level;
    #    here we check per-paper: observations should not be identical to each other
    obs_values = list(observations.values())
    seen_texts: set = set()
    for obs_slug, obs_text in observations.items():
        text = str(obs_text or "").strip()
        if text in seen_texts:
            findings.append(("WARN", f"observations[{obs_slug}] is identical to another observation in this paper"))
        seen_texts.add(text)

    # Extra: observation word overlap with principle description
    for obs_slug, obs_text in observations.items():
        if not obs_text or obs_slug not in principles:
            continue
        principle_desc = principles[obs_slug].get("description") or ""
        obs_tokens = tokenize(str(obs_text))
        desc_tokens = tokenize(str(principle_desc))
        sim = jaccard(obs_tokens, desc_tokens)
        if sim > 0.5:
            findings.append((
                "WARN",
                f"observations[{obs_slug}] may restate the principle (word overlap {sim:.0%})",
            ))

    return findings


# ── cross-paper duplicate observation check ───────────────────────────────────

def cross_paper_obs_check(all_papers: list[tuple[str, dict]]) -> list[tuple[str, str]]:
    """Return (message) for cross-paper identical observation texts."""
    # {principle_slug: {obs_text: [slugs]}}
    principle_to_obs: dict = {}
    for slug, p in all_papers:
        for obs_slug, obs_text in (p.get("observations") or {}).items():
            text = str(obs_text or "").strip()
            if not text:
                continue
            if obs_slug not in principle_to_obs:
                principle_to_obs[obs_slug] = {}
            if text not in principle_to_obs[obs_slug]:
                principle_to_obs[obs_slug][text] = []
            principle_to_obs[obs_slug][text].append(slug)

    msgs = []
    for obs_slug, text_map in principle_to_obs.items():
        for text, slugs in text_map.items():
            if len(slugs) > 1:
                msgs.append(
                    f"CROSS-PAPER: identical observations[{obs_slug}] in {', '.join(slugs)} "
                    f"— possible copy-paste"
                )
    return msgs


# ── LLM checks ────────────────────────────────────────────────────────────────

LLM_PROMPT_TEMPLATE = """\
You are reviewing a paper entry in an ML systems paper index. The audience is senior ML \
systems engineers. Evaluate the entry quality on these 4 dimensions:

1. PROBLEM VOICE: Does `problem` read like a practitioner describing a real pain point \
(specific, concrete) or like an academic abstract (vague, generic)?

2. KEY CONTRIBUTIONS SPECIFICITY: Do the `## Key Contributions` bullets each name a \
specific artifact (algorithm/data structure/protocol) with a concrete mechanism? \
Or are they vague ("we propose a new approach")?

3. OBSERVATION SPECIFICITY: For each observation, does it say something paper-specific \
(what the authors measured/noticed) or does it just restate the general principle?

4. MISSING NUANCES: Based on the problem and contributions described, what obvious \
limitations or gotchas are likely present that are missing from `## Nuances`?

For each dimension, give ONE sentence of critique if there's a real issue, or "OK" if fine.
Be concise. Don't repeat the content back to me.

--- PAPER ENTRY ---
slug: {slug}
problem: {problem}
key_results: {key_results}
principles: {principles}
observations: {observations}

{body}
--- END ---

Format your response as:
PROBLEM VOICE: <one sentence or OK>
KEY CONTRIBUTIONS: <one sentence or OK>
OBSERVATIONS: <one sentence or OK>
MISSING NUANCES: <one sentence or OK>
"""


def llm_check_paper(slug: str, p: dict, body: str) -> tuple[str, str]:
    """Return (slug, critique_text). Runs a single API call."""
    try:
        import anthropic  # type: ignore
    except ImportError:
        return (slug, "ERROR: 'anthropic' package not installed")

    client = anthropic.Anthropic()
    prompt = LLM_PROMPT_TEMPLATE.format(
        slug=slug,
        problem=p.get("problem") or "",
        key_results=p.get("key_results") or "",
        principles=", ".join(p.get("principles") or []),
        observations="\n".join(
            f"  {k}: {v}" for k, v in (p.get("observations") or {}).items()
        ),
        body=body[:3000],  # truncate very long bodies
    )
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        return (slug, message.content[0].text.strip())
    except Exception as exc:
        return (slug, f"ERROR: {exc}")


def run_llm_checks(papers: list[tuple[str, dict, str]]) -> None:
    """Run LLM checks with concurrency=4 and print results."""
    print("\n=== LLM Quality Checks ===\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(llm_check_paper, slug, p, body): slug
                   for slug, p, body in papers}
        for future in concurrent.futures.as_completed(futures):
            slug, critique = future.result()
            print(f"[{slug}]")
            print(critique)
            print()


# ── main ─────────────────────────────────────────────────────────────────────

def load_papers(slug_filter: str | None = None) -> list[tuple[str, dict, str]]:
    """Load papers as (slug, metadata, body) triples."""
    papers = []
    for path in sorted((DATA / "papers").glob("*.md")):
        post = frontmatter.load(path)
        meta = dict(post.metadata)
        slug = meta.get("slug") or path.stem
        if slug_filter and slug != slug_filter:
            continue
        papers.append((slug, meta, post.content))
    return papers


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Content quality checks for paper entries",
    )
    parser.add_argument(
        "--llm", action="store_true",
        help="Also run LLM quality checks (requires ANTHROPIC_API_KEY)",
    )
    parser.add_argument(
        "--slug", default=None,
        help="Run checks on a single paper by slug",
    )
    args = parser.parse_args()

    papers = load_papers(slug_filter=args.slug)
    if not papers:
        if args.slug:
            print(f"No paper found with slug: {args.slug!r}")
        else:
            print("No papers found.")
        sys.exit(1)

    principles = load_principles()
    has_failures = False

    print(f"=== Heuristic Quality Checks ({len(papers)} paper(s)) ===\n")

    all_paper_metas = [(slug, p) for slug, p, _ in papers]

    for slug, p, body in papers:
        findings = heuristic_checks(slug, p, body, principles)
        if findings:
            print(f"[{slug}]")
            for level, msg in findings:
                marker = "FAIL" if level == "FAIL" else "WARN"
                print(f"  {marker}: {msg}")
                if level == "FAIL":
                    has_failures = True
            print()

    # Cross-paper checks
    cross_msgs = cross_paper_obs_check(all_paper_metas)
    if cross_msgs:
        print("[cross-paper]")
        for msg in cross_msgs:
            print(f"  {msg}")
        print()

    if not any(True for _, p, body in papers
               for _ in heuristic_checks(_, p, body, principles)):
        print("No heuristic issues found.")

    if args.llm:
        run_llm_checks(papers)

    if has_failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
