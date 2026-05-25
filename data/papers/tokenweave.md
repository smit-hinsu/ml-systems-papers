---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2505.11329
authors:
- Raja Gond
- Nipun Kwatra
- Ramachandran Ramjee
award: ''
citations: 0
citations_updated: '2026-05-24'
code_url: https://github.com/microsoft/tokenweave
date: '2026-05-19'
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
observations:
- fusion-reduces-bandwidth
- communication-compute-overlap
key_results: Up to 1.28× latency speedup, up to 1.19× higher throughput via fused
  AllReduce–RMSNorm kernel
mlsys_official_category: Research Papers
mlsys_url: https://mlsys.org/virtual/2026/oral/3744
models_evaluated: []
openreview_url: https://openreview.net/forum?id=rh2Ylffkq6
organizations:
- Microsoft
presentation_type: oral
problem: In tensor-parallel LLM inference, AllReduce communication between GPUs is
  on the critical path and cannot be hidden, limiting throughput.
project_url: ''
reading_status: read
research_or_industry: research
slides_url: ''
slug: tokenweave
topics:
- tensor-parallelism
- kernel-fusion
- communication-overlap
- all-reduce
title: 'TokenWeave: Efficient Compute-Communication Overlap for Distributed LLM Inference'
---

## Summary

In tensor-parallel inference, each transformer layer requires an AllReduce collective to synchronize partial results across GPUs. This communication is on the critical path: the next layer cannot start until AllReduce completes. TokenWeave attacks this with a fused kernel that combines AllReduce and RMSNorm into a single operation, leveraging modern GPU features (likely NVLink topology awareness and in-network compute).

The key insight is that **the work immediately following AllReduce (RMSNorm) can be partially overlapped with the in-flight AllReduce**, by having GPUs begin normalizing the partial results they already have while waiting for remaining shards. This is made possible by a carefully designed fused kernel that pipelines the two operations.

## Key Contributions

- Fused AllReduce–RMSNorm kernel exploiting modern GPU interconnect features
- Token-level overlapping of communication with normalization computation
- Demonstrated gains across multiple model sizes and workloads

## Method

The fused kernel proceeds as follows: as each GPU receives partial AllReduce results from its peers, it immediately begins the RMSNorm computation on the received portion. This hides part of the AllReduce latency behind useful computation. The kernel requires careful synchronization to ensure correctness while maximizing overlap.

## Results

- Up to 1.28× speedup in latency
- Up to 1.19× higher throughput
- Tested across various models and inference workloads

## Limitations

- Gains are limited by the fraction of time spent in AllReduce (Amdahl's law)
- May require hardware-specific tuning for different interconnect topologies (NVLink vs. InfiniBand)
- Evaluation hardware not specified

## Personal Notes

<!-- Add your own observations, questions, and connections to other work here -->