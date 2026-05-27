---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Yichuan Wang
- Zhifei Li
- Shu Liu
- Yongji Wu
- Ziming Mao
- Yilong Zhao
- Xiao Yan
- Zhiying Xu
- Yang Zhou
- Ion Stoica
- Sewon Min
- Matei Zaharia
- Joseph Gonzalez
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Up to 50× index size reduction vs. HNSW-style indices while maintaining
  comparable accuracy and latency for RAG on real-world benchmarks
models_evaluated: []
observations:
  recompute: LEANN drops precomputed embeddings after index construction and recomputes
    them at query time from compressed graph structure; storage shrinks to 1.5 bytes/vector
    at ~2× query latency.
  tier: Compressed proximity graph retains only structure and IDs, fitting to 5% of
    original storage and enabling deployment on personal devices or large-scale systems
    without embedding storage.
official_category: ''
openreview_url: https://openreview.net/forum?id=e8Dp5QkFxP
organizations:
- UC Berkeley
- Amazon
- Wuhan University
presentation_type: oral
principles:
- tier
- recompute
problem: Vector search indices storing full embeddings and graph metadata are several
  times larger than raw data, making personal-device deployment impractical.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3786_vlIWXsd.pdf
slug: leann-a-low-storage-overhead-vector-index
status: draft
title: 'LEANN: A Low-Storage Overhead Vector Index'
topics:
- memory-management
- prefix-caching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3786
---

## Background

Vector search indices (e.g., HNSW) store both embeddings and multi-layer graph metadata, typically occupying 3–10× more storage than raw text. For RAG on a laptop or personal device, this overhead makes indexing even a moderately large corpus impractical — the index alone can exhaust disk before a user's data is ingested.

## Key Contributions

- **On-the-fly embedding recomputation**: LEANN discards stored embeddings and recomputes them at query time using the original encoder, reducing index storage to graph structure and IDs only (≈5% of original data size).
- **Compressed proximity graph**: State-of-the-art proximity graph (HNSW-style) indices are compressed while preserving search accuracy, eliminating the redundant metadata overhead that causes conventional indices to exceed raw data size by several times.
- **Storage-efficient construction and updates**: The compressed index supports incremental updates and construction without materializing full embeddings, enabling practical deployment on evolving datasets.

## Trade-offs

- On-the-fly recomputation adds encoding latency per query; workloads with strict latency SLOs may need to balance storage savings against per-query compute cost.
- Recomputation requires the original encoder to be available and fast; large or slow encoders (e.g., cross-encoders) would undermine the latency parity claim.

## Nuances

- The 50× storage reduction is the peak case; practical deployments targeting high recall may need to retain more graph metadata, reducing the compression ratio.
- "Comparable latency" for RAG is evaluated on specific benchmark retrieval tasks; latency parity may not hold for extremely large corpora where recomputation overhead accumulates.