---
agentic_models: []
arxiv_url: ''
authors:
- Ran Ran
- Zhaoting Gong
- Zhaowei Li
- Xianting Lu
- Jiajia Li
- Wujie Wen
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-kernels
hardware:
- Multi-GPU (4-GPU system)
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: G-HEMP achieves 4.41x speedup over feature-wise packing and 3.88x latency
  improvement on 4-GPU vs single GPU, 3.13x gain vs Cinnamon on GCN inference.
models_evaluated:
- Large-scale GCNs
observations:
  balance: Multi-GPU workload partitioning halves per-GPU peak memory on 4-GPU systems,
    enabling larger graphs that exceed single GPU capacity.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=RSTrFSPIMy
organizations:
- North Carolina State University
presentation_type: oral
principles:
- balance
problem: Homomorphic encryption for private GCN inference on GPUs has excessive memory
  and redundant compute, preventing scaling to large real-world graphs.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3811.pdf
slug: g-hemp-fast-multi-gpu-private-inference-for-large-scale-gcns
status: draft
title: 'G-HEMP: Fast Multi-GPU Private Inference for Large-Scale GCNs with Homomorphic
  Encryption'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3811
---

## Background

Homomorphic encryption (HE) lets a server run inference on encrypted inputs without seeing the data, but HE arithmetic is orders of magnitude slower than plaintext. The main efficiency lever is **ciphertext packing**: several values share one ciphertext and amortize per-ciphertext overhead. Graph convolutional networks aggregate neighbor features through an encrypted adjacency matrix, where a bad packing choice forces redundant HE operations. Prior HE-GCN systems ran on one GPU only.

## Key Contributions

- **Block-diagonal parallel packing**: Eliminates redundant data replication in HE-encrypted adjacency matrices, reducing the number of HE operations by up to 4.41x compared to conventional feature-wise packing.
- **Multi-GPU workload partitioning**: Splits encrypted GCN computation across GPUs with a partitioning policy that halves per-GPU peak memory on 4-GPU systems, achieving near-linear scaling.

## Trade-offs

- HE operations are still orders of magnitude slower than plaintext computation; G-HEMP improves HE GCN efficiency but does not approach plaintext performance.
- Block-diagonal packing is specific to graph-structured data; generalization to other HE workloads requires adapting the packing scheme.

## Nuances

- The 3.13x gain over Cinnamon comes from superior multi-device partition policy, not from algorithmic improvements to HE itself.
- G-HEMP is model-agnostic and scales with both graph size and GPU count, making it practical for recommendation systems and bioinformatics.