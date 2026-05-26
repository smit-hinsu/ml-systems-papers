---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Dong Wang
- Yang Li
- Ansong Ni
- Ching-Feng Yeh
- Youssef Emad
- Xinjie Lei
- Liam Robbins
- Karthik Padthe
- Hu Xu
- Xian Li
- Asli Celikyilmaz
- Ramya Raghavendra
- LIFEI HUANG
- Carole-Jean Wu
- Shang-Wen Li
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 2–15× higher synthetic data generation throughput under identical hardware
  across multi-agent dialogue, web reasoning, and tool-use scenarios
models_evaluated: []
observations:
  balance: Eliminating the central orchestrator removes the coordination
    bottleneck; tasks progress independently through queues, keeping all workers busy
    without a serializing scheduler.
  pipeline: Peer-to-peer message passing lets concurrent agentic
    workflows advance in parallel on Ray, overlapping LLM inference across tens of
    thousands of tasks simultaneously.
official_category: ''
openreview_url: https://openreview.net/forum?id=ok96wGyPdI
organizations:
- Meta
presentation_type: oral
principles:
- balance
- pipeline
problem: Centralized orchestrators in multi-agent synthetic data pipelines create
  scalability bottlenecks; hardcoded designs limit reuse across diverse generation tasks.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: matrix-peer-to-peer-multi-agent-synthetic-data-generation-fr
status: draft
title: 'Matrix: Peer-to-Peer Multi-Agent Synthetic Data Generation Framework'
topics:
- streaming
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3753
---

## Key Contributions

- **Decentralized control flow**: represents both control and data as serialized messages through distributed queues, eliminating the central orchestrator bottleneck; built on Ray to scale to tens of thousands of concurrent agentic workflows
- **Peer-to-peer agent design**: each task progresses independently through lightweight agents; compute-intensive operations (LLM inference, containerized sandboxes) run as separate distributed services rather than routing through a single coordinator
- **Modular configurability**: pluggable agent and service definitions enable adaptation to multi-agent collaborative dialogue, web-based reasoning extraction, and tool-use trajectory generation without framework changes
- Evaluated across three distinct synthesis scenarios, achieving 2–15× throughput improvement over centralized baselines under identical hardware

## Trade-offs

- Decentralized message-passing complicates global state tracking and fault recovery; debugging distributed queue failures is harder than tracing a single orchestrator log.
- Throughput gains depend on workload parallelizability; highly sequential pipelines where each step depends on the prior output gain little from the peer-to-peer design.
