---
agentic_models: []
arxiv_date: 2024-12
arxiv_url: https://arxiv.org/abs/2412.03594
authors:
- Zhen Zheng
- Xin Ji
- Taosong Fang
- Fanghao Zhou
- Chuanjie Liu
- Gang Peng
award: ''
citations: 42
citations_updated: '2026-07-31'
code_url: https://github.com/microsoft/MixLLM/tree/batchllm_vllm_064
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 1.3×–10.8× throughput vs. vLLM/SGLang on microbenchmarks; largest gains
  on high-prefix-sharing batch tasks
models_evaluated: []
observations:
  schedule: Offline batch jobs expose every request before scheduling starts, so
    request order can be planned across the whole batch instead of guessed one
    arrival at a time by an LRU cache.
  cache: Global prefix scan groups all requests sharing a prefix before scheduling;
    the common KV cache is computed once and stays resident rather than being evicted
    by LRU between requests.
official_category: ''
openreview_url: https://openreview.net/forum?id=IuVHde07l6
optimization_type: []
organizations:
- Microsoft
presentation_type: oral
principles:
- cache
- schedule
problem: Batch LLM engines optimized for streaming evict shared KV before reuse; LRU
  caches waste compute and underutilize GPUs on prefix-heavy workloads.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3833.pdf
slug: batchllm-optimizing-large-batched-llm-inference-with-global-
status: draft
title: 'BatchLLM: Optimizing Large Batched LLM Inference with Global Prefix Sharing
  and Throughput-oriented Token Batching'
topics:
- prefix-caching
- kv-cache
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3833
---

## Key Contributions

- **Global prefix identification**: explicitly scans the entire request batch to identify all shared prefixes before scheduling begins, avoiding the fragmented per-request LRU cache lookups that cause premature eviction in streaming systems
- **Prefix-aware scheduling**: groups requests sharing the same prefix together so KV context is available when needed; requests sharing a prefix are coscheduled to maximize cache reuse without risking eviction between grouped requests
- **Decode-first reordering**: reorders requests within the batch to schedule high decode-to-prefill ratio requests first, enabling decode tokens to be mixed with later prefill chunks and improving GPU utilization
- **Memory-centric token batching**: enlarges the effective token batch size within memory constraints, saturating GPU compute during decode phases that would otherwise leave capacity idle
- **1.3×–10.8× throughput improvement**: evaluated against vLLM and SGLang across microbenchmarks and a typical industry workload under different hardware environments

## Trade-offs

- Global prefix identification requires a full pass over the batch before scheduling starts; this adds latency at the start of batch processing and is less suited to streaming arrival patterns.
- Decode-first reordering increases the time-to-first-token for requests with large prefill phases; not appropriate for latency-sensitive interactive workloads.

## Nuances

- The 10.8× peak speedup applies to workloads with very high prefix-sharing ratios; realistic industry workloads show lower but still substantial gains.
- The system is designed for large batched/offline tasks; the streaming-oriented design of vLLM and SGLang is an intentional trade-off for their target workloads, not a bug.
