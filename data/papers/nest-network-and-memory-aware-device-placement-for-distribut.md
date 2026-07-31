---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Irene Wang
- Vishnu Varma Venkata
- Arvind Krishnamurthy
- Divya Mahajan
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/scai-tech/Nest
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 2.43× training throughput vs. heuristic placement methods, with
  better memory efficiency across diverse hardware and datacenter network topologies
models_evaluated: []
observations: {}
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=jpIoO2zSKA
organizations:
- Georgia Tech
- University of Washington
presentation_type: oral
principles: []
problem: Heuristic or topology-agnostic distributed training placement causes post-hoc
  sharding that inflates communication and underutilizes compute.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3767_u5zq5Pz.pdf
slug: nest-network-and-memory-aware-device-placement-for-distribut
status: draft
title: 'NEST: Network- and Memory-Aware Device Placement for Distributed Deep Learning'
topics:
- tensor-parallelism
- pipeline-parallelism
- fsdp-zero
- all-reduce
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3767
---

## Key Contributions

- **Unified structured dynamic programming**: operator graph annotated with intra-layer parallelism configs (tensor, expert, sequence, context), explicit allreduce latencies, and per-device memory/compute profiles; DP searches hybrid strategies in a principled, jointly-feasible space
- **Topology modeling**: models hierarchical or arbitrary datacenter networks with explicit allreduce latency estimates per communication group, enabling co-location decisions that minimize synchronization cost on real networks
- **Memory-feasible search**: encodes per-device memory capacity as a hard constraint within the DP, eliminating infeasible placements without post-hoc correction and avoiding the over-sharding that inflates communication in prior heuristic methods
- Achieves up to 2.43× higher throughput than SOTA baselines across diverse hardware configurations and datacenter network topologies

## Trade-offs

- Structured DP search over the joint parallelism space is more expensive than per-dimension heuristic search; compilation overhead may be significant for very large or heterogeneous operator graphs.
- Topology models must be calibrated per-cluster; inaccurate bandwidth or latency estimates can degrade placement quality without triggering obvious errors.