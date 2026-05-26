#!/usr/bin/env python3
"""One-shot migration: rename principle slugs across all paper files.

Old → new mapping:
  avoid-redundant-work     → cache
  overlap-independent-work → pipeline
  exploit-sparsity         → skip
  reduce-data-movement     → fuse
  exploit-memory-hierarchy → tier
  balance-utilization      → balance
  ai-solves-verifiable     → search-ai
"""

import re
import sys
from pathlib import Path

SLUG_MAP = {
    "avoid-redundant-work": "cache",
    "overlap-independent-work": "pipeline",
    "exploit-sparsity": "skip",
    "reduce-data-movement": "fuse",
    "exploit-memory-hierarchy": "tier",
    "balance-utilization": "balance",
    "ai-solves-verifiable": "search-ai",
}

def migrate_file(path: Path, dry_run: bool) -> int:
    text = path.read_text()
    original = text
    for old, new in SLUG_MAP.items():
        # principles list entry:  "- old-slug"
        text = re.sub(rf"(- ){re.escape(old)}\b", rf"\g<1>{new}", text)
        # observations dict key:  "  old-slug:"  (use str.replace — no quantifier f-string issue)
        text = text.replace(f"  {old}:", f"  {new}:")
    if text != original:
        if not dry_run:
            path.write_text(text)
        return 1
    return 0

def main():
    dry_run = "--dry-run" in sys.argv
    papers_dir = Path(__file__).parent.parent / "data" / "papers"
    changed = 0
    for p in sorted(papers_dir.glob("*.md")):
        changed += migrate_file(p, dry_run)
    mode = "Would change" if dry_run else "Changed"
    print(f"{mode} {changed} / {len(list(papers_dir.glob('*.md')))} files")

if __name__ == "__main__":
    main()
