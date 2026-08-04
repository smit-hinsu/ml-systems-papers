---
agentic_models: []
arxiv_date: ''
arxiv_url: https://arxiv.org/abs/2511.21686
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
citations: 2
citations_updated: '2026-07-31'
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
  simplify: Centralized orchestration for synthetic data generation serializes task
    dispatch; a coordinator-free peer-to-peer design achieves 2–15× throughput because
    the coordinator itself was the bottleneck.
official_category: ''
openreview_url: https://openreview.net/forum?id=ok96wGyPdI
optimization_type: []
organizations:
- Meta
presentation_type: oral
principles:
- simplify
problem: Centralized orchestrators in multi-agent synthetic data pipelines create
  scalability bottlenecks; hardcoded designs limit reuse across diverse generation
  tasks.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3753_h4L43wQ.pdf
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
