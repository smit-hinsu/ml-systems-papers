---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Ansel Erol
- Seungjun Lee
- Divya Mahajan
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- fleet-efficiency
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 1.9× lower compute time per image; 90th-percentile end-to-end latency
  from 51 to 21 minutes vs. state-of-the-art baseline using satellite simulator
models_evaluated: []
observations:
  skip: Dynamic filter ordering rejects low-value images early based on
    selectivity and accuracy estimates, avoiding full inference on images unlikely
    to meet user query thresholds — amortizing compute only on high-value imagery.
  balance: Ground-station query scheduler aggregates user requests and
    distributes compute budgets to incoming images across the constellation, preventing
    hotspot satellites from wasting cycles while others are idle.
  cache: Shared backbone multi-task inference amortizes feature extraction
    across multiple vision tasks per satellite pass, so the same backbone activations
    serve N tasks rather than running N separate models.
official_category: ''
openreview_url: https://openreview.net/forum?id=c3O6DnhUYm
organizations:
- Georgia Tech
presentation_type: oral
principles:
- skip
- balance
- cache
problem: Satellite constellation intelligence is bottlenecked by redundant onboard
  inference across satellites and tasks, wasting scarce compute and downlink bandwidth.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: earthsight-a-distributed-framework-for-low-latency-satellite
status: draft
title: 'EarthSight: A Distributed Framework for Low-Latency Satellite Intelligence'
topics:
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3792
---

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
