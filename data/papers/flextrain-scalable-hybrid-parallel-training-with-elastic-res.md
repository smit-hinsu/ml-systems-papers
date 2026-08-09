---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Weilin Cai
- Diandian Gu
- Baoquan Zhong
- Jun Wang
- Zhuolin Zheng
- Gaohong Liu
- Jiang Kaihua
- Shuguang Wang
- Wencong Xiao
- Jiayi Huang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
- fleet-efficiency
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 1.73× speedup with consistent accuracy and 2.27× with relaxed consistency
  vs. non-elastic scheduling; evaluated on shared GPU clusters.
models_evaluated: []
observations:
  elastic: Shared clusters free GPUs mid-run, but a job that widens its parallelism
    to absorb them changes the gradient reduction order and gives up reproducible
    accuracy to do it.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=h2yhNcbwSL
organizations:
- HKUST (Guangzhou)
- ByteDance
presentation_type: oral
principles:
- elastic
problem: Elastic LLM training on shared clusters causes accuracy inconsistency, high
  profiling overhead, or limited parallelism flexibility when absorbing idle GPUs.
project_url: ''
reading_status: want-to-read
research_or_industry: mixed
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3776.pdf
slug: flextrain-scalable-hybrid-parallel-training-with-elastic-res
status: draft
title: 'FlexTrain: Scalable Hybrid-Parallel Training with Elastic Resource Utilization
  and Consistent Accuracy'
topics:
- pipeline-parallelism
- tensor-parallelism
- fsdp-zero
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3776
---

## Key Contributions

- **PP-first elasticity**: Prioritizes adjusting pipeline-parallelism degree when GPU resources change, preserving deterministic stage assignments and bitwise-reproducible gradients, thereby maintaining training accuracy consistency
- **Performance prediction and scheduling**: Predicts training throughput under different PP/DP configurations given job submission intervals and scaling overhead, making scaling decisions that maximize net throughput gains
- **Optimal PP schedule generation**: Automatically generates pipeline schedules for asymmetric stage assignments when the number of pipeline stages changes at runtime
- **DP scaling under relaxed consistency**: Supplements PP adjustments with data-parallelism scaling for additional throughput when users accept minor numerical non-determinism, reaching 2.27× improvement

## Trade-offs

- PP-first scaling requires periodic checkpoint synchronization to maintain consistent model state across stage reconfigurations, adding overhead not present in static training.
- Accuracy consistency under elastic PP is preserved deterministically only when stage boundaries do not change; borderline cases may require additional validation.

## Nuances

- The 1.73× figure is for elastic jobs specifically (i.e., jobs that receive additional GPUs mid-run); the comparison baseline is conventional static scheduling, not another elastic system.
- Production deployment at ByteDance is implied by authorship but not explicitly stated in the paper.