---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Zhen Zheng
- Xin Ji
- Taosong Fang
- Fanghao Zhou
- Chuanjie Liu
- Gang Peng
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/microsoft/MixLLM/tree/batchllm_vllm_064
domain:
- llm-serving
organizations:
- Microsoft
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 1.3×–10.8× throughput over vLLM and SGLang on microbenchmarks and industry
  workloads; largest gains on high-prefix-sharing batched tasks
models_evaluated: []
observations:
  cache: Global prefix identification groups requests sharing the same
    prefix together for scheduling, ensuring KV cache of the common prefix is computed
    once and reused across all requests in the batch rather than being evicted by LRU
    before reuse.
  balance: Reordering requests to schedule high-decode-ratio requests
    first enables mixing decode tokens with later prefill chunks, filling the GPU with
    mixed computation rather than leaving it underutilized during decode-heavy phases.
  tier: Memory-centric token batching enlarges token batch sizes
    to increase GPU utilization by fitting more decode tokens into each forward pass
    iteration without exceeding KV cache memory limits.
official_category: ''
openreview_url: https://openreview.net/forum?id=IuVHde07l6
presentation_type: oral
principles:
- cache
- balance
- tier
problem: LLM inference engines optimized for streaming requests fail large-batch offline
  tasks with prefix sharing because LRU caches evict shared KV context before it can
  be reused, wasting compute and leaving GPU underutilized.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: batchllm-optimizing-large-batched-llm-inference-with-global-
status: draft
title: 'BatchLLM: Optimizing Large Batched LLM Inference with Global Prefix Sharing and Throughput-oriented Token Batching'
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
