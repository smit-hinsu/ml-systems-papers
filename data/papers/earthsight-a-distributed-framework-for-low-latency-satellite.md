---
agentic_models: []
arxiv_date: 2025-11
arxiv_url: https://arxiv.org/abs/2511.10834
authors:
- Ansel Erol
- Seungjun Lee
- Divya Mahajan
award: ''
citations: 1
citations_updated: '2026-07-31'
code_url: ''
domain:
- fleet-efficiency
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 1.9× lower compute time per image; 90th-percentile end-to-end latency
  51→21 minutes vs. per-satellite independent inference baseline in satellite simulator
models_evaluated: []
observations:
  cache: Shared backbone multi-task inference amortizes feature extraction across
    multiple vision tasks per satellite pass, so the same backbone activations serve
    N tasks rather than running N separate models.
  skip: Dynamic filter ordering rejects low-value frames using selectivity and accuracy
    estimates, skipping full inference on frames below query thresholds to save onboard
    compute for high-priority imagery.
official_category: ''
openreview_url: https://openreview.net/forum?id=c3O6DnhUYm
optimization_type: []
organizations:
- Georgia Tech
presentation_type: oral
principles:
- skip
principles_review:
- cache
problem: Satellite constellation intelligence is bottlenecked by redundant onboard
  inference across satellites and tasks, wasting scarce compute and downlink bandwidth.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3792_EM9rZRX.pdf
slug: earthsight-a-distributed-framework-for-low-latency-satellite
status: draft
title: 'EarthSight: A Distributed Framework for Low-Latency Satellite Intelligence'
topics:
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3792
---

## Background

Earth observation satellites carry onboard compute to run vision models (fire, flood, ship detection) before downlinking, so scarce downlink bandwidth carries only relevant findings. Each satellite in a constellation usually runs on its own, wasting compute twice over: a separate model instance per task re-runs the same backbone, and nothing coordinates load across satellites — one over a high-value region saturates while others over open ocean sit idle.

## Key Contributions

- **Multi-task onboard inference with shared backbones**: a single satellite runs multiple vision tasks sharing a common backbone, amortizing the expensive feature extraction step across all tasks and reducing total per-image compute time 1.9×
- **Ground-station query scheduler**: aggregates user requests from multiple tasks and users, predicts image priorities, and assigns compute budgets to incoming satellite imagery — coordinating decisions globally rather than treating each satellite as an independent node
- **Dynamic filter ordering**: integrates model selectivity, accuracy, and execution cost to reject low-value images early in the pipeline, conserving onboard power and compute for high-priority imagery
- **90th-percentile latency reduction**: end-to-end latency from first contact to image delivery drops from 51 to 21 minutes vs. state-of-the-art baseline, validated using an established satellite simulation framework

## Trade-offs

- The ground-station scheduler requires accurate priority prediction; stale or incorrect priority estimates could cause under-allocation to high-value imagery or over-spending on low-value frames.
- Multi-task backbone sharing couples the performance of tasks with incompatible feature requirements; tasks with conflicting backbone demands may see accuracy degradation relative to task-specific models.

## Nuances

- Evaluation uses a satellite simulator, not live constellation hardware; link latency variability, onboard hardware heterogeneity, and orbital constraints may differ in practice.
- Dynamic filter ordering depends on pre-calibrated selectivity and accuracy models per task; deploying new tasks to the constellation requires re-calibrating these cost models without onboard retraining.
