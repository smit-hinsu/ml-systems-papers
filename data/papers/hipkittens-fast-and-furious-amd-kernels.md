---
agentic_models: []
arxiv_date: ''
arxiv_url: 'https://arxiv.org/abs/2511.08083'
authors:
- William Hu
- Drew Wadsworth
- Sean Siddens
- Stanley Winata
- Daniel Y. Fu
- Ryan Swann
- Muhammad Osama
- Christopher Ré
- Simran Arora
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/HazyResearch/HipKittens
domain:
- ml-kernels
hardware:
- AMD CDNA3
- AMD CDNA4
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 1.2–2.4× over all baselines for d=64 attention, GQA non-causal backward,
  and memory-bound kernels on AMD CDNA3/CDNA4; matches hand-optimized assembly for
  GEMM
models_evaluated: []
observations:
  fuse: HipKittens' tile-based primitives group data into hardware-aligned tiles,
    reducing redundant global memory transactions and maximizing L2 reuse on AMD CDNA
    GPUs without hand-written assembly.
  tier: Explicit tile-based programming exposes CDNA's LDS and cache hierarchy, enabling
    data reuse patterns that compiler auto-vectorization misses for attention and
    GEMM kernels on AMD hardware.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=xxSSrndQrI
organizations:
- Stanford University
- AMD
- UC San Diego
presentation_type: oral
principles:
- fuse
- tier
problem: Peak-performance AMD GPU kernels required hand-written assembly; no high-level
  DSL existed for AMD CDNA hardware, blocking efficient AI kernel development.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3735.pdf
slug: hipkittens-fast-and-furious-amd-kernels
status: draft
title: 'HipKittens: Fast and Furious AMD Kernels'
topics:
- attention-kernels
- kernel-fusion
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3735
---

## Background

ThunderKittens introduced a C++ tile-based DSL for NVIDIA GPUs that exposes the memory hierarchy and wavefront scheduling without hand-written assembly. AMD's CDNA GPUs (MI300X and successors) are gaining datacenter adoption, but the ROCm stack lacked an equivalent: engineers tolerated compiler-auto-vectorized code or wrote low-level HIP approaching assembly complexity. Porting high-performance attention and GEMM kernels from NVIDIA to AMD required substantial per-kernel effort, fragile across AMD generations.

## Key Contributions

- **HipKittens (HK) programming framework**: A C++ tile-based DSL for AMD GPUs that ports the ThunderKittens abstractions (explicit tile management, asynchronous execution, fine-grained worker control) to the AMD HIP/ROCm stack with AMD-specific algorithm redesigns.
- **AMD-specific algorithm adaptations**: While tile-based abstractions generalize from NVIDIA to AMD, the underlying algorithms (e.g., attention tiling strategies, GEMM scheduling) must be rethought for AMD's CDNA memory subsystem and wavefront execution model.
- **Performance on CDNA3/CDNA4**: HK kernels match AMD's hand-optimized assembly for GEMM and attention, and outperform compiler baselines by 1.2–2.4× for attention (d=64), GQA non-causal backward, and memory-bound kernels where no assembly baseline exists.
- **Production deployment**: HipKittens is productionalized in the AMD AITER inference library, confirming practical viability beyond benchmarks.

## Trade-offs

- AMD-specific algorithm redesigns mean HipKittens kernels cannot be directly ported from ThunderKittens without implementation work; the abstraction layer is shared but the algorithmic instantiation diverges.
- The DSL does not cover all AMD workloads; sparse operations and custom reduction patterns may still require raw HIP or assembly for peak performance.

## Nuances

- Assembly remains difficult to scale across the breadth of AI workloads; HK's advantage is most pronounced precisely where assembly coverage is sparse (e.g., GQA non-causal backward).
- CDNA4 results demonstrate the framework generalizes across AMD generations, but re-tuning tile sizes and wavefront parameters is still required per generation.