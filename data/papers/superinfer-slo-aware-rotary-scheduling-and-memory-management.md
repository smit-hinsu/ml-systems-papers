---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Jiahuan Yu
- Mingtao Hu
- Zichao Lin
- Minjia Zhang
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/Supercomputing-System-AI-Lab/SuperInfer
domain:
- llm-serving
hardware:
- NVIDIA GH200
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 74.7% improvement in TTFT SLO attainment on GH200 vs. state-of-the-art
  systems while maintaining comparable TBT and throughput.
models_evaluated: []
observations:
  tier: DuplexKV uses full-duplex NVLink-C2C to transfer KV cache
    between GH200 GPU and CPU simultaneously; higher bandwidth than PCIe enables profitable
    KV offloading under tight TTFT SLOs.
  balance: RotaSched proactively rotates requests between GPU and CPU
    pools before KV cache exhaustion, preventing head-of-line blocking without reactive
    eviction that degrades TTFT.
official_category: ''
openreview_url: https://openreview.net/forum?id=RuslSHdIHa
organizations:
- UIUC
presentation_type: oral
principles:
- tier
- balance
problem: PCIe-based KV offloading cannot sustain tight TTFT and TBT SLOs at high
  request rates, causing head-of-line blocking when the KV cache budget is exhausted.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: superinfer-slo-aware-rotary-scheduling-and-memory-management
status: draft
title: 'SuperInfer: SLO-Aware Rotary Scheduling and Memory Management for LLM Inference
  on Superchips'
topics:
- kv-cache
- cpu-offload
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3809
---

## Key Contributions

- **RotaSched**: the first proactive SLO-aware rotary scheduler for Superchips; monitors KV cache occupancy and rotates requests between GPU and CPU memory before the cache budget is exhausted, preventing HOL blocking and maintaining TTFT/TBT compliance.
- **DuplexKV**: a high-performance KV rotation engine that exploits the GH200's bidirectional NVLink-C2C interconnect to run simultaneous inbound and outbound transfers, doubling effective KV migration bandwidth compared to PCIe-based offloading.
- System evaluated on GH200 across multiple models and datasets; achieves up to 74.7% improvement in TTFT SLO attainment while maintaining comparable TBT and throughput versus state-of-the-art LLM serving systems.

## Trade-offs

- RotaSched's proactive rotation requires accurate prediction of future KV demand; mispredictions under highly variable request arrival patterns may trigger unnecessary rotations or fail to prevent exhaustion.
- DuplexKV's bandwidth advantage is specific to NVLink-C2C; the approach provides limited benefit on standard PCIe-attached CPU-GPU systems.

## Nuances

- Evaluation is on GH200; generalization to other NVLink-C2C Superchip variants (e.g., future Grace-Blackwell systems) is implied but not explicitly characterized.
- The paper focuses on TTFT SLO attainment; long decode tail latency (P99 TBT) under sustained high request rates is not the primary metric.
