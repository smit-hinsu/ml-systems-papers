---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Nilesh Jagnik
- Xiaohao Yang
- Tuan Do
- Chelsea Chen
- Harshvardhan GM
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
- fleet-efficiency
organizations:
- Google
hardware:
- TPU
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Maximizes TPU inference throughput for LLM-based quality evaluation at
  Google; serves multiple evaluation workflows under constrained TPU budgets with
  priority-differentiated latency
models_evaluated: []
observations:
  balance: AIRS schedules evaluation workflows across shared TPU resources
    with priority-aware scheduling; higher-priority rating tasks receive lower latency
    while background evaluation fills spare capacity, maximizing overall TPU utilization.
  cache: Pipeline engineering across evaluation workflows avoids redundant
    preprocessing and caching shared prompt prefixes across ratings tasks that share
    common system-prompt templates.
official_category: ''
openreview_url: https://openreview.net/forum?id=g1RWik4Gy1
presentation_type: oral
principles:
- balance
- cache
problem: LLM rating demand at Google far exceeds the allocated TPU budget; human raters
  take days and are expensive, but serving all LLM evaluation tasks competes with
  live user traffic for the same TPUs.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: airs-scaling-live-inference-in-resource-constrained-environm
status: draft
title: 'AIRS: Scaling Live Inference in Resource Constrained Environments'
topics:
- continuous-batching
- prefix-caching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3781
---

## Key Contributions

- **AI Rater Service (AIRS)**: production inference pipeline at Google that performs LLM-based quality evaluation of search engine responses, replacing multi-day human rating processes with low-latency automated ratings
- **Multi-workflow TPU scheduling**: optimizes TPU resource utilization across diverse evaluation workflows with different priority levels, ensuring high-priority live ratings get low latency while lower-priority batch evaluations fill spare capacity
- **Resource-constrained throughput maximization**: engineering techniques (batching, caching, workflow pipelining) that maximize the number of LLM ratings produced within a fixed TPU budget smaller than total demand
- **Priority-differentiated serving**: distinguishes live evaluation latency requirements from batch evaluation workflows, allowing the system to serve both classes reliably without over-provisioning

## Trade-offs

- Fixed TPU budget means demand surges (e.g., new product launches requiring large-scale evaluation) must be queued or throttled; latency SLOs for lower-priority workflows are soft targets.
- Sharing TPU capacity between evaluation and live user traffic creates head-of-line blocking risk during traffic spikes.

## Nuances

- AIRS is described at a high level with production deployment context; specific throughput numbers and latency quantiles are not reported in the abstract.
- The paper focuses on engineering techniques for a constrained-resource production system rather than proposing novel algorithmic contributions.
