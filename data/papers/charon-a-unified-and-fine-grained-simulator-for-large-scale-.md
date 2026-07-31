---
agentic_models: []
arxiv_date: 2026-05
arxiv_url: https://arxiv.org/abs/2605.17164
authors:
- Mengtian Yang
- Zhekun Zhang
- Mingheng Wu
- Jianwen Yan
- Hanshi Sun
- Li-wen Chang
award: ''
citations: 0
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-training
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Prediction error under 5.35% across models and configurations; under
  3.74% for large-scale GPU cluster training; discovered a higher-throughput inference
  config
models_evaluated: []
observations:
  measure: Testing one tensor/pipeline parallelism split costs a full cluster run,
    so teams settle on an expert guess and never learn what the untried points in
    the space would have delivered.
official_category: ''
openreview_url: https://openreview.net/forum?id=19O6GAS7Su
optimization_type: []
organizations:
- ByteDance
presentation_type: oral
principles:
- measure
problem: Exploring parallelism and optimization design spaces for large-scale LLM
  training/inference requires expensive empirical runs that are prohibitively slow.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3861_7kTIKEc.pdf
slug: charon-a-unified-and-fine-grained-simulator-for-large-scale-
status: draft
title: 'Charon: A Unified and Fine-Grained Simulator for Large-Scale LLM Training
  and Inference'
topics:
- tensor-parallelism
- pipeline-parallelism
- communication-overlap
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3861
---

## Key Contributions

- **Charon simulator**: unified, modular, fine-grained performance predictor for LLM training and inference that models parallelism strategies, system optimizations, and hardware configurations in a single framework
- **High accuracy**: prediction error consistently under 5.35% across varied models and configurations; under 3.74% for large-scale cluster training, enabling reliable what-if hypothesis validation
- **Practical inference optimization**: in a real deployment case, Charon identified a configuration that improved system throughput beyond an expert-tuned engineering baseline, demonstrating production utility

## Trade-offs

- Fine-grained simulation requires accurate hardware performance models; miscalibrated roofline or bandwidth parameters would propagate error to all predictions.
- Simulation may not capture transient effects like thermal throttling, NCCL contention at scale, or OS noise that affect wall-clock performance in real clusters.

## Nuances

- The <3.74% error claim is for training on large-scale GPU clusters; serving prediction accuracy may vary, and the paper does not detail accuracy breakdowns by workload type.
- The discovered higher-throughput inference configuration is described qualitatively; the specific optimization knob found is not detailed in the abstract.
