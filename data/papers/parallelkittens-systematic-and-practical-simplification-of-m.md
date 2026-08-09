---
agentic_models: []
arxiv_date: 2025-11
arxiv_url: https://arxiv.org/abs/2511.13940
authors:
- Stuart H. Sul
- Simran Arora
- Benjamin F. Spector
- Christopher Ré
award: ''
citations: 9
citations_updated: '2026-07-31'
code_url: ''
domain:
- ml-kernels
hardware:
- H100
- NVIDIA Blackwell (B200)
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 4.08× speedup for sequence-parallel, 2.33× for data/tensor-parallel,
  and 1.22× for expert-parallel workloads with fewer than 50 lines of device code
models_evaluated: []
observations:
  pipeline: Every multi-GPU kernel alternates between moving data and computing on
    it, leaving the interconnect idle during compute and the tensor cores idle during
    transfers.
  simplify: Every workload (TP, SP, EP) had its own ad-hoc overlap kernel; finding
    that all share 8 underlying primitives let a single template outperform the specialized
    code by up to 4×.
official_category: ''
openreview_url: https://openreview.net/forum?id=Cv5e5uRXFb
optimization_type: []
organizations:
- Stanford University
presentation_type: oral
principles:
- pipeline
principles_review:
- simplify
problem: Inter-GPU communication bottlenecks AI workloads; existing overlap techniques
  fail to reach peak bandwidth across heterogeneous workloads and accelerators.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3845.pdf
slug: parallelkittens-systematic-and-practical-simplification-of-m
status: draft
title: 'ParallelKittens: Systematic and Practical Simplification of Multi-GPU AI Kernels'
topics:
- tensor-parallelism
- communication-overlap
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3845
---

## Key Contributions

- **ParallelKittens (PK) framework**: minimal CUDA extension of ThunderKittens exposing eight core multi-GPU primitives derived from a systematic analysis of data-transfer mechanisms, resource scheduling, and design overheads
- **Unified programming template**: single template captures the structure of optimal overlapped multi-GPU kernels; developers instantiate it for specific workloads in fewer than 50 lines of device code
- **Validated on Hopper and Blackwell**: achieves up to 4.08× speedup for sequence-parallel, 2.33× for data- and tensor-parallel, and 1.22× for expert-parallel workloads; generalization confirmed across both GPU generations
- Systematic derivation of the eight primitives from first principles makes the design approach transferable to new accelerators without ad-hoc operator-specific techniques

## Trade-offs

- The unified template is optimized for the dominant communication patterns; highly irregular or dynamic communication topologies (e.g., expert routing with variable loads) may require custom extensions beyond the eight primitives.
- Expert-parallel speedup (1.22×) is substantially lower than sequence-parallel (4.08×), reflecting that MoE communication patterns are less amenable to the current primitive set.
