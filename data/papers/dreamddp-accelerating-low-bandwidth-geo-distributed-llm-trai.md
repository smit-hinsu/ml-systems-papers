---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- zhenheng Tang
- Zichen TANG
- Junlin Huang
- Xinglin Pan
- Rudan Yan
- Yuxin Wang
- Amelie Chi Zhou
- Shaohuai Shi
- Xiaowen Chu
- Bo Li
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 1.49×–3.91× speedup over leading baseline methods on 32 GPUs with ResNet
  and GPT-2/Llama-2 in low-bandwidth geo-distributed settings
models_evaluated:
- GPT-2
- Llama-2
observations:
  pipeline: Layer-wise partial sync decouples gradient communication from the backward
    pass; non-synced layers' gradients overlap with compute rather than blocking on
    a cross-datacenter all-reduce.
  cache: Partial Local SGD syncs only layers whose staleness exceeds a threshold,
    skipping full-model communication each step and cutting total cross-datacenter
    bandwidth by an order of magnitude.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=cnvw0mbZQp
organizations:
- HKUST
- HKUST (Guangzhou)
presentation_type: oral
principles:
- pipeline
- cache
problem: Geo-distributed LLM training stalls on slow inter-datacenter links because
  Local SGD's strict model synchronization blocks compute-communication overlap.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: dreamddp-accelerating-low-bandwidth-geo-distributed-llm-trai
status: draft
title: 'DreamDDP: Accelerating Low-Bandwidth Geo-Distributed LLM Training with Layer-wise
  Partial Synchronization'
topics:
- pipeline-parallelism
- communication-overlap
- fsdp-zero
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3790
---

## Background

Geo-distributed LLM training spans GPU clusters across datacenters connected by links orders of magnitude slower than intra-datacenter InfiniBand (1–10 Gbps vs. 400 Gbps). Standard data parallelism all-reduces after every backward pass — too expensive across slow WAN links. Local SGD reduces synchronization frequency by letting clusters train independently for several steps, but its sync step still exchanges every parameter in the full model, consuming enormous bandwidth even infrequently and blocking compute while the sync completes.

## Key Contributions

- **Partial Local SGD**: extends Local SGD by synchronizing only a subset of layers per iteration rather than the full model; only layers whose local divergence exceeds a threshold are synchronized, with theoretical convergence guarantees comparable to S-SGD
- **Layer-wise comm-compute overlap**: schedules per-layer gradient synchronization to overlap with forward/backward computation of other layers using fine-grained profiling, eliminating the blocking all-reduce that prevents overlap in standard Local SGD
- **Memory-neutral overlap**: achieves communication overlap without allocating extra GPU memory for parameter buffers — a key requirement for LLM-scale training where memory is already near capacity
- **Fine-grained profiler**: identifies three scheduling properties (computation order, synchronization opportunity, communication priority) to optimally interleave layer-level gradient communication with compute
- **1.49×–3.91× speedup** over leading baselines (DiLoCo and similar) across ResNet-18/50, GPT-2, and Llama-2 on 32 GPUs in low-bandwidth settings

## Trade-offs

- Partial synchronization introduces bounded parameter staleness across data-center nodes; convergence proofs show comparable rates to S-SGD, but practical model quality at large scale requires careful hyperparameter tuning of the synchronization frequency.
- Layer-wise profiling adds initialization overhead and must be re-run when model architecture or batch size changes.

## Nuances

- Evaluation uses 32 GPUs emulating geo-distributed low-bandwidth conditions; actual multi-datacenter deployments may exhibit more variable and bursty inter-link congestion not captured by the benchmark setup.
- The convergence guarantee is for the same theoretical rate as S-SGD, but matching S-SGD's final accuracy in practice requires tuning the partial synchronization schedule — a practical gap the abstract does not quantify.
