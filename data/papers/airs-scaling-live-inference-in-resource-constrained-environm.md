---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
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
hardware:
- TPU
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Serves Google LLM-based evaluation across 2+ priority tiers on shared
  TPUs; high-priority tasks meet latency SLOs while background tasks fill spare capacity.
models_evaluated: []
observations:
  balance: AIRS priority-aware scheduling gives high-priority rating tasks lower latency
    while background evaluation fills spare TPU capacity, maximizing utilization under
    a fixed resource budget.
  cache: Pipeline engineering across evaluation workflows avoids redundant preprocessing
    and caching shared prompt prefixes across ratings tasks that share common system-prompt
    templates.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=g1RWik4Gy1
organizations:
- Google
presentation_type: oral
principles:
- balance
- cache
problem: LLM rating demand at Google far exceeds the allocated TPU budget; serving
  all evaluation tasks competes with live user traffic for the same TPUs.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3781.pdf
slug: airs-scaling-live-inference-in-resource-constrained-environm
status: draft
title: 'AIRS: Scaling Live Inference in Resource Constrained Environments'
topics:
- continuous-batching
- prefix-caching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3781
---

## Background

Google uses LLM-based automated rating to evaluate search quality at the pace of model updates — replacing multi-day human rater cycles. This rating workload competes with live user traffic for the same TPU budget and total demand consistently exceeds capacity. Rating is latency-tolerant compared to user requests, making it a candidate for filling spare capacity, but requires a scheduler that can differentiate priority tiers without over-provisioning dedicated pools.

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