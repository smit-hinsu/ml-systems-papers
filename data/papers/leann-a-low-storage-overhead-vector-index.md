---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
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
key_results: Up to 50× index size reduction vs. conventional HNSW-style indices while
  maintaining comparable accuracy and latency for RAG applications on real-world benchmarks
models_evaluated: []
observations:
  cache: LEANN recomputes embeddings on the fly at query time rather
    than storing precomputed vectors, trading CPU/GPU compute for storage elimination;
    index metadata is compressed to 5% of original data size.
  tier: Compressed proximity graph retains only the graph structure
    and IDs rather than full embeddings, fitting the graph into a fraction of the
    storage and enabling deployment on personal devices or large-scale distributed
    systems without embedding storage.
official_category: ''
openreview_url: https://openreview.net/forum?id=e8Dp5QkFxP
organizations:
- UC Berkeley
- Amazon
- Wuhan University
presentation_type: oral
principles:
- cache
- tier
problem: Vector search indices storing full embeddings and graph metadata can be several
  times larger than raw data, making deployment on personal devices or massive datasets
  impractical.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: leann-a-low-storage-overhead-vector-index
status: draft
title: 'LEANN: A Low-Storage Overhead Vector Index'
topics:
- memory-management
- prefix-caching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3786
---

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
