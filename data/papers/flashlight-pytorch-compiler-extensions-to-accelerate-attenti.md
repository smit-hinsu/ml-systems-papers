---
agentic_models: []
arxiv_date: 2025-11
arxiv_url: https://arxiv.org/abs/2511.02043
authors:
- Bozhi You
- Irene Wang
- Zelal Su Mustafaoglu
- Abhinav Jangda
- Angélica Moreira
- Roshan Dathathri
- Divya Mahajan
- Keshav Pingali
award: ''
citations: 1
citations_updated: '2026-07-31'
code_url: ''
domain:
- ml-compilers
- ml-kernels
hardware:
- H100
- A100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 1.48× over FlexAttention on H100/A100; 5× for Evoformer; 6–9% end-to-end
  latency reduction for AlphaFold2 row/column-wise attention.
models_evaluated:
- LLaMA-3.2-1B
observations:
  fuse: TorchInductor treats a GEMM as a fusion barrier, so every new attention variant
    writes its score matrix out to HBM and reads it back unless someone hand-writes
    a kernel for it.
official_category: ''
openreview_url: https://openreview.net/forum?id=lboOMA8XWr
optimization_type: []
organizations:
- UT Austin
- Georgia Tech
- Microsoft
presentation_type: oral
principles:
- fuse
problem: New attention variants require hand-written specialized kernels; FlexAttention
  covers only a subset via rigid static templates, blocking rapid exploration.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3763_pOXWfhT.pdf
slug: flashlight-pytorch-compiler-extensions-to-accelerate-attenti
status: under-review
title: 'Flashlight: PyTorch Compiler Extensions to Accelerate Attention Variants'
topics:
- kernel-fusion
- autotuning
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3763
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
