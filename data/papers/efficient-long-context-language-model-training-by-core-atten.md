---
agentic_models: []
arxiv_date: 2025-10
arxiv_url: https://arxiv.org/abs/2510.18121
authors:
- Yonghao Zhuang
- Junda Chen
- Bo Pang
- Yi Gu
- Yibo Zhu
- Yimin Jiang
- Ion Stoica
- Hao Zhang
- Eric P. Xing
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
hardware:
- H200
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 1.9× training throughput over Megatron-LM and 1.35× over existing
  load-balancing methods at 512K context length on 512 H200 GPUs
models_evaluated: []
observations:
  balance: At 512K context, softmax(QKᵀ)V grows quadratically vs. near-linear for
    other ops; DistCA dispatches CA-tasks to dedicated attention servers, equalizing
    load and eliminating DP/PP stragglers.
  fuse: Rebatching CA-tasks at attention servers creates dense fused batches that
    sustain high kernel utilization, avoiding the low utilization of scattered small
    attention shards processed independently.
  pipeline: DistCA's ping-pong scheme overlaps CA communication with compute on host
    devices; attention servers process CA-task batches while hosts proceed with non-attention
    ops, eliminating idle time.
official_category: ''
openreview_url: https://openreview.net/forum?id=oIonqkc8hM
optimization_type: []
organizations:
- Carnegie Mellon University
- UC Berkeley
- NVIDIA
presentation_type: oral
principles:
- balance
- pipeline
- fuse
problem: At long context, attention grows quadratically while other ops grow linearly,
  creating stragglers that cap throughput across DP and PP groups.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3754.pdf
slug: efficient-long-context-language-model-training-by-core-atten
status: draft
title: Efficient Long-Context Language Model Training by Core Attention Disaggregation
topics:
- pipeline-parallelism
- tensor-parallelism
- communication-overlap
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3754
---

## Key Contributions

- **Core attention disaggregation (CAD)**: separates the parameter-free softmax(QKᵀ)V computation from the rest of the transformer and dispatches it to a dedicated pool of attention server devices, exploiting its statelessness (no trainable parameters, minimal transient state) and composability (attention kernels sustain high utilization on arbitrary-length batches)
- **DistCA system**: implements CAD with a ping-pong communication scheme that completely overlaps CA communication with compute, and uses in-place attention servers to improve memory utilization
- **Token-level CA-task scheduling**: dynamically partitions attention into token-level tasks and rebatches them at attention servers to equalize compute across the server pool, eliminating stragglers without sacrificing kernel efficiency
- **Scaling results**: 1.9× throughput improvement over Megatron-LM and 1.35× over existing load-balancing methods at 512K context length on 512 H200 GPUs; near-perfect compute and memory balance

## Trade-offs

- CAD requires dedicating a fraction of devices as attention servers, reducing the number of devices available for model-parallel training; the optimal server ratio depends on context length and model size.
- The ping-pong overlap scheme requires careful synchronization; if attention server latency exceeds the compute time of the host device's non-attention work, bubbles reappear.

## Nuances

- The 1.9× improvement over Megatron-LM is at 512K context; at shorter contexts, the attention/non-attention compute ratio shrinks and the benefit of disaggregation diminishes.
- CAD addresses the training-time compute imbalance; the attention disaggregation architecture is not directly applicable to inference, where KV cache management and decode batching present different bottlenecks.