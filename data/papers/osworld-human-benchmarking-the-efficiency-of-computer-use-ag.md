---
agentic_models: []
arxiv_date: 2025-06
arxiv_url: https://arxiv.org/abs/2506.16042
authors:
- Reyna Abhyankar
- Qi Qi
- Yiying Zhang
award: ''
citations: 30
citations_updated: '2026-07-31'
code_url: ''
domain:
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Best agents take 2.7–4.3× more steps than humans; planning/reflection
  model calls dominate latency; per-step latency grows 3× as context accumulates
models_evaluated: []
observations: {}
official_category: ''
openreview_url: https://openreview.net/forum?id=0Cp8l6cvyq
optimization_type: []
organizations:
- UC San Diego
presentation_type: oral
principles: []
problem: Computer-use agents achieve high benchmark accuracy but are unusable in practice
  due to end-to-end latency tens of minutes for tasks humans complete in minutes.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3865.pdf
slug: osworld-human-benchmarking-the-efficiency-of-computer-use-ag
status: draft
title: 'OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3865
---

## Key Contributions

- **OSWorld-Human benchmark**: manually annotated version of the OSWorld dataset with human-determined optimal trajectories for each task, providing a ground-truth efficiency reference against which agent step counts can be measured
- **Efficiency evaluation of 16 agents**: systematic comparison measuring step count ratio (agent steps vs. human steps) and per-step latency distribution across the OSWorld task suite
- **Latency breakdown**: quantifies that large model calls for planning, reflection, and judging dominate overall latency; reveals that per-step latency grows 3× over a task as context accumulates

## Findings

- Even the best computer-use agents require 2.7–4.3× more steps than human-determined optimal trajectories, indicating that accuracy optimization has not addressed step efficiency.
- Each successive agent step takes progressively longer than earlier steps (up to 3×), driven by growing context windows passed to planning and reflection models.
- Planning, reflection, and judging model calls collectively account for the majority of end-to-end task latency; the action execution itself is a small fraction.
- Practical deployability requires both accuracy and efficiency to be simultaneously addressed; current SOTA systems fail on the efficiency axis despite high benchmark accuracy.

## Nuances

- Human-annotated trajectories represent one valid optimal path, not the unique shortest path; some human annotations may still include unnecessary steps.
- Benchmark tasks are from the original OSWorld suite; specialized enterprise computer-use scenarios may have different latency bottlenecks.
