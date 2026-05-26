---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2512.01278
arxiv_date: '2025-12'
authors:
- Yilong Zhao
- Jiaming Tang
- Kan Zhu
- Zihao Ye
- Chi-Chih Chang
- Chaofan Lin
- Jongseok Park
- Guangxuan Xiao
- Mohamed S. Abdelfattah
- Mingyu Gao
- Baris Kasikci
- Song Han
- Ion Stoica
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
organizations:
- MIT
- UC Berkeley
- University of Michigan
- Tsinghua University
hardware:
- H100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 2.13× throughput over vLLM on H100 for long-CoT reasoning models;
  3.29× attention latency reduction via PillarAttn sparse drafting
models_evaluated: []
observations:
  skip: PillarAttn reuses verification-phase attention scores to select
    critical tokens at zero overhead; top-k filtering identifies the sparse set
    that preserves accuracy across reasoning steps.
  cache: Suffix-tree-based sparse attention draft reuses the sparsity
    pattern identified during the previous verification step, avoiding redundant full-attention
    computation during drafting phases.
  pipeline: Delayed verification decouples CPU metadata preparation
    from the critical GPU path by deferring it one iteration, enabling asynchronous
    CPU-GPU execution that hides verification overhead.
  tier: Dynamic KV-cache offloads chunks to host memory asynchronously
    overlapped with GPU compute, bounding peak GPU memory use without stalling inference.
official_category: ''
openreview_url: https://openreview.net/forum?id=yeqrwcWjPu
presentation_type: oral
principles:
- skip
- cache
- pipeline
- tier
problem: Long CoT reasoning shifts inference from compute-bound to memory-bound; each
  decoding step reads a growing KV-cache that bottlenecks throughput on H100s.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: accelerating-large-scale-reasoning-model-inference-with-spar
status: under-review
title: Accelerating Large-Scale Reasoning Model Inference with Sparse Self-Speculative
  Decoding
topics:
- speculative-decoding
- sparse-attention
- kv-cache
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3733
---

## Key Contributions

- **SpecGen framework**: self-speculative decoding that uses the same model as both draft and target, eliminating the need to maintain a separate smaller draft model while achieving 2.13× throughput over vLLM on long-chain-of-thought workloads
- **PillarAttn sparse draft attention**: selectively attends only to critical tokens identified by reusing attention score dumps from the preceding verification stage; zero-overhead sparsity identification via top-k filtering of averaged scores, achieving 3.29× attention latency reduction
- **Unified batch scheduler**: greedy bin-packing assigns requests into k draft-phase buckets to mix drafting and verification requests, sustaining high GPU utilization across fluctuating workloads via a fused sparse+full attention kernel
- **Delayed verification**: postpones CPU verification metadata by one iteration to fully decouple CPU overhead from GPU critical path, enabling asynchronous execution for non-verification requests
- **Dynamic KV-cache management**: offloads KV chunks to host memory asynchronously overlapped with computation, bounding GPU memory pressure to allow larger effective batch sizes

## Trade-offs

- PillarAttn reuses sparsity patterns from the previous verification step; for highly dynamic reasoning tasks where attention patterns shift rapidly, the reused pattern may lag and reduce acceptance rate.
- Dynamic host-memory offload adds PCIe bandwidth pressure; systems with slow CPU-GPU interconnects may see diminishing returns.

## Nuances

- Results are measured on H100 DGX-SXM5 servers with TP1/2/4; smaller GPU clusters or older hardware may show different bottleneck profiles.
- Self-speculation requires the draft and target to be the same model; heterogeneous draft/target setups (e.g., quantized draft) are not evaluated.
