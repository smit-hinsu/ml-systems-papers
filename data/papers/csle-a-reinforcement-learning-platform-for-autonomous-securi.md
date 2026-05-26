---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Kim Hammar
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- rl-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Near-optimal security management across four use cases in an emulated
  operational environment; simulation-to-emulation gap closed via iterative refinement
models_evaluated: []
observations:
  balance: Emulation system replicates the target operational environment
    in virtualized form, enabling realistic RL training that closes the simulation-to-operational
    performance gap seen in prior simulation-only approaches.
official_category: ''
openreview_url: https://openreview.net/forum?id=QGuRWjFsnm
organizations:
- KTH Royal Institute of Technology
presentation_type: oral
principles:
- balance
problem: RL-based security management strategies trained in simulation fail to generalize
  to operational networked systems due to the sim-to-real gap in system dynamics.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: csle-a-reinforcement-learning-platform-for-autonomous-securi
status: draft
title: 'CSLE: A Reinforcement Learning Platform for Autonomous Security Management'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3812
---

## Key Contributions

- **CSLE platform**: a two-system RL platform for autonomous security management comprising an emulation system (virtualizes the operational environment for measurement/log collection) and a simulation system (learns strategies from an MDP model fit to emulation data)
- **Emulation-simulation loop**: strategies learned in fast simulation are evaluated in the emulation environment, and the gap between simulated and emulated performance is used to refine the MDP model — closing the sim-to-real gap iteratively
- **Four security use cases**: demonstrates CSLE across flow control, replication control, segmentation control, and recovery control, achieving near-optimal management policies that approach theoretical benchmarks in each domain

## Findings

- Simulation-only RL for security management shows poor operational generalization; the emulation system is essential for bridging the gap to real system behavior.
- Iterative refinement of the MDP model using emulation measurements is sufficient to achieve near-optimal policies without direct online RL in the production system.
- Near-optimal security management is achievable across diverse control tasks (flow, replication, segmentation, recovery) using a shared platform architecture.

## Trade-offs

- The emulation system must replicate key operational components faithfully; simplifications in the virtual environment introduce residual sim-to-real gaps that iterative refinement may not fully close.
- Emulation is more expensive than pure simulation; training throughput is limited by how fast the virtual environment can execute episodes.

## Nuances

- Results are validated in an emulation environment that approximates operational systems, not in live production infrastructure; true operational deployment is not demonstrated.
- The platform is general-purpose, but the four use cases are all network-security scenarios; applicability to other RL-driven autonomous management tasks (e.g., resource scheduling, fault recovery) is asserted but not validated.
