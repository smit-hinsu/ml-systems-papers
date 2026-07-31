---
agentic_models: []
arxiv_date: ''
arxiv_url: 'https://arxiv.org/abs/2510.18830'
authors:
- Wenxuan Li
- Chengruidong Zhang
- Huiqiang Jiang
- Yucheng Li
- Yuqing Yang
- Lili Qiu
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/microsoft/MInference/tree/main/mtraining
domain:
- llm-training
hardware:
- A100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 6× training throughput improvement expanding context from 32K/128K
  to 512K tokens on 32× A100 GPUs while preserving model accuracy on RULER and NIAH
models_evaluated:
- Qwen2.5-3B
- Llama-3.1-8B
observations:
  balance: Balanced sparse ring attention partitions tokens so each worker gets equal
    compute load despite variable patterns; hierarchical ring attention reduces cross-node
    communication at 512K context.
  skip: Dynamic sparse attention skips computation for unimportant token pairs; a
    distributed index approximation makes sparsity patterns available across ring-attention
    workers without full synchronization.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=h6SD2zgwGq
organizations:
- Microsoft
- University of Cambridge
- University of Surrey
presentation_type: oral
principles:
- skip
- balance
problem: Dynamic sparse attention for ultra-long context training causes worker- and
  step-level load imbalance in distributed settings, negating its compute savings.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3775_6HYrxML.pdf
slug: mtraining-distributed-dynamic-sparse-attention-for-efficient
status: draft
title: 'MTraining: Distributed Dynamic Sparse Attention for Efficient Ultra-Long Context
  Training'
topics:
- sparse-attention
- communication-overlap
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3775
---

## Key Contributions

- **Distributed sparse index approximation**: computes sparse attention patterns in a distributed-friendly manner, making sparsity indices available across ring-attention workers without requiring full synchronization of attention scores
- **Balanced sparse ring attention**: partitions token sequences across workers so that the number of active (non-sparse) attention operations is equalized, eliminating per-step load imbalance that arises from variable routing patterns
- **Hierarchical sparse ring attention**: two-level ring topology reduces inter-node communication at extreme sequence lengths (512K), keeping cross-node data movement sub-linear in sequence length
- Extends Qwen2.5-3B and Llama-3.1-8B context from 32K/128K to 512K on 32 A100 GPUs with up to 6× throughput improvement; evaluated on RULER, PG-19, InfiniteBench, and NIAH

## Trade-offs

- Sparse index approximation introduces approximation error in sparsity pattern selection; rare long-range dependencies may be missed if their attention scores are underestimated during the approximation step.
- Balanced partitioning requires knowledge of the sparse pattern before assigning tokens to workers; this creates a chicken-and-egg dependency that the approximation algorithm resolves with some overhead.