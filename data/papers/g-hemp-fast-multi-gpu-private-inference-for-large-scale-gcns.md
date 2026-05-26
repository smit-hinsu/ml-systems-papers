---
slug: g-hemp-fast-multi-gpu-private-inference-for-large-scale-gcns
title: "G-HEMP: Fast Multi-GPU Private Inference for Large-Scale GCNs with Homomorphic Encryption"
authors:
- Ran Ran
- Zhaoting Gong
- Zhaowei Li
- Xianting Lu
- Jiajia Li
- Wujie Wen
organizations:
- North Carolina State University
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3811
openreview_url: https://openreview.net/forum?id=RSTrFSPIMy
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
- llm-serving
hardware:
- Multi-GPU (4-GPU system)
models_evaluated:
- Large-scale GCNs
agentic_models: []
topics: []
principles:
- cache
- balance
observations:
  cache: "Block-diagonal parallel packing eliminates redundant data replication in encrypted adjacency matrices, reducing HE operations by up to 4.41x over feature-wise packing."
  balance: "Multi-GPU workload partitioning halves per-GPU peak memory on 4-GPU systems, enabling larger graphs that exceed single GPU capacity."
problem: "Homomorphic encryption for private GCN inference on GPUs has excessive memory and redundant compute, preventing scaling to large real-world graphs."
key_results: "G-HEMP achieves 4.41x speedup over feature-wise packing and 3.88x latency improvement on 4-GPU vs single GPU, 3.13x gain vs Cinnamon on GCN inference."
---

## Key Contributions

- **Block-diagonal parallel packing**: Eliminates redundant data replication in HE-encrypted adjacency matrices, reducing the number of HE operations by up to 4.41x compared to conventional feature-wise packing.
- **Multi-GPU workload partitioning**: Splits encrypted GCN computation across GPUs with a partitioning policy that halves per-GPU peak memory on 4-GPU systems, achieving near-linear scaling.

## Trade-offs

- HE operations are still orders of magnitude slower than plaintext computation; G-HEMP improves HE GCN efficiency but does not approach plaintext performance.
- Block-diagonal packing is specific to graph-structured data; generalization to other HE workloads requires adapting the packing scheme.

## Nuances

- The 3.13x gain over Cinnamon comes from superior multi-device partition policy, not from algorithmic improvements to HE itself.
- G-HEMP is model-agnostic and scales with both graph size and GPU count, making it practical for recommendation systems and bioinformatics.
