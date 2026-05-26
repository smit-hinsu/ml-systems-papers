---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
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
key_results: Up to 3× higher training throughput than state-of-the-art systems across
  representative heterogeneous training scenarios.
models_evaluated: []
observations:
  balance: Pipeline-Efficient ZeRO DP partitions model parameters across
    pipeline stages without replication, ensuring slower GPUs do not bottleneck the
    pipeline through balanced compute assignment found by the planner.
  fuse: Pipeline-Efficient ZeRO DP is both communication- and memory-efficient;
    it avoids the extra all-reduce traffic of sharded data parallelism combined with
    pipeline parallelism while also avoiding the memory overhead of replicating parameters
    across data-parallel ranks.
official_category: ''
openreview_url: https://openreview.net/forum?id=40leuGH3iO
organizations:
- University of Waterloo
- Microsoft Research
presentation_type: oral
principles:
- balance
- fuse
problem: Training LLMs on heterogeneous GPU clusters is inefficient because existing
  integrations of data, pipeline, and tensor parallelism trade off communication overhead
  for memory overhead, causing bottlenecks.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
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
