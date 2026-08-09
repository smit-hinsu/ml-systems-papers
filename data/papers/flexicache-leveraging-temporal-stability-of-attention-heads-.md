---
agentic_models: []
arxiv_date: 2025-11
arxiv_url: https://arxiv.org/abs/2511.00868
authors:
- Nazmul Takbir
- HamidReza Alikhani Koshkak
- Nikil Dutt
- Sangeetha Abdu Jyothi
award: ''
citations: 3
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-serving
hardware:
- H100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 70% GPU memory reduction, 1.38–1.55× offline throughput and 1.6–2.1×
  lower online token latency on H100 across four models vs. vLLM.
models_evaluated:
- Llama-3.1-8B-Instruct
- Mistral-7B-Instruct-v0.2
- Mistral-Small-24B-Instruct-2501
- Qwen2.5-32B-Instruct
observations:
  approximate: Three quarters of heads attend to the same tokens step after step,
    so their remaining KV pages can be dropped from the attention math for a small
    but real accuracy cost.
  tier: KV pages a stable head has stopped attending to still hold HBM, while host
    DDR5 sits an order of magnitude larger and mostly empty next to it.
official_category: ''
openreview_url: https://openreview.net/forum?id=GgX6dPJx9M
optimization_type: []
organizations:
- UC Irvine
presentation_type: oral
principles:
- approximate
- tier
problem: KV cache memory grows with context and generation length, limiting LLM serving
  throughput; naively evicting tokens degrades accuracy in long-generation tasks.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3838_zYgO11t.pdf
slug: flexicache-leveraging-temporal-stability-of-attention-heads-
status: under-review
title: 'FlexiCache: Leveraging Temporal Stability of Attention Heads for Efficient
  KV Cache Management'
topics:
- kv-cache
- sparse-attention
- cpu-offload
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3838
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
