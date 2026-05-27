---
agentic_models: []
arxiv_url: ''
authors:
- Jaeyong Song
- Seongyeon Park
- Hongsun Jang
- Jaewon Jung
- Hunseong Lim
- Junguk Hong
- Jinho Lee
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-kernels
hardware:
- Single GPU
- NVMe SSD
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: GriNNder achieves up to 9.78x speedup over baselines on a single GPU
  with NVMe offloading, matching distributed multi-GPU system throughput on large
  graphs.
models_evaluated:
- GNNs (various models and large graph datasets)
observations:
  tier: SSO framework coordinates GPU-host-storage hierarchy via cache, regather,
    and bypass mechanisms tuned to full-graph GNN's unique cross-partition access
    patterns.
official_category: ''
openreview_url: https://openreview.net/forum?id=8SNPzGRldN
organizations:
- Seoul National University
presentation_type: oral
principles:
- tier
problem: Full-graph GNN training requires multiple GPUs or servers when graphs exceed
  GPU/host memory, incurring high hardware and communication costs.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3851_xn3JSf6.pdf
slug: grinnder-breaking-the-memory-capacity-wall-in-full-graph-gnn
status: draft
title: 'GriNNder: Breaking the Memory Capacity Wall in Full-Graph GNN Training with
  Storage Offloading'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3851
---

## Background

GNNs pass messages between connected nodes across layers. Full-graph training — processing all nodes and edges each iteration — is more accurate than mini-batch sampling but requires holding the entire graph in memory simultaneously. Real-world graphs (social, citation, molecular) easily exceed GPU memory, so the standard solution is multi-GPU distribution. GNN neighbor aggregation produces irregular random memory accesses that defeat naive CPU/NVMe offloading strategies, making single-machine alternatives impractical without careful hierarchy management.

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