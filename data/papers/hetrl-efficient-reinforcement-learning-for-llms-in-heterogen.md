---
agentic_models: []
arxiv_date: 2025-12
arxiv_url: https://arxiv.org/abs/2512.12476
authors:
- Yongjun He
- Shuai Zhang
- Jiading Gai
- Xiyuan Zhang
- Boran Han
- Bernie Wang
- Huzefa Rangwala
- George Karypis
award: ''
citations: 2
citations_updated: '2026-07-31'
code_url: ''
domain:
- rl-training
hardware:
- Heterogeneous GPU clusters
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Up to 9.17× throughput vs. Ray on heterogeneous GPU clusters in 20,000
  GPU-hour evaluation
models_evaluated: []
observations:
  balance: GPU tiers differ in speed, but schedulers hand every tier the same share
    of actor, critic, and rollout work, so fast GPUs finish and idle while slow tiers
    still grind.
  pipeline: The hybrid scheduler identifies independent RL stages that run concurrently
    across GPU types, shrinking iteration time beyond what serial actor-critic-rollout
    execution allows.
official_category: ''
openreview_url: https://openreview.net/forum?id=LRLyuaz1W7
optimization_type: []
organizations:
- ETH Zurich
- Amazon
presentation_type: oral
principles:
- balance
- pipeline
problem: RL post-training for LLMs on heterogeneous GPU clusters wastes compute; schedulers
  assume homogeneous hardware and serialize actor, critic, rollout stages.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3825_dNuKxpR.pdf
slug: hetrl-efficient-reinforcement-learning-for-llms-in-heterogen
status: draft
title: 'HetRL: Efficient Reinforcement Learning for LLMs in Heterogeneous Environments'
topics:
- pipeline-parallelism
- tensor-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3825
---

## Key Contributions

- **Constrained joint optimization**: HetRL models the RL training workflow as a constrained optimization problem over heterogeneous GPU-network topologies, enabling principled task allocation rather than ad-hoc placement of actor, critic, and rollout stages.
- **Hybrid scheduling algorithm**: A heuristic solver rapidly produces near-optimal schedules, trading a small optimality gap for fast schedule generation suitable for dynamic heterogeneous workloads.
- **ILP-based scheduling**: An integer linear programming formulation yields optimal schedules when budget permits, enabling flexible throughput-vs-optimality trade-offs suited to offline or periodic re-scheduling.

## Trade-offs

- ILP scheduling is computationally expensive at large GPU counts; the hybrid heuristic must substitute for large clusters where exact optimization is intractable.
- The system assumes a fixed RL workflow graph structure; novel RL algorithms with non-standard stage dependencies require re-modeling the optimization problem.

## Nuances

- The 9.17× peak speedup targets a specific workload configuration; the 3.17× average across the evaluation suite better reflects general heterogeneous cluster gains.
- Results consume 20,000 GPU-hours, confirming large-scale validation but also indicating high development experimentation costs.
