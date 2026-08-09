---
agentic_models: []
arxiv_date: 2026-05
arxiv_url: https://arxiv.org/abs/2605.21603
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
citations: 0
citations_updated: '2026-07-31'
code_url: https://github.com/uw-syfi/DynaFlow
domain:
- llm-serving
- ml-compilers
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 1.29× throughput vs. unmodified baseline across 6 ML systems (including
  FlashAttention and vLLM) with minimal per-system code changes
models_evaluated: []
observations:
  pipeline: A single device runs memory-bound and compute-bound operators back to
    back, and overlapping them today means hand-rewriting model code per architecture
    and per hardware target.
official_category: ''
openreview_url: https://openreview.net/forum?id=i0yqC9954S
optimization_type: []
organizations:
- University of Washington
presentation_type: oral
principles: []
principles_review:
- pipeline
problem: Adding intra-device parallelism to ML frameworks requires invasive, model-specific
  code rewrites that don't generalize across architectures or hardware.
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
