---
title: 'Flashlight: PyTorch Compiler Extensions to Accelerate Attention Variants'
slug: flashlight-pytorch-compiler-extensions-to-accelerate-attenti
authors:
- Bozhi You
- Irene Wang
- Zelal Su Mustafaoglu
- Abhinav Jangda
- Angélica Moreira
- Roshan Dathathri
- Divya Mahajan
- Keshav Pingali
organizations:
- UT Austin
- Georgia Tech
- Microsoft
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3763
openreview_url: https://openreview.net/forum?id=lboOMA8XWr
arxiv_url: https://arxiv.org/abs/2511.02043
slides_url: ''
code_url: ''
project_url: ''
official_category: ''
presentation_type: oral
award: ''
arxiv_date: '2025-11'
domain:
- ml-compilers
- ml-kernels
topics:
- kernel-fusion
- autotuning
principles:
- fuse
- tier
observations:
  fuse: Structural fusion with dimension demotion eliminates intermediate HBM tensor writes by merging GEMM output with dependent operations in a single fused kernel, avoiding a full round-trip.
  tier: Semantic fusion via algebraic transformation rewrites multi-pass reductions like stable softmax into single-pass online algorithms, keeping partial results in registers.
hardware:
- H100
- A100
models_evaluated:
- LLaMA-3.2-1B
agentic_models: []
citations: null
citations_updated: ''
research_or_industry: research
problem: New attention variants require hand-written specialized kernels; FlexAttention covers only a subset via rigid static templates, blocking rapid exploration.
key_results: Up to 1.48× over FlexAttention on H100/A100; 5× for Evoformer; 6–9% end-to-end latency reduction for AlphaFold2 row/column-wise attention.
status: under-review
reading_status: want-to-read
indexed_by: smithinsu
indexed_date: '2026-05-25'
---

## Key Contributions

- **Unified Reduction IR**: Represents matrix multiplications as generalized reductions inside TorchInductor, breaking the hard boundary between GEMMs and surrounding elementwise operations that previously blocked cross-operation fusion
- **Structural Fusion with Dimension Demotion**: Converts a parallel output dimension of a producer kernel into a reduction dimension of the fused kernel, trading a small amount of thread-level parallelism to eliminate an intermediate HBM write
- **Semantic Fusion via Algebraic Transformation**: Automatically detects homomorphism properties and rewrites dependent multi-stage reductions (e.g., two-pass stable softmax) into equivalent single-pass online algorithms, enabling fusion without correctness loss
- **FlexAttention superset coverage**: Handles all variants expressible in FlexAttention plus data-dependent formulations such as Evoformer and gated row/column-wise self-attention that FlexAttention cannot represent

## Trade-offs

- Dimension demotion reduces thread-level parallelism within the fused kernel; net benefit only materializes when memory bandwidth savings outweigh the occupancy reduction.
- Compilation adds JIT overhead on first use; latency-sensitive deployments require pre-warming the TorchInductor compilation cache.

## Nuances

- Experiments cap SM frequency (H100 at 1290 MHz, A100 at 1080 MHz) to reduce measurement variance; absolute throughput numbers are below production-tuned configurations.
- The 5× Evoformer improvement is on a variant unsupported by FlexAttention; for variants both systems handle, margins are closer to 1–1.48×.
- The paper uses anonymous authors in arXiv HTML (review artifact); published version restores author names.
