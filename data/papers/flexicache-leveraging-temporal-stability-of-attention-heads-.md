---
title: 'FlexiCache: Leveraging Temporal Stability of Attention Heads for Efficient KV Cache Management'
slug: flexicache-leveraging-temporal-stability-of-attention-heads-
authors:
- Nazmul Takbir
- HamidReza Alikhani Koshkak
- Nikil Dutt
- Sangeetha Abdu Jyothi
organizations:
- UC Irvine
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3838
openreview_url: https://openreview.net/forum?id=GgX6dPJx9M
arxiv_url: https://arxiv.org/abs/2511.00868
slides_url: ''
code_url: ''
project_url: ''
official_category: ''
presentation_type: oral
award: ''
arxiv_date: '2025-11'
domain:
- llm-serving
topics:
- kv-cache
- sparse-attention
- cpu-offload
principles:
- skip
- tier
observations:
  skip: Classifying 75% of heads as stable and caching only top-K pages for them reduces GPU KV footprint by up to 70% with near-zero accuracy drop on long-context workloads.
  tier: Stable-head pages beyond top-K are offloaded to 1.1TB DDR5 host memory and asynchronously transferred via UVA CUDA kernels overlapped with computation.
hardware:
- H100
models_evaluated:
- Llama-3.1-8B-Instruct
- Mistral-7B-Instruct-v0.2
- Mistral-Small-24B-Instruct-2501
- Qwen2.5-32B-Instruct
agentic_models: []
citations: null
citations_updated: ''
research_or_industry: research
problem: KV cache memory grows with context and generation length, limiting LLM serving throughput; naively evicting tokens degrades accuracy in long-generation tasks.
key_results: 70% GPU memory reduction, 1.38–1.55× offline throughput and 1.6–2.1× lower online token latency on H100 across four models vs. vLLM.
status: under-review
reading_status: want-to-read
indexed_by: smithinsu
indexed_date: '2026-05-25'
---

## Key Contributions

- **Temporal stability classification**: Scores each KV head by how consistently it attends to the same tokens across decoding steps; classifies the least-stable 25% as unstable (retain all GPU pages) and the rest as stable (keep only top-K pages on GPU)
- **Hierarchical memory management**: Stable heads offload low-ranked pages to 180GB DDR5 host memory via custom CUDA kernels using Unified Virtual Addressing (UVA), overlapping transfers with computation; unstable heads retain full GPU residency
- **Periodic reranking**: Every 16 decode steps, re-scores stable-head pages using query-aware importance to fetch newly promoted top pages, maintaining accuracy during long generation
- **Sparse attention kernels**: Custom decode kernels attend only to selected top-K pages per head, reducing attention FLOPs proportionally to evicted fraction; implemented on top of vLLM

## Trade-offs

- PCIe 5.0 bandwidth (64 GB/s bidirectional) is the bottleneck for asynchronous host fetches; older PCIe 4.0 interconnects halve bandwidth and would reduce throughput gains.
- The 25% unstable threshold is a fixed heuristic; accuracy-sensitive tasks on different model families may require per-model calibration.

## Nuances

- Reranking every 16 steps introduces periodic latency spikes; the interval is a trade-off between token importance freshness and overhead, not characterized across tasks.
- Evaluation uses PCIe 5.0 and 1.1TB DDR5 — hardware configurations not yet common in typical serving deployments.
