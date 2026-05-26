---
slug: faascale-unlocking-fast-llm-scaling-for-serverless-inference
title: "FaaScale: Unlocking Fast LLM Scaling for Serverless Inference"
authors:
- Minchen Yu
- Rui Yang
- Chaobo Jia
- Zhaoyuan Su
- Sheng Yao
- Tingfeng Lan
- Yuchen Yang
- Zirui Wang
- Yue Cheng
- Wei Wang
- Ao Wang
- Ruichuan Chen
organizations:
- Chinese University of Hong Kong
- University of Virginia
- Hong Kong University of Science and Technology
- Alibaba
- Nokia Bell Labs
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3769
openreview_url: https://openreview.net/forum?id=jgL8LuOVyT
arxiv_url: ''
presentation_type: oral
official_category: ''
award: ''
status: draft
reading_status: want-to-read
research_or_industry: research
indexed_by: smithinsu
indexed_date: '2026-05-24'
citations: null
citations_updated: ''
code_url: ''
project_url: ''
slides_url: ''
domain:
- llm-serving
- fleet-efficiency
hardware:
- GPU cluster
models_evaluated:
- LLMs (serverless cloud workloads)
agentic_models: []
topics:
- pipeline-parallelism
principles:
- pipeline
- fuse
observations:
  pipeline: "PipeCast overlaps model block multicast transfer with pipeline-parallel inference execution, hiding model download latency during scale-out."
  fuse: "Multicast transfers a single copy of model blocks to multiple nodes simultaneously instead of unicast per node, reducing total bytes transferred."
problem: "Serverless LLM scaling-on-demand is bottlenecked by high model data transfer cost, causing long cold-start latency under bursty traffic."
key_results: "FaaScale cuts tail TTFT by up to 5x and reduces serving cost by 31.3% on real-world LLM traces via pipelined multicast inference."
---

## Key Contributions

- **Pipelined multicast inference (PipeCast)**: Synergizes network multicast with dynamic, cross-node pipeline-parallel execution during model transfer — model blocks are multicasted to new nodes while inference is simultaneously served on partially loaded pipelines.
- **Adaptive memory management**: Efficient GPU and host memory management to handle bursty serverless LLM workloads with minimal waste.

## Trade-offs

- Pipelined inference during model transfer requires careful synchronization to avoid serving partial-model outputs; the design must ensure inference correctness.
- Multicast is only efficient when multiple nodes need the same model; heterogeneous multi-model deployments reduce the benefit.

## Nuances

- The 5x tail TTFT improvement is the peak case on bursty traces; average improvements depend on traffic patterns and scale-out frequency.
- Cost reduction of 31.3% is measured end-to-end on real-world LLM traces, accounting for infrastructure costs.
