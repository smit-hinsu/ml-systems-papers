#!/usr/bin/env python3
"""
Fill the paper_summary prompt with a paper stub, call Claude, and write back.

Usage:
    # Print the filled prompt (for copy-paste into Claude web):
    python scripts/summarize_paper.py pike-pytorch-llm-agents

    # Call the API and write result back to stub:
    python scripts/summarize_paper.py pike-pytorch-llm-agents --write

    # Add personal reading notes:
    python scripts/summarize_paper.py pike --write --notes "key insight: ..."

    # Provide full paper text from a file (better than abstract-only):
    python scripts/summarize_paper.py pike --write --text ~/Downloads/pike.txt

    # Batch: process all draft papers (requires ANTHROPIC_API_KEY):
    python scripts/summarize_paper.py --all --write

    # Batch with concurrency:
    python scripts/summarize_paper.py --all --write --concurrency 4

    # Dry-run: print merged result without saving:
    python scripts/summarize_paper.py pike --write --dry-run
"""

import argparse
import asyncio
import re
import sys
from pathlib import Path

import frontmatter

ROOT = Path(__file__).parent.parent
PAPERS_DIR = ROOT / "data" / "papers"
PROMPT_FILE = ROOT / "prompts" / "paper_summary.md"

DEFAULT_MODEL = "claude-sonnet-4-6"

# Fields the API response may fill; original values take priority unless listed in ALWAYS_REPLACE
FILL_IF_EMPTY = {
    "domain", "topics", "principles", "hardware", "models_evaluated",
    "agentic_models", "research_or_industry", "organizations",
}
ALWAYS_REPLACE = {"problem", "key_results"}


# ── helpers ────────────────────────────────────────────────────────────────────

def find_stub(slug: str) -> Path:
    candidates = list(PAPERS_DIR.glob(f"{slug}*.md"))
    if not candidates:
        sys.exit(f"No stub found for slug: {slug!r}  (in {PAPERS_DIR})")
    if len(candidates) > 1:
        sys.exit(f"Ambiguous: {slug!r} matches " + ", ".join(p.name for p in candidates))
    return candidates[0]


def all_draft_paths() -> list[Path]:
    paths = []
    for p in sorted(PAPERS_DIR.glob("*.md")):
        post = frontmatter.load(p)
        if post.metadata.get("status") == "draft":
            paths.append(p)
    return paths


def build_paper_text(post) -> str:
    meta = post.metadata
    lines = []
    for field in ("title", "authors", "organizations"):
        val = meta.get(field)
        if val:
            lines.append(f"{field}: {val}")
    for field in ("arxiv_url", "openreview_url", "mlsys_url"):
        val = meta.get(field, "")
        if val:
            lines.append(f"{field}: {val}")
    body = post.content.strip()
    if body:
        lines += ["", "--- existing stub body ---", body]
    return "\n".join(lines)


def extract_prompt_block(prompt_md: str) -> str:
    m = re.search(r"<prompt>(.*?)</prompt>", prompt_md, re.DOTALL)
    if not m:
        sys.exit("Could not find <prompt>…</prompt> in prompt file.")
    return m.group(1).strip()


def fill_prompt(prompt_text: str, paper_text: str, notes: str) -> str:
    filled = prompt_text.replace("{{PAPER_TEXT}}", paper_text or "(none)")
    filled = filled.replace("{{NOTES}}", notes or "(none)")
    return filled


# ── parsing & merging ──────────────────────────────────────────────────────────

def parse_response(response: str):
    """
    Parse a Claude response into a frontmatter Post.
    The prompt instructs Claude to start with '---' on line 1; handle the case
    where it wraps in a code fence anyway.
    """
    text = response.strip()

    # Strip leading code fence if present
    if text.startswith("```"):
        text = re.sub(r"^```[a-z]*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
        text = text.strip()

    # Find the first '---' and trim anything before it (preamble)
    m = re.search(r"(---\s*\n)", text)
    if m:
        text = text[m.start():]

    try:
        return frontmatter.loads(text)
    except Exception as e:
        raise ValueError(f"Could not parse response as frontmatter: {e}\n\nFirst 400 chars:\n{text[:400]}")


def merge(orig_path: Path, new_post) -> str:
    """Merge new_post into orig_path and return the resulting YAML string."""
    orig = frontmatter.load(orig_path)

    # Always replace these
    for key in ALWAYS_REPLACE:
        val = new_post.metadata.get(key)
        if val:
            orig.metadata[key] = val

    # Fill empty fields
    for key in FILL_IF_EMPTY:
        existing = orig.metadata.get(key)
        new_val = new_post.metadata.get(key)
        is_empty = not existing or existing in ([], "")
        if is_empty and new_val:
            orig.metadata[key] = new_val

    # Replace body
    new_body = new_post.content.strip()
    if new_body:
        orig.content = "\n\n" + new_body + "\n"

    return frontmatter.dumps(orig)


# ── API call ───────────────────────────────────────────────────────────────────

def call_api_sync(prompt: str, model: str) -> str:
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic package not installed. Run: .venv/bin/pip install anthropic")
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


async def call_api_async(prompt: str, model: str, sem: asyncio.Semaphore) -> str:
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic package not installed.")
    async with sem:
        client = anthropic.AsyncAnthropic()
        msg = await client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text


# ── single paper ──────────────────────────────────────────────────────────────

def process_one(path: Path, text_file: str | None, notes: str, model: str,
                write: bool, dry_run: bool):
    post = frontmatter.load(path)
    paper_text = Path(text_file).read_text() if text_file else build_paper_text(post)

    prompt_md = PROMPT_FILE.read_text(encoding="utf-8")
    prompt_text = extract_prompt_block(prompt_md)
    filled = fill_prompt(prompt_text, paper_text, notes)

    if not write:
        print(filled)
        return

    print(f"  {path.stem}: calling {model}…", flush=True)
    response = call_api_sync(filled, model)

    try:
        new_post = parse_response(response)
    except ValueError as e:
        print(f"  {path.stem}: ERROR – {e}", file=sys.stderr)
        return

    merged = merge(path, new_post)

    if dry_run:
        print(merged)
        return

    path.write_text(merged, encoding="utf-8")
    print(f"  {path.stem}: updated")


# ── batch ─────────────────────────────────────────────────────────────────────

async def process_batch(paths: list[Path], model: str, concurrency: int, dry_run: bool):
    prompt_md = PROMPT_FILE.read_text(encoding="utf-8")
    prompt_text = extract_prompt_block(prompt_md)
    sem = asyncio.Semaphore(concurrency)

    async def handle(path: Path):
        post = frontmatter.load(path)
        paper_text = build_paper_text(post)
        filled = fill_prompt(prompt_text, paper_text, "")
        print(f"  {path.stem}: calling {model}…", flush=True)
        try:
            response = await call_api_async(filled, model, sem)
            new_post = parse_response(response)
        except Exception as e:
            print(f"  {path.stem}: ERROR – {e}", file=sys.stderr)
            return
        merged = merge(path, new_post)
        if dry_run:
            print(f"\n=== {path.name} ===\n{merged[:300]}…\n")
            return
        path.write_text(merged, encoding="utf-8")
        print(f"  {path.stem}: updated")

    await asyncio.gather(*[handle(p) for p in paths])


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Summarize a paper stub via Claude")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("slug", nargs="?", help="Paper slug (or partial match)")
    group.add_argument("--all", action="store_true", help="Process all draft papers")

    parser.add_argument("--write", action="store_true",
                        help="Call the API and write result back to stub")
    parser.add_argument("--dry-run", action="store_true",
                        help="With --write: print merged result, don't save")
    parser.add_argument("--text", metavar="FILE",
                        help="Path to full paper text file (overrides stub body)")
    parser.add_argument("--notes", metavar="TEXT",
                        help="Personal reading notes")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Claude model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--concurrency", type=int, default=3,
                        help="Parallel API calls for --all (default: 3)")
    args = parser.parse_args()

    if args.all:
        paths = all_draft_paths()
        if not paths:
            print("No draft papers found.")
            return
        print(f"Processing {len(paths)} draft papers (concurrency={args.concurrency})…")
        asyncio.run(process_batch(paths, args.model, args.concurrency, args.dry_run))
    else:
        path = find_stub(args.slug)
        process_one(path, args.text, args.notes or "", args.model, args.write, args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
