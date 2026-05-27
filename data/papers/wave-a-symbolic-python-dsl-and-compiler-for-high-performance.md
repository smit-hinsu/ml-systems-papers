---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Harsh Menon
- Oleksandr Zinenko
- Gaurav Verma
- Stanley Winata
- Ivan Butygin
- Nithin Meganathan
- Sanket Pandit
- William Hatch
- Surya Jasper
- Megan Kuo
- Sahil Faizal
- Ashay Rane
- Aurore De Spirlet
- Martin Paul Lücke
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-kernels
hardware:
- NVIDIA GPU
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Wave matches or surpasses 2 leading baselines (Triton, CUTLASS) in kernel
  performance while eliminating manual matrix core address computation on NVIDIA GPUs
models_evaluated: []
observations:
  fuse: Wave's symbolic address computation automatically generates optimal tile addressing
    for matrix cores, avoiding manual indexing errors that cause excess global memory
    traffic in hand-written kernels.
  tier: Automated register and shared-memory address scheduling in Wave keeps operands
    in the fastest memory tiers throughout matrix core computation, without requiring
    manual tiling directives.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=gcXV1E8HRH
organizations:
- AMD
presentation_type: oral
principles:
- fuse
- tier
problem: GPU matrix cores require complex addressing schemes that are difficult to
  manage by hand, making high-performance kernel authoring error-prone and tedious.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3778_wPh602N.pdf
slug: wave-a-symbolic-python-dsl-and-compiler-for-high-performance
status: draft
title: 'Wave: A Symbolic Python DSL And Compiler for High-Performance Machine Learning'
topics:
- kernel-fusion
- autotuning
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3778
---

## Background

GPU matrix cores require precisely structured operand layouts in registers and shared memory: tiles must arrive in a specific arrangement, results must land at specific register locations, and the sequence must not stall the units. CUTLASS exposes these details directly, requiring intricate multi-level addressing where a single wrong index silently kills performance. Higher-level DSLs like Triton abstract some details but still require explicit tiling strategies and memory access patterns from the programmer.

## Key Contributions

- **Wave DSL**: a Python-embedded symbolic domain-specific language for kernel authoring that abstracts away matrix core addressing schemes; authors express core computations directly while the compiler handles tile address generation and scheduling.
- **Symbolic address computation**: automatically derives the intricate indexing patterns required by hardware matrix units (e.g., WMMA/MMA instructions), eliminating a major source of hand-written kernel bugs and performance cliffs.
- **Compiler backend**: lowers Wave's symbolic representation to hardware-specific code; targets GPU matrix cores and generates addressing that matches or surpasses hand-tuned kernels from state-of-the-art DSLs and libraries.
- Performance competitive with or better than leading kernel DSLs and libraries across evaluated workloads.

## Trade-offs

- Symbolic abstraction over hardware addressing may limit fine-grained control needed for extreme performance tuning in specific edge cases; expert kernel authors may still prefer low-level intrinsics for the final 1–2% of performance.
- The compiler's code generation quality is bounded by the symbolic representation's expressiveness; kernels requiring non-standard addressing patterns may require DSL extensions.

## Nuances

- The abstract does not specify which state-of-the-art DSLs or libraries are compared; the competitive baseline and evaluated workload types are not fully detailed.
- Wave targets GPU matrix cores specifically; its applicability to other accelerator architectures (TPUs, custom ASICs) is not addressed.