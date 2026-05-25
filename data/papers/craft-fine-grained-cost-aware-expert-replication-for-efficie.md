---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2603.28768
authors:
- Adrian Zhao
- Zhenkun Cai
- Zhenyu Song
- Lingfan Yu
- Haozheng Fan
- Jun Wu
- Yida Wang
- Nandita Vijaykumar
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware:
- NVIDIA A100
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 1.14× average (up to 1.2×) goodput over EPLB baseline on DeepSeek-R1-671B
  and Kimi-K2-1000B; 29% avg TTFT reduction using 7.5× fewer replicas on A100 clusters.
models_evaluated:
- DeepSeek-R1-671B
- Kimi-K2-1000B
observations:
  exploit-sparsity: Per-layer MoE load skew follows a heavy-tail distribution; CRAFT
    skips replication for the majority of low-skew layers, targeting only the sparse
    tail where imbalance exceeds replication cost.
  balance-utilization: MoE load is skewed per-layer — one expert can get 10× average
    load while others are balanced; uniform replication wastes HBM on low-skew layers
    that gain nothing from it.
  exploit-memory-hierarchy: Reducing total replicas via fine-grained allocation frees
    GPU HBM for a larger KV cache, which improves decode throughput enough to offset
    the slightly lower expert load balance.
official_category: ''
openreview_url: https://openreview.net/forum?id=zdRvzU9ZCe
organizations:
- University of Toronto
- Amazon
presentation_type: oral
principles:
- exploit-sparsity
- balance-utilization
- exploit-memory-hierarchy
problem: Expert parallelism creates token-level load imbalance; uniform replication
  over-replicates balanced MoE layers, wasting HBM that could serve more KV cache.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3731_3lg6KXh.pdf
slug: craft-fine-grained-cost-aware-expert-replication-for-efficie
status: draft
title: 'CRAFT: Fine-Grained Cost-Aware Expert Replication For Efficient Mixture-of-Experts
  Serving'
topics:
- moe
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3731
---

## Key Contributions

- **Layer-wise benefit estimation**: For each MoE layer, CRAFT computes an L×K benefit matrix measuring load-balancedness gain for each of K=log₂D+1 possible replica counts, using offline expert load distributions; this exposes that high-skew layers benefit greatly from replication while low-skew layers do not.
- **Multiple-Choice Knapsack optimizer**: Formulates per-layer replica allocation as a knapsack problem — one replica count per layer, total replica budget as capacity, cumulative balancedness gain as value — solved with dynamic programming to maximize load balance under a memory constraint.
- **Automatic replication-factor selection**: Identifies the per-layer replica count at the knee of the diminishing-returns curve (highest per-replica balancedness gain) as the default choice, without requiring user-specified targets.
- Seamlessly integrates into existing MoE serving frameworks with no model weight changes or additional training; evaluated on 6–12 node A100 clusters serving DeepSeek-R1-671B and Kimi-K2-1000B.

## Trade-offs

- CRAFT requires an offline profiling phase to collect per-layer expert load distributions; results may not generalize across datasets with different routing patterns, requiring re-profiling when traffic changes significantly.
- Reducing total replicas frees KV cache memory, but on small clusters this trade-off is more favorable than on large clusters where expert placement itself becomes the binding constraint.

## Nuances

- The ~10-second initialization overhead for computing the allocation is negligible for long-running serving jobs but may matter for cold-start latency in short-lived deployments.
- CRAFT is evaluated on AWS p4de instances (A100 80GB with NVLink + EFA); different interconnect topologies (e.g., InfiniBand vs EFA) could change the communication-compute balance and alter optimal replication counts.
- Expert load distributions are measured offline from a representative dataset; for models with strong routing sensitivity to input domain (e.g., code vs. math), production traffic shifts could degrade allocation quality between re-profiling windows.