---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Yi Pan
- Yile Gu
- Jinbin Luo
- Yibo Wu
- Ziren Wang
- Hongtao Zhang
- Ziyi Xu
- Shengkai Lin
- Baris Kasikci
- Stephanie Wang
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/uw-syfi/DynaFlow
domain:
- llm-serving
- ml-compilers
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 1.29× throughput vs. unmodified baseline across 6 ML systems
  (including FlashAttention and vLLM) with minimal per-system code changes
models_evaluated: []
observations:
  pipeline: DynaFlow's scheduler overlaps memory-bound and compute-bound operators
    without model-specific code, achieving up to 1.29× throughput across 6 ML
    systems including vLLM and FlashAttention.
  cache: DynaFlow's custom memory manager eliminates copy overheads from async
    control/data-flow that naive async execution introduces as redundant intermediate
    buffers between concurrent operators.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=i0yqC9954S
organizations:
- University of Washington
presentation_type: oral
principles:
- pipeline
- cache
problem: Adding intra-device parallelism to ML frameworks requires invasive,
  model-specific code rewrites that don't generalize across architectures or hardware.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: dynaflow-transparent-and-flexible-intra-device-parallelism-v
status: draft
title: 'DynaFlow: Transparent and Flexible Intra-Device Parallelism via Programmable
  Operator Scheduling'
topics:
- pipeline-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3771
---

## Background

A single GPU has multiple independent engines — tensor cores, copy engines, separate SM partitions — that can run concurrently. Overlapping memory-bound operators (KV cache loads) with compute-bound operators (matmuls) on the same device improves utilization, but ML frameworks serialize operators by default. Adding this intra-device overlap to an existing system like vLLM or FlashAttention requires invasive, model-specific rewrites — work that must be repeated from scratch for each framework and doesn't generalize.

## Key Contributions

- **DynaFlow abstraction**: decouples logical model definition from physical execution schedule via a flexible frontend with graph partitioning annotations and a programmable intra-device parallelism interface — developers describe strategies declaratively rather than rewriting model code
- **Asynchronous backend**: manages complex control/data-flow asynchronously using custom memory management that eliminates copy overheads from async execution; preserves compatibility with CUDA Graphs and TorchInductor
- **Cross-system integration**: integrates representative intra-device parallelism strategies into 6 state-of-the-art ML systems with minimal code changes per system, achieving up to 1.29× throughput improvement
- **Strategy sensitivity handling**: the programmable interface enables the same DynaFlow backend to express multiple parallelism strategies that adapt to different execution contexts (workload size, model architecture, hardware)

## Trade-offs

- The annotation layer requires developers to mark graph partitioning boundaries and declare parallelism strategies; this is simpler than full custom implementations, but not fully automatic — some ML expertise is still required.
- Compatibility with CUDA Graphs is preserved, but complex dynamic shapes or data-dependent operators may limit which kernels can be fused or overlapped within DynaFlow's scheduling framework.

## Nuances

- The 1.29× speedup is the upper bound reported across 6 systems; average improvement across all systems and workloads is not specified in the abstract.
- DynaFlow targets intra-device (single GPU/accelerator) parallelism; multi-device tensor or pipeline parallelism are complementary dimensions not addressed.
