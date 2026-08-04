---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Runsheng Guo
- Utkarsh Anand
- Khuzaima Daudjee
- Rathijit Sen
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
hardware:
- NVIDIA GPU (heterogeneous generations)
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 3× training throughput vs. Megatron-LM and DeepSpeed on representative
  heterogeneous GPU cluster scenarios
models_evaluated: []
observations:
  balance: In a mixed-generation GPU cluster, an even split of layers across pipeline
    stages makes the slowest GPU set the step time, so every faster GPU idles at each
    pipeline bubble.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=40leuGH3iO
organizations:
- University of Waterloo
- Microsoft Research
presentation_type: oral
principles:
- balance
problem: Heterogeneous GPU clusters bottleneck LLM training — existing parallelism
  integrations trade communication for memory overhead with no clean solution.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3859.pdf
slug: zorse-optimizing-llm-training-efficiency-on-heterogeneous-gp
status: draft
title: 'Zorse: Optimizing LLM Training Efficiency on Heterogeneous GPU Clusters'
topics:
- pipeline-parallelism
- fsdp-zero
- communication-overlap
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3859
---

## Key Contributions

- **Pipeline-Efficient ZeRO DP**: novel parallelism strategy that integrates pipeline parallelism with data parallelism in a way that is simultaneously communication-efficient (no extra all-reduce for sharded gradients) and memory-efficient (no full parameter replication across data-parallel ranks), overcoming the tradeoff in existing heterogeneous training systems.
- **Zorse planner**: automatically searches the vast configuration space of pipeline stage assignments, data-parallel group sizes, and GPU allocations to find an optimized training plan for a given heterogeneous cluster topology; avoids manual tuning.
- **Heterogeneous cluster handling**: accounts for varying compute, memory, and network bandwidth across GPU generations; the planner assigns heavier pipeline stages to faster GPUs to prevent slower devices from bottlenecking training.
- Achieves up to 3× higher training throughput than state-of-the-art systems (e.g., Megatron-LM, DeepSpeed) across representative heterogeneous training scenarios.

## Trade-offs

- Pipeline-Efficient ZeRO DP imposes specific pipeline-stage-to-data-parallel-rank assignment constraints; configurations where pipeline depth does not divide evenly across available GPU types may see suboptimal plans.
- The planner's search space grows with cluster heterogeneity; at very large scales (hundreds of heterogeneous nodes), planning time may become non-trivial.

## Nuances

- The 3× throughput improvement is measured "across representative heterogeneous scenarios"; specific scenarios (GPU generation mixes, model sizes) that achieve this upper bound are not detailed in the abstract.
- Evaluation covers training efficiency only; fault tolerance and recovery from heterogeneous GPU failures in long training runs are not addressed.