---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Siqi Chen
- Ke Hong
- Tianchen Zhao
- Ruiqi Xie
- Zhenhua Zhu
- Xudong Zhang
- Yu Wang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 1.25× end-to-end and 1.40× attention speedup over Ulysses/Ring Attention
  sequence parallel methods for DiT inference with sparse attention on average
models_evaluated: []
observations:
  balance: Sparse imbalance ratio quantifies per-head and per-block sparsity variation
    that creates unequal work across SP workers; dual-level partitioning achieves
    near-perfect balance at both granularities.
  skip: DiT block-wise sparse attention produces irregular dense blocks unevenly across
    heads; db-SP routes blocks to workers by actual sparsity pattern rather than naive
    head or sequence splitting.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=XgKteNxNe0
organizations:
- Tsinghua University
presentation_type: oral
principles:
- balance
- skip
problem: Sequence parallelism for DiT inference creates severe workload imbalance
  because sparse attention density varies unpredictably across heads and blocks.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3798.pdf
slug: db-sp-accelerating-sparse-attention-for-visual-generative-mo
status: draft
title: 'db-SP: Accelerating Sparse Attention for Visual Generative Models with Dual-Balanced
  Sequence Parallelism'
topics:
- sparse-attention
- tensor-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3798
---

## Background

Diffusion Transformers (DiTs) use sparse attention at high resolution to avoid quadratic cost — skipping attention between image patches unlikely to interact. Unlike text models where sparsity is roughly uniform, DiT sparsity varies dramatically across heads and denoising steps: some heads are dense, others 90% sparse. Sequence parallelism splits attention work across GPUs by head or sequence dimension, but applied to uneven sparse patterns it creates severe load imbalance where GPUs assigned dense heads do far more work.

## Key Contributions

- **Sparse imbalance ratio**: formal metric that quantifies workload imbalance arising from uneven sparsity across attention heads and blocks when sequence parallelism is applied to DiT models
- **Dual-level partitioning**: assigns work at both the head dimension and the block dimension simultaneously, achieving near-perfect load balance even under irregular sparse attention masks with negligible runtime overhead
- **Dynamic parallel degree tuning**: adapts the parallelism split between head and block dimensions at runtime as the sparsity pattern evolves across denoising steps and transformer layers, avoiding static miscalibration
- **1.25× end-to-end / 1.40× attention speedup** over state-of-the-art sequence parallel methods on average across DiT inference workloads

## Trade-offs

- Dynamic parallel degree determination adds runtime overhead; the paper reports this as negligible, but in very short-sequence or low-sparsity regimes the overhead-to-benefit ratio may reverse.
- The approach is designed for block-wise sparse attention patterns; models using unstructured or token-level sparse attention may not exhibit the regular block sparsity that db-SP exploits.

## Nuances

- Speedup figures are averages across denoising steps and layers; peak improvements at high-sparsity steps will be larger than the mean, while dense early steps contribute minimal benefit.
- The dual-balance is evaluated for Ulysses-style (head-dimension) and Ring Attention (block-dimension) parallelism; hybrid parallelism strategies not covered by these two paradigms are not addressed.