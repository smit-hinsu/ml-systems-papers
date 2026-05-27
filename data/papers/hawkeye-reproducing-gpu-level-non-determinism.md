---
slug: hawkeye-reproducing-gpu-level-non-determinism
title: "Hawkeye: Reproducing GPU-Level Non-Determinism"
authors:
- Erez Badash
- Dan Boneh
- Ilan Komargodski
- Megha Srivastava
organizations:
- Stanford University
- Duplex
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3829
optimization_type: []
openreview_url: https://openreview.net/forum?id=JnmgsTFQQv
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
- observability
hardware:
- NVIDIA GPU (Ampere, Hopper, Lovelace)
models_evaluated:
- ML model training and inference (FP16, BF16, FP8)
agentic_models: []
topics: []
principles:
- search-ai
observations:
  search-ai: "Systematic tests of rounding direction, subnormal handling, and accumulation order on Tensor Cores enable perfect CPU reproduction of GPU matrix multiplications for auditing."
problem: "GPU arithmetic non-determinism prevents verifiable reproduction of ML training and inference, blocking trustworthy third-party auditing of AI workloads."
key_results: "Hawkeye enables perfect CPU reproduction of NVIDIA Tensor Core matmul across Ampere, Hopper, and Lovelace for FP16, BF16, and FP8 without precision loss."
---

## Background

Floating-point arithmetic is not associative: GPU matmuls use massively parallel reduction trees whose accumulation order depends on undocumented, architecture-specific hardware details. The same model on different GPU generations (Ampere vs. Hopper) or precisions (FP16 vs. FP8) produces different bit patterns. For third-party ML auditing — verifying a model owner's reported outputs match declared weights — this non-determinism is a fundamental blocker: an auditor cannot reproduce the computation to check it without burdening the model owner with cryptographic overhead.

## Key Contributions

- **Hawkeye framework**: A systematic sequence of tests that characterizes NVIDIA Tensor Core behavior — rounding direction, subnormal number handling, and non-associative accumulation order — enabling exact CPU reproduction of GPU matrix multiplications.
- **Cross-architecture coverage**: Verified on Ampere, Hopper, and Lovelace GPUs across FP16, BF16, and FP8 precision types, with perfect reproduction in all test cases.

## Trade-offs

- CPU reproduction of GPU matmul is significantly slower than native GPU execution; Hawkeye is intended for auditing not production inference.
- The framework covers matrix multiplication only; other GPU operations (activations, reductions) are not characterized.

## Nuances

- Prior verifiable ML approaches either add compute overhead to the original model owner or suffer quality degradation; Hawkeye imposes no burden on the model owner.
- Non-associativity of floating-point accumulation is the key challenge — Hawkeye's tests determine the exact accumulation order used by each GPU architecture.
