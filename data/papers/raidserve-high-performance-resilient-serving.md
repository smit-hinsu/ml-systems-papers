---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Ziyi Xu
- Zhiqiang Xie
- Swapnil Gandhi
- Christos Kozyrakis
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware:
- H100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 'Up to 2× throughput and 100× faster recovery vs. standard fault-handling on 8×H100 DGX under multiple GPU failures'
models_evaluated: []
observations:
  balance: A GPU failure leaves survivors holding uneven KV cache and attention work,
    so the overloaded rank becomes a straggler the rest of the TP group waits on every
    step.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=5pl9fdbEkq
organizations:
- Stanford University
presentation_type: oral
principles:
- balance
problem: 'TP LLM serving fails on single GPU fault — halts execution, forces full KVCache recompute, and leaves surviving GPUs compute/memory imbalanced.'
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: raidserve-high-performance-resilient-serving
status: draft
title: 'RaidServe: High-performance Resilient Serving'
topics:
- tensor-parallelism
- kv-cache
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3856
---

## Key Contributions

- **Cyclic KVCache Placement**: distributes KV cache blocks cyclically across GPUs to maintain even memory utilization after a GPU failure, preventing memory hotspots on surviving nodes
- **Hybrid Attention**: combines tensor-parallel and data-parallel attention to eliminate attention stragglers under irregular GPU availability; adapts attention execution strategy to current cluster state
- **Fine-Grained Load-Aware Routing**: dynamically balances requests across healthy GPUs based on real-time load; compensates for reduced capacity after failures without pipeline stalls
- **Proactive KVCache backup + on-demand weight recovery**: backs up KV state before failure events and recovers weights on-demand, avoiding the 100×+ overhead of full KVCache recomputation used by standard methods
- Implemented as a lightweight serving engine compatible with existing TP infrastructures; evaluated on 8×H100 DGX with multiple simultaneous GPU failures

## Trade-offs

- Proactive KVCache backup consumes additional GPU memory for redundancy; the memory overhead trades off against recovery speed.
- Hybrid attention introduces architectural complexity; the overhead of switching between TP and DP attention modes adds latency in fault-free execution.

## Nuances

- The 2× throughput and 100× recovery speedup are measured under failure conditions; fault-free overhead from the backup mechanism is not independently characterized in the abstract.
- Evaluation is limited to 8×H100 DGX (single node); multi-node TP across InfiniBand fabrics may exhibit different failure patterns.
