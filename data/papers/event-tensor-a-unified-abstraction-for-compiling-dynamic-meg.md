---
agentic_models: []
arxiv_url: ''
authors:
- Hongyi Jin
- Bohan Hou
- Guanjie Wang
- Ruihang Lai
- Jinqi Chen
- Zihao Ye
- Yaxing Cai
- Yixin Dong
- Xinhao Cheng
- Zhihao Zhang
- Yilong Zhao
- Yingyi Huang
- Lijie Yang
- Jinchen Jiang
- Gabriele Oliaro
- Jianan Ji
- Xupeng Miao
- Vinod Grover
- Todd C. Mowry
- Zhihao Jia
- Tianqi Chen
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-compilers
- llm-serving
hardware:
- GPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: ETC matches the best LLM serving latency on GPU while cutting warmup
  overhead vs prior megakernels; supports 2 classes of dynamism (shape + data-dependent).
models_evaluated:
- LLM inference workloads
observations:
  cache: Persistent megakernel eliminates repeated kernel launch overhead and coarse
    synchronization barriers between fused operators.
  fuse: Fusing operators into a single persistent kernel eliminates intermediate tensor
    writes to global memory between consecutive ops in the LLM decode graph.
  pipeline: Event Tensor compiler exposes inter-kernel parallelism by encoding tiled
    task dependencies, enabling static and dynamic scheduling to overlap independent
    ops.
official_category: ''
openreview_url: https://openreview.net/forum?id=PJqFhAbUHa
organizations:
- Carnegie Mellon University
- NVIDIA
- University of Washington
- UC Berkeley
- Princeton University
- Purdue University
presentation_type: oral
principles:
- pipeline
- cache
- fuse
problem: Existing megakernel approaches eliminate kernel launch overhead but cannot
  handle dynamic shapes or data-dependent computation in real LLM workloads.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3815.pdf
slug: event-tensor-a-unified-abstraction-for-compiling-dynamic-meg
status: draft
title: 'Event Tensor: A Unified Abstraction for Compiling Dynamic Megakernel'
topics:
- kernel-fusion
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3815
---

## Background

A megakernel handles an entire forward pass as one persistent GPU kernel, eliminating launch overhead and keeping intermediate tensors in registers instead of HBM. Megakernels work well for static models, but LLM inference is dynamic: sequence lengths vary per request, speculative decoding produces data-dependent token counts, and MoE routing selects experts at runtime. Existing megakernel compilers assume shapes are fixed at compile time and break when a runtime decision changes a downstream tensor's shape.

## Key Contributions

- **Event Tensor abstraction**: Encodes dependencies between tiled tasks as first-class events, enabling megakernel compilation to support both shape-dependent and data-dependent dynamism in LLM workloads.
- **Event Tensor Compiler (ETC)**: Applies static and dynamic scheduling transformations on top of the Event Tensor IR to generate high-performance persistent kernels for real LLM inference workloads.

## Trade-offs

- The compiler must handle runtime dynamism (variable sequence lengths, conditional branches) which adds scheduling complexity over static megakernels.
- Compile times may be higher than simpler kernel fusion approaches due to the richer dependency representation.

## Nuances

- The key novelty over prior megakernels (e.g., FlashInfer persistent kernels) is first-class support for data-dependent execution paths, not just shape dynamism.
- Warmup overhead reduction is a secondary but important benefit for serving systems that need fast cold starts.