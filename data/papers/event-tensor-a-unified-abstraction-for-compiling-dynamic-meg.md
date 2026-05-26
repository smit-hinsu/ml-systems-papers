---
slug: event-tensor-a-unified-abstraction-for-compiling-dynamic-meg
title: "Event Tensor: A Unified Abstraction for Compiling Dynamic Megakernel"
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
organizations:
- Carnegie Mellon University
- NVIDIA
- University of Washington
- UC Berkeley
- Princeton University
- Purdue University
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3815
openreview_url: https://openreview.net/forum?id=PJqFhAbUHa
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
- ml-compilers
- llm-serving
hardware:
- GPU
models_evaluated:
- LLM inference workloads
agentic_models: []
topics:
- kernel-fusion
principles:
- pipeline
- cache
- fuse
observations:
  pipeline: "Event Tensor compiler exposes inter-kernel parallelism by encoding tiled task dependencies, enabling static and dynamic scheduling to overlap independent ops."
  cache: "Persistent megakernel eliminates repeated kernel launch overhead and coarse synchronization barriers between fused operators."
  fuse: "Fusing operators into a single persistent kernel eliminates intermediate tensor writes to global memory between consecutive ops in the LLM decode graph."
problem: "Existing megakernel approaches eliminate kernel launch overhead but cannot handle dynamic shapes or data-dependent computation in real LLM workloads."
key_results: "ETC matches the best LLM serving latency on GPU while cutting warmup overhead vs prior megakernels; supports 2 classes of dynamism (shape + data-dependent)."
---

## Key Contributions

- **Event Tensor abstraction**: Encodes dependencies between tiled tasks as first-class events, enabling megakernel compilation to support both shape-dependent and data-dependent dynamism in LLM workloads.
- **Event Tensor Compiler (ETC)**: Applies static and dynamic scheduling transformations on top of the Event Tensor IR to generate high-performance persistent kernels for real LLM inference workloads.

## Trade-offs

- The compiler must handle runtime dynamism (variable sequence lengths, conditional branches) which adds scheduling complexity over static megakernels.
- Compile times may be higher than simpler kernel fusion approaches due to the richer dependency representation.

## Nuances

- The key novelty over prior megakernels (e.g., FlashInfer persistent kernels) is first-class support for data-dependent execution paths, not just shape dynamism.
- Warmup overhead reduction is a secondary but important benefit for serving systems that need fast cold starts.
