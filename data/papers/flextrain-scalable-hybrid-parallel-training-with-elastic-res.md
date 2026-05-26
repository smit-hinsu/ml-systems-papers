---
title: 'FlexTrain: Scalable Hybrid-Parallel Training with Elastic Resource Utilization and Consistent Accuracy'
slug: flextrain-scalable-hybrid-parallel-training-with-elastic-res
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
organizations:
- HKUST (Guangzhou)
- ByteDance
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3776
openreview_url: https://openreview.net/forum?id=h2yhNcbwSL
arxiv_url: ''
slides_url: ''
code_url: ''
project_url: ''
official_category: ''
presentation_type: oral
award: ''
arxiv_date: ''
domain:
- llm-training
- fleet-efficiency
topics:
- pipeline-parallelism
- tensor-parallelism
- fsdp-zero
principles:
- balance
- pipeline
observations:
  balance: FlexTrain adjusts pipeline-parallelism degree first when idle GPUs appear, preserving deterministic computation and consistent accuracy without needing full retraining.
  pipeline: When accuracy consistency is relaxed, additional data-parallelism scaling overlaps independent gradient reductions across newly added GPUs, reaching 2.27× over static allocation.
hardware: []
models_evaluated: []
agentic_models: []
citations: null
citations_updated: ''
research_or_industry: mixed
problem: Shared GPU clusters have significant idle GPUs, but elastic LLM training methods cause accuracy inconsistency, high profiling overhead, or limited parallelism flexibility.
key_results: Up to 1.73× speedup with consistent accuracy and 2.27× with relaxed consistency vs. non-elastic scheduling; evaluated on shared GPU clusters.
status: draft
reading_status: want-to-read
indexed_by: smithinsu
indexed_date: '2026-05-25'
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
