---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Mengtian Yang
- Zhekun Zhang
- Mingheng Wu
- Jianwen Yan
- Hanshi Sun
- Li-wen Chang
award: ''
citations: null
citations_updated: ''
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
observations: {}
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=19O6GAS7Su
organizations:
- ByteDance
presentation_type: oral
principles: []
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

## Background

Choosing parallelism strategies for LLM training — pipeline parallelism, tensor parallelism, data parallelism, and communication overlap — requires evaluating combinations that each demand real GPU-hours to measure. Running systematic experiments on a 512-GPU cluster is prohibitively expensive, but naive roofline simulators miss fine-grained effects like pipeline bubbles and NCCL contention that determine actual throughput.

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