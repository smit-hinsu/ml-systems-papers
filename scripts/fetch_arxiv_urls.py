#!/usr/bin/env python3
"""Fetch arxiv_url for a list of paper slugs via Semantic Scholar API."""

import time
import urllib.parse
import urllib.request
import json
import re
import sys

PAPERS_DIR = "/Users/smithinsu/claude/mlsys26/data/papers"

SLUGS = [
    "airs-scaling-live-inference-in-resource-constrained-environm",
    "attribution-based-sparse-activation-in-large-language-models",
    "approxmlir-accuracy-aware-compiler-for-compound-ml-system",
    "beam-joint-resourcepower-optimization-for-energy-efficient-l",
    "boost-bottleneck-optimized-scalable-training-framework-for-l",
    "cage-curvature-aware-gradient-estimation-for-accurate-quanti",
    "catwild-compiler-autotuning-for-tpu-workloads-in-the-wild",
    "breaking-the-ice-analyzing-cold-start-latency-in-vllm",
    "cost-aware-duration-prediction-for-software-upgrades-in-data",
    "csle-a-reinforcement-learning-platform-for-autonomous-securi",
    "dataflow-is-all-you-need",
    "demystifying-the-mixture-of-experts-serving-tax",
    "driftbench-measuring-and-predicting-infrastructure-drift-in-",
    "dreamddp-accelerating-low-bandwidth-geo-distributed-llm-trai",
    "dynaflow-transparent-and-flexible-intra-device-parallelism-v",
    "efficient-vram-constrained-xlm-inference-on-clients",
    "efficient-long-context-language-model-training-by-core-atten",
    "faascale-unlocking-fast-llm-scaling-for-serverless-inference",
    "flashagents",
    "farskip-collective-unhobbling-blocking-communication-in-mixt",
]


def get_title(slug):
    path = f"{PAPERS_DIR}/{slug}.md"
    with open(path) as f:
        for line in f:
            if line.startswith("title:"):
                # Strip the "title: " prefix and quotes
                title = line[6:].strip()
                title = title.strip("'\"")
                return title
    return None


def search_semantic_scholar(title, retries=3):
    encoded = urllib.parse.quote(title)
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded}&fields=title,externalIds&limit=3"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 15 * (attempt + 1)
                print(f"  429 rate limit, waiting {wait}s...", flush=True)
                time.sleep(wait)
            else:
                print(f"  HTTP error {e.code}", flush=True)
                return None
        except Exception as ex:
            print(f"  Error: {ex}", flush=True)
            return None
    return None


def find_arxiv_id(data, title):
    """Find best-matching paper in results and return ArXiv ID if present."""
    if not data or "data" not in data:
        return None
    title_lower = title.lower()
    for paper in data["data"]:
        paper_title = paper.get("title", "").lower()
        # Simple similarity: check if most words from query title appear in result
        query_words = set(re.findall(r'\w+', title_lower))
        result_words = set(re.findall(r'\w+', paper_title))
        if len(query_words) > 0:
            overlap = len(query_words & result_words) / len(query_words)
            if overlap >= 0.6:
                ext_ids = paper.get("externalIds", {})
                if "ArXiv" in ext_ids:
                    return ext_ids["ArXiv"]
    return None


def update_file(slug, arxiv_id):
    path = f"{PAPERS_DIR}/{slug}.md"
    with open(path) as f:
        content = f.read()
    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
    new_content = re.sub(r"arxiv_url: ''", f"arxiv_url: '{arxiv_url}'", content, count=1)
    if new_content == content:
        print(f"  WARNING: could not replace arxiv_url field in {slug}", flush=True)
        return False
    with open(path, "w") as f:
        f.write(new_content)
    return True


found = []
not_found = []

for i, slug in enumerate(SLUGS):
    title = get_title(slug)
    if not title:
        print(f"[{i+1}/20] {slug}: could not read title", flush=True)
        not_found.append(slug)
        continue

    print(f"[{i+1}/20] {slug}", flush=True)
    print(f"  Title: {title}", flush=True)

    data = search_semantic_scholar(title)
    arxiv_id = find_arxiv_id(data, title) if data else None

    if arxiv_id:
        ok = update_file(slug, arxiv_id)
        if ok:
            print(f"  FOUND: {arxiv_id}", flush=True)
            found.append((slug, arxiv_id))
        else:
            print(f"  Found ID {arxiv_id} but file update failed", flush=True)
            not_found.append(slug)
    else:
        print(f"  NOT FOUND", flush=True)
        not_found.append(slug)

    if i < len(SLUGS) - 1:
        time.sleep(1.0)

print(f"\n=== SUMMARY ===", flush=True)
print(f"Found: {len(found)}/{len(SLUGS)}", flush=True)
for slug, arxiv_id in found:
    print(f"  {slug}: {arxiv_id}", flush=True)
print(f"Not found: {len(not_found)}", flush=True)
for slug in not_found:
    print(f"  {slug}", flush=True)
