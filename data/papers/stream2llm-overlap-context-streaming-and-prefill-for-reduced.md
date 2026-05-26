---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Rajveer Bachkaniwala
- Chengqi Luo
- Richard So
- Divya Mahajan
- Kexin Rong
award: ''
citations: null
citations_updated: ''
code_url: 'https://github.com/rajveerb/stream2llm/tree/mlsys_artifact'
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Up to 11× TTFT improvement through streaming architecture; throughput
  parity with non-streaming baselines maintained under memory pressure on real-world
  web crawl and ANN search workloads
models_evaluated: []
observations:
  pipeline: Stream2LLM overlaps context retrieval with LLM prefill
    processing, allowing incremental context chunks to trigger partial prefill computations
    rather than waiting for all retrieved context before beginning inference.
  cache: Longest common prefix matching minimizes redundant prefill
    computation when context updates dynamically; only the changed suffix is re-processed
    rather than re-prefilling the full updated context from scratch.
official_category: ''
openreview_url: https://openreview.net/forum?id=FuRo7Ur5Ib
organizations:
- Georgia Institute of Technology
presentation_type: oral
principles:
- pipeline
- cache
problem: LLM serving with context retrieval stalls on high retrieval latency while
  waiting for complete context before starting prefill, causing poor time-to-first-token.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: stream2llm-overlap-context-streaming-and-prefill-for-reduced
status: draft
title: 'Stream2LLM: Overlap Context Streaming and Prefill for Reduced Time-to-First-Token'
topics:
- prefill-decode-disaggregation
- prefix-caching
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3842
---

## Key Contributions

- **Streaming-aware scheduling for two retrieval modes**: Adaptive scheduling for append-mode (progressive context accumulation) and update-mode (iterative context refinement with cache invalidation) handles the distinct preemption patterns each mode requires.
- **Decoupled scheduling and resource acquisition**: Scheduling decisions are separated from physical resource allocation, enabling flexible preemption strategies guided by hardware-specific cost models without tying policy to mechanism.
- **Longest common prefix matching**: When streamed context changes dynamically, the system identifies the longest common prefix between the old and new context and only re-prefills the diverging suffix, eliminating redundant prefill computation on shared context.

## Trade-offs

- Streaming context introduces additional complexity in KV cache management; cache invalidation in update-mode requires careful coordination to avoid serving requests with stale KV states.
- The cost model that guides preemption decisions is hardware-specific; deploying Stream2LLM across heterogeneous clusters requires re-calibrating cost models for each hardware target.

## Nuances

- The 11× TTFT improvement is the peak case; gains depend heavily on retrieval latency relative to prefill time — workloads where retrieval is fast relative to prefill see smaller improvements.
- Throughput parity is maintained at the system level; individual requests may still experience higher latency variance under memory pressure compared to non-streaming baselines.
