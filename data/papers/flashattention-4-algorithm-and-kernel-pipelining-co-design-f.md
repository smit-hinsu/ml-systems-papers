---
slug: flashattention-4-algorithm-and-kernel-pipelining-co-design-f
title: "FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling"
authors:
- Ted Zadouri
- Markus Hoehnerbach
- Jay Shah
- Vijay Thakkar
- Tri Dao
organizations:
- Princeton University
- RWTH Aachen University
- Colfax International
- NVIDIA
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3759
openreview_url: https://openreview.net/forum?id=mN5RtvuYl3
arxiv_url: ''
presentation_type: oral
official_category: ''
award: ''
status: draft
reading_status: want-to-read
research_or_industry: research
indexed_by: smithinsu
indexed_date: '2026-05-24'
citations: null
citations_updated: ''
code_url: ''
project_url: ''
slides_url: ''
domain:
- ml-kernels
- llm-serving
hardware:
- NVIDIA B200
- NVIDIA GB200
models_evaluated:
- Transformer attention (BF16)
agentic_models: []
topics:
- kernel-fusion
principles:
- pipeline
- fuse
observations:
  pipeline: "Fully asynchronous MMA pipelines with larger tile sizes overlap tensor core compute with memory operations, exploiting B200's doubled MMA throughput."
  fuse: "Tensor memory acceleration and 2-CTA MMA mode cut shared memory traffic and eliminate atomic adds in the backward pass."
problem: "Blackwell GPUs double tensor core throughput but other units scale slower, making Hopper-era attention kernels bottlenecked by non-matmul ops on B200."
key_results: "FlashAttention-4 achieves 1613 TFLOPs/s (71% utilization) on B200 BF16, 1.3x over cuDNN 9.13 and 2.7x over Triton."
---

## Background

FlashAttention (v1–v3) fused attention into a tiled shared-memory kernel tuned for Hopper (H100). NVIDIA's Blackwell (B200/GB200) doubles tensor core throughput but shared memory bandwidth and softmax instruction throughput do not scale proportionally. This asymmetric scaling makes non-matmul operations and synchronization the new bottlenecks — Hopper-era assumptions break, and a kernel designed around Blackwell's actual unit balance is needed.

## Key Contributions

- **Asymmetric hardware co-design**: Redesigned pipelines exploiting B200's fully asynchronous MMA and larger tiles, addressing the bottleneck shift when tensor cores scale 2x but shared memory bandwidth does not.
- **Software-emulated exponential and conditional softmax**: Reduces non-matmul operations that are not accelerated by Blackwell's doubled tensor core throughput.
- **CuTe-DSL Python implementation**: FlashAttention-4 implemented entirely in Python-embedded CuTe-DSL, achieving 20-30x faster compile times vs C++ template approaches with no expressivity loss.

## Trade-offs

- The Blackwell-specific optimizations (2-CTA MMA, tensor memory) do not directly transfer to Hopper H100; this is a Blackwell-targeted implementation.
- Larger tile sizes require more shared memory and may reduce occupancy on smaller GPU configurations.

## Nuances

- The 71% hardware utilization is exceptional for attention, which is memory-bandwidth-bound on older hardware; Blackwell's architectural changes shift this balance.
- CuTe-DSL Python implementation is a secondary contribution enabling faster iteration but the performance claims are about the compiled kernel output.
