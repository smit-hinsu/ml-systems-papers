---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Joyce Yuan
- Yichuan Shi
- Abhishek Singh
- Rishi Sharma
- Ramesh Raskar
- Jonas Blanc
- Martin Jaggi
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
- observability
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 5+ topology variants; sparse ring/torus match dense graphs at lower communication
  cost; collaborator collapse is a systematic failure in adaptive selection
models_evaluated: []
observations:
  measure: Every decentralized-learning paper picks its own node count, data split,
    and neighbor graph, so topology results cannot be compared — and collaborator
    collapse never shows up in the accuracy number.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=4Bqg7Xyk5t
organizations:
- MIT Media Lab
- EPFL
presentation_type: oral
principles:
- measure
problem: Network topology's role in decentralized learning is poorly understood due
  to lack of controlled, reproducible evaluation frameworks with consistent conditions.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3857.pdf
slug: sonar-benchmarking-topology-and-collaboration-in-decentraliz
status: draft
title: 'SONAR: Benchmarking Topology and Collaboration in Decentralized Learning'
topics:
- all-reduce
- communication-overlap
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3857
---

## Background

Decentralized learning trains across nodes that talk only to neighbors defined by a communication topology, with no central parameter server. Topology — dense graph vs. sparse ring or torus — drives convergence speed, communication cost, and robustness to data heterogeneity, but prior work uses inconsistent setups that make results incomparable. Adaptive neighbor selection adds a failure mode: nodes cluster into homogeneous groups and lose gradient diversity.

## Key Contributions

- **SONAR framework**: modular system for topology-aware decentralized learning that unifies communication, topology management, and fine-grained telemetry; enables end-to-end measurement of performance, communication, robustness, and privacy under consistent conditions
- **Topology as a systems variable**: demonstrates that sparse structured topologies (rings, tori) can achieve comparable or superior accuracy to dense graphs at substantially lower communication cost, revealing a clear efficiency frontier
- **Collaborator collapse identification**: discovers and characterizes a systematic failure mode in adaptive collaboration where similarity-based neighbor selection reduces diversity, degrading generalization as neighbors converge to homogeneous groups
- Enables systematic, reproducible evaluation of decentralized learning; provides practical guidance for designing efficient and robust collaborative systems at scale

## Findings

- Sparse, structured topologies (rings and tori) can match dense graphs in accuracy at much lower communication cost under certain conditions; the efficiency frontier depends on scale and data heterogeneity.
- Topology impact amplifies with scale and data heterogeneity; small-scale homogeneous settings underestimate topology effects.
- Collaborator collapse is a systematic failure mode in adaptive (similarity-based) neighbor selection; it is distinct from and not captured by standard accuracy metrics.

## Trade-offs

- The efficiency advantage of sparse topologies holds "under circumstances" (data heterogeneity, scale); dense topologies may outperform sparse ones in homogeneous, small-scale settings.
- SONAR's modular design adds instrumentation overhead vs. lean production decentralized learning implementations.

## Nuances

- Collaborator collapse is identified as a failure mode but mitigation strategies (e.g., diversity-preserving selection) are not fully prescribed in the abstract.
- Evaluation is on academic decentralized learning benchmarks; real-world federated learning at hyperscale may have different topology constraints (geographic routing, privacy regulations).