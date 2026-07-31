---
agentic_models: []
arxiv_date: 2024-09
arxiv_url: https://arxiv.org/abs/2409.01143
authors:
- Ran Yan
- Youhe Jiang
- Xiaonan Nie
- Fangcheng Fu
- Bin Cui
- Binhang Yuan
award: ''
citations: 14
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-training
hardware:
- Heterogeneous GPU clusters
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 1.5×–2.4× higher throughput vs. heterogeneous baselines; similar throughput
  to homogeneous baselines when given equal theoretical FLOPS, for 7B–30B LLMs
models_evaluated:
- LLMs (7B to 30B)
observations:
  balance: Equal-size parallelism partitions on mixed GPU generations let the weakest
    device set the step time; every faster GPU waits at the sync point for it.
  pipeline: Asymmetric tensor and pipeline parallelism partitions allow work-stealing
    across heterogeneous tiers so that faster GPUs do not idle while slower ones finish
    their unequal slices.
official_category: ''
openreview_url: https://openreview.net/forum?id=KgcqSNio0U
optimization_type: []
organizations:
- Hong Kong University of Science and Technology
- Peking University
- Shanghai Jiao Tong University
presentation_type: oral
principles:
- balance
- pipeline
problem: Standard LLM parallelism strategies assume equal-speed devices, leaving weaker
  GPUs as stragglers in heterogeneous clusters and wasting available compute.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3828_GyjCel6.pdf
slug: hexiscale-facilitating-large-language-model-training-over-he
status: draft
title: 'HexiScale: Facilitating Large Language Model Training over Heterogeneous Hardware'
topics:
- pipeline-parallelism
- tensor-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3828
---

## Key Contributions

- **Asymmetric parallelism support**: HexiScale extends data-, pipeline-, and tensor-parallelism to allow unequal partition sizes, enabling each GPU to receive a workload slice proportional to its actual compute capacity rather than a fixed equal share.
- **Hierarchical graph partitioning algorithm**: An efficient algorithm solves the constrained optimization of mapping asymmetrically partitioned computations to heterogeneous GPUs, fully exploiting available FLOPS without manual tuning.
- **Heterogeneous cluster parity**: When given the same aggregate theoretical FLOPS as a homogeneous cluster, HexiScale matches homogeneous baseline throughput, demonstrating that performance parity is achievable without sacrificing heterogeneous flexibility.

## Trade-offs

- Asymmetric partitions complicate gradient synchronization and require careful load-balancing logic; implementation complexity is higher than standard homogeneous training.
- The hierarchical partitioning algorithm's runtime grows with cluster heterogeneity; very large clusters with many distinct GPU types may incur non-trivial scheduling overhead.

## Nuances

- The 1.5×–2.4× speedup over heterogeneous baselines is evaluated on clusters with a specific mix of GPU generations; gains depend heavily on the degree of hardware heterogeneity.
- Parity with homogeneous baselines holds when theoretical FLOPS are matched; real deployments may have memory bandwidth mismatches that reduce parity.
