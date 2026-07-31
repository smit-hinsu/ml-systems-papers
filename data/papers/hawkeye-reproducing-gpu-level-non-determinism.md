---
agentic_models: []
arxiv_date: 2026-03
arxiv_url: https://arxiv.org/abs/2603.20421
authors:
- Erez Badash
- Dan Boneh
- Ilan Komargodski
- Megha Srivastava
award: ''
citations: 1
citations_updated: '2026-07-31'
code_url: ''
domain:
- observability
- hardware
hardware:
- NVIDIA GPU (Ampere, Hopper, Lovelace)
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Hawkeye enables perfect CPU reproduction of NVIDIA Tensor Core matmul
  across Ampere, Hopper, and Lovelace for FP16, BF16, and FP8 without precision loss.
models_evaluated:
- ML model training and inference (FP16, BF16, FP8)
observations:
  measure: An auditor rerunning a model gets different bits than the owner reported
    and cannot separate fraud from Tensor Core accumulation order, which NVIDIA
    documents nowhere.
  search-ai: Systematic tests of rounding direction, subnormal handling, and accumulation
    order on Tensor Cores enable perfect CPU reproduction of GPU matrix multiplications
    for auditing.
official_category: ''
openreview_url: https://openreview.net/forum?id=JnmgsTFQQv
optimization_type: []
organizations:
- Stanford University
- Duplex
presentation_type: oral
principles:
- search-ai
- measure
problem: GPU arithmetic non-determinism prevents verifiable reproduction of ML training
  and inference, blocking trustworthy third-party auditing of AI workloads.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: hawkeye-reproducing-gpu-level-non-determinism
status: draft
title: 'Hawkeye: Reproducing GPU-Level Non-Determinism'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3829
---

## Background

Third-party ML auditing asks whether a model owner's reported outputs really came from the declared weights. Rerunning the computation is the cheapest check, but GPU matmuls accumulate in an undocumented, architecture-specific order, so the same model emits different bit patterns on Ampere vs. Hopper, or FP16 vs. FP8. Existing verifiable-ML schemes route around this with cryptographic machinery the model owner has to pay for.

## Key Contributions

- **Hawkeye framework**: A systematic sequence of tests that characterizes NVIDIA Tensor Core behavior — rounding direction, subnormal number handling, and non-associative accumulation order — enabling exact CPU reproduction of GPU matrix multiplications.
- **Cross-architecture coverage**: Verified on Ampere, Hopper, and Lovelace GPUs across FP16, BF16, and FP8 precision types, with perfect reproduction in all test cases.

## Trade-offs

- CPU reproduction of GPU matmul is significantly slower than native GPU execution; Hawkeye is intended for auditing not production inference.
- The framework covers matrix multiplication only; other GPU operations (activations, reductions) are not characterized.

## Nuances

- Prior verifiable ML approaches either add compute overhead to the original model owner or suffer quality degradation; Hawkeye imposes no burden on the model owner.
- Non-associativity of floating-point accumulation is the key challenge — Hawkeye's tests determine the exact accumulation order used by each GPU architecture.
