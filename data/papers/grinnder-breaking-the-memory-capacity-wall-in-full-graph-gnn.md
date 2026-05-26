---
slug: grinnder-breaking-the-memory-capacity-wall-in-full-graph-gnn
title: "GriNNder: Breaking the Memory Capacity Wall in Full-Graph GNN Training with Storage Offloading"
authors:
- Jaeyong Song
- Seongyeon Park
- Hongsun Jang
- Jaewon Jung
- Hunseong Lim
- Junguk Hong
- Jinho Lee
organizations:
- Seoul National University
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3851
openreview_url: https://openreview.net/forum?id=8SNPzGRldN
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
- llm-training
hardware:
- Single GPU
- NVMe SSD
models_evaluated:
- GNNs (various models and large graph datasets)
agentic_models: []
topics: []
principles:
- tier
- cache
observations:
  tier: "SSO framework coordinates GPU-host-storage hierarchy via cache, regather, and bypass mechanisms tuned to full-graph GNN's unique cross-partition access patterns."
  cache: "Regathering strategy for gradient computation eliminates redundant NVMe reads by reusing already-fetched neighbor data during backprop."
problem: "Full-graph GNN training requires multiple GPUs or servers when graphs exceed GPU/host memory, incurring high hardware and communication costs."
key_results: "GriNNder achieves up to 9.78x speedup over baselines on a single GPU with NVMe offloading, matching distributed multi-GPU system throughput on large graphs."
---

## Key Contributions

- **Structured Storage Offloading (SSO)**: A framework managing the GPU-host-storage three-level hierarchy through coordinated cache, regather, and bypass mechanisms specifically designed for full-graph GNN access patterns.
- **Partition-wise caching**: Host memory cache strategy exploiting cross-partition dependencies in GNN computation to maximize cache hit rates for neighbor lookups.
- **Lightweight partitioning scheme**: Reduces memory requirements of graph partitioning itself, addressing a bootstrapping problem where partitioners need memory to enable memory-saving.

## Trade-offs

- NVMe bandwidth (>10 GB/s) is the new bottleneck when graphs exceed host memory; performance depends heavily on SSD bandwidth.
- The SSO framework requires graph partitioning as a preprocessing step, adding upfront overhead for very large graphs.

## Nuances

- GriNNder enables previously infeasible training scenarios — graphs that require multiple servers can now train on a single GPU-equipped machine with NVMe SSDs.
- The 9.78x speedup is over storage-based baselines, not GPU-only baselines; compared to distributed systems the throughput is comparable.
