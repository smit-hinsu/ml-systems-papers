---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Yi Li
- Lianjie Cao
- Faraz Ahmed
- Puneet Sharma
- Bingzhe Li
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 1.1×–31.5× retrieval latency speedup and 1.1×–14.5× token footprint
  reduction over dense-vector and knowledge-graph memory baselines on LoCoMo and LongMemEval
models_evaluated: []
observations:
  cache: Compact binary signatures enable semantic search in the compressed
    domain without expanding embeddings; the Dynamic Wavelet Matrix avoids re-decompressing
    memory entries for queries that can be resolved from the binary index alone.
  tier: The DWM co-indexes binary signatures and lossless token-ID
    streams together in a compressed structure, keeping frequently searched indices
    in fast memory while full token streams stay compressed until reconstruction is
    needed.
official_category: ''
openreview_url: https://openreview.net/forum?id=0sUYZh9D4a
organizations:
- University of Texas at Dallas
- Hewlett Packard Enterprise
presentation_type: oral
principles:
- cache
- tier
problem: Agentic AI memory systems using dense vectors or knowledge graphs incur high
  retrieval latency and storage costs that prevent scaling to long-horizon deployments.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: hippocampus-an-efficient-and-scalable-memory-module-for-agen
status: draft
title: 'Hippocampus: An Efficient and Scalable Memory Module for Agentic AI'
topics:
- kv-cache
- memory-management
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3863
---

## Key Contributions

- **Binary signature semantic search**: Compact binary signatures replace high-dimensional float embeddings for semantic similarity search, enabling ultra-fast semantic lookup in the compressed domain without costly dense-vector dot products.
- **Lossless token-ID streams**: Exact content reconstruction uses lossless token-ID streams rather than storing raw text or embeddings, separating the search index from the content store for independent optimization of each.
- **Dynamic Wavelet Matrix (DWM)**: A single compressed data structure co-indexes both binary signatures and token-ID streams, supporting search directly in the compressed domain; storage grows linearly with memory size for a fixed tokenizer vocabulary.

## Trade-offs

- Binary signatures are lossy approximations of semantic similarity; recall may degrade for queries whose nearest neighbors are poorly separated in the binary space.
- The fixed-vocabulary assumption means HIPPOCAMPUS must be rebuilt or adapted when the tokenizer changes, limiting portability across LLM generations.

## Nuances

- The 31.5× speedup represents the best case over the slowest baseline; the 1.1× lower bound reflects scenarios where the evaluated baselines are already competitive.
- Task accuracy is reported as "competitive," not strictly better; the system trades some accuracy for the observed latency and token-footprint reductions.
