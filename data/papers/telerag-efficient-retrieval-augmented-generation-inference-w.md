---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Chien-Yu Lin
- Keisuke Kamahori
- Yiyu Liu
- Xiaoxiang Shi
- Madhav Kashyap
- Yile Gu
- Rulin Shao
- Zihao Ye
- Kan Zhu
- Rohan Kadekodi
- Stephanie Wang
- Arvind Krishnamurthy
- Luis Ceze
- Baris Kasikci
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 1.98× latency reduction (single-query) and 1.83× throughput improvement
  (batched) with minimal GPU memory requirements.
models_evaluated: []
observations:
  pipeline: Lookahead retrieval predicts needed datastore entries
    during LLM generation and prefetches them from CPU to GPU in parallel, hiding
    retrieval latency behind decode.
  tier: Prefetching scheduler moves retrieval data from CPU memory
    to GPU just-in-time for each RAG lookup, keeping GPU memory overhead minimal while
    avoiding retrieval stalls.
  cache: Cache-aware scheduler routes repeated or similar queries to
    cached GPU-side retrievals, avoiding redundant CPU-GPU transfers for hot datastore
    entries.
official_category: ''
openreview_url: https://openreview.net/forum?id=YsOyCpMUYD
organizations:
- University of Washington
- University of Michigan
presentation_type: oral
principles:
- pipeline
- tier
- cache
problem: Large RAG datastores cannot fit in GPU memory, forcing expensive CPU-to-GPU
  retrieval transfers that block LLM generation and reduce throughput.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: telerag-efficient-retrieval-augmented-generation-inference-w
status: draft
title: 'TeleRAG: Efficient Retrieval-Augmented Generation Inference with Lookahead
  Retrieval'
topics:
- prefix-caching
- kv-cache
- streaming
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3796
---

## Key Contributions

- **Lookahead retrieval**: predicts which datastore entries will be needed for upcoming RAG lookups based on in-progress LLM generation, and transfers them from CPU to GPU memory in parallel with decode — hiding retrieval latency behind generation.
- **Prefetching scheduler**: manages CPU-to-GPU transfer ordering and bandwidth allocation across concurrent RAG requests, ensuring prefetched data arrives before the lookup is needed while minimizing GPU memory pressure.
- **Cache-aware scheduler**: routes requests with repeated or similar queries to GPU-cached retrieval results, avoiding redundant CPU-GPU transfers for frequently accessed datastore entries; supports efficient multi-GPU inference with low coordination overhead.
- Evaluated across multiple RAG benchmarks; achieves up to 1.98× average end-to-end latency reduction for single queries and 1.83× throughput improvement for batched inference, while keeping GPU memory requirements minimal.

## Trade-offs

- Lookahead retrieval requires accurately predicting future retrieval queries from partial generation; mispredictions cause wasted prefetch bandwidth or late arrivals that stall inference.
- The prefetching scheduler adds scheduling complexity proportional to datastore size and query diversity; very large or highly diverse datastores reduce prefetch accuracy.

## Nuances

- Throughput gains depend on the ratio of retrieval latency to generation latency; workloads where retrieval is fast (small datastores or local SSDs) will see smaller benefits.
- Multi-GPU evaluation shows good scalability but the paper does not deeply characterize behavior under GPU memory exhaustion from competing prefetch and KV cache demands.
