---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2506.05508
authors:
- Tiyasa Mitra
- Ritika Borkar
- Nidhi Bhatia
- Shivam Raj
- hongkuan zhou
- Yan Ru Pei
- Vishwanath Venkatesan
- Kyle Kranen
- Ramon Matas
- Dheevatsa Mudigere
- Ritchie Zhao
- Maximilian Golub
- Arpan Dutta
- Suresh Nambi
- Sailaja Madduri
- Dharmesh Jani
- Brian Pharris
- Itay Neeman
- Bita Darvish Rouhani
award: ''
citations: null
citations_updated: ''
code_url: ''
date: 2026-05
domain:
- llm-serving
hardware:
- NVIDIA Blackwell (B200)
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Disaggregation + CPP on Blackwell achieves Pareto-optimal TTFT/throughput
  on Llama-405B and DeepSeek-R1; generation-heavy traffic sees no benefit.
models_evaluated:
- Llama-3.1-70B
- Llama-3.1-405B
- DeepSeek-R1
observations:
  balance-utilization: The optimal context-to-generation GPU ratio varies significantly
    with model size and traffic pattern; static ratios leave either prefill or decode
    GPUs underutilized without elastic scaling.
  overlap-independent-work: Prefill and decode have fundamentally different optimal
    batch sizes; running them on separate GPU pools lets each phase be sized and batched
    independently, eliminating head-of-line blocking.
official_category: ''
openreview_url: https://openreview.net/forum?id=NqC5tcBsa0
organizations:
- NVIDIA
presentation_type: oral
principles:
- overlap-independent-work
- balance-utilization
problem: In monolithic LLM serving, long prefill requests block decode batches causing
  head-of-line latency spikes, but disaggregation gains vary widely by workload.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3819_593EcQk.pdf
slug: beyond-the-buzz-a-pragmatic-take-on-inference-disaggregation
status: draft
title: 'Beyond the Buzz: A Pragmatic Take on Inference Disaggregation'
topics:
- continuous-batching
- kv-cache
- pipeline-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3819
---

## Key Contributions

- **Systematic disaggregation study**: First evaluation of hundreds of thousands of design points spanning workload shapes, GPU counts, and hardware generations; establishes when prefill-decode disaggregation improves vs. degrades the TTFT/throughput Pareto frontier.
- **Rate matching solver**: Integer-programming algorithm that sets the prefill-to-decode GPU ratio to balance phase throughputs under latency SLO constraints, replacing the static ratios used in prior systems.
- **Elastic scaling**: Dynamic adjustment of the context-to-generation GPU ratio as traffic patterns shift; necessary because the optimal ratio varies substantially with model size and request mix.
- **Chunked Pipeline Parallelism (CPP)**: Splits context (prefill) processing into pipeline-parallel chunks on Blackwell GPUs, enabling long-context requests within first-token latency budgets without requiring wide tensor parallelism.
- Deployed within NVIDIA Dynamo; the study yields actionable deployment guidance — disaggregation excels for prefill-heavy, larger-model workloads and adds overhead for decode-dominated traffic.

## Trade-offs

- For generation-heavy or short-context workloads, piggybacking (co-located prefill and decode) outperforms disaggregation; the added scheduling and KV-transfer overhead is not amortized.
- Maintaining two separate GPU pools requires an elasticity layer to rebalance ratios; static disaggregated deployments can strand capacity on either the prefill or decode side.
- Results are normalized and presented as trends; specific throughput numbers are deliberately withheld to avoid making configuration-specific claims.

## Nuances

- Evaluations use Blackwell (FP4) hardware; disaggregation's cost-benefit calculus may differ on Hopper or older platforms with different NVLink topologies and memory bandwidth.
- The paper does not deeply evaluate KV-cache migration costs between prefill and decode nodes, which can dominate at large sequence lengths.
- "Hundreds of thousands of design points" is a sweep, not a production workload trace; real-world multi-modal traffic mixes may not align with the evaluated patterns.