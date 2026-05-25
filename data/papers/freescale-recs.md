---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2604.24073
authors:
- Chenhao Feng
- Haoli Zhang
- Shakhzod Ali-zade
- Yanli Zhao
- Liang Luo
- Jennifer Cao
- Lisen Deng
- Siqiao Chen
- Chenyu Zhao
- Tristan Rice
- Daniel Johnson
- Min Si
- Tiantu Xu
- Yi Zhang
- Evgenii Kolpakov
- Siqi Yan
- Chuanhao Zhuge
- Min Ni
- Bi Xue
- Qunshu Zhang
- Shen Li
award: ''
citations: 0
citations_updated: '2026-05-24'
code_url: ''
date: '2026-05-21'
domain:
- recs-models
hardware:
- H100
indexed_by: smithinsu
indexed_date: '2026-05-24'
observations:
- straggler-bubbles
- communication-compute-overlap
key_results: Up to 90.3% reduction in computational bubbles on 256 H100 GPUs
mlsys_official_category: Research Papers
mlsys_url: https://mlsys.org/virtual/2026/oral/3821
models_evaluated: []
openreview_url: https://openreview.net/forum?id=MY0BIdK4hn
organizations:
- Meta
presentation_type: oral
problem: Large-scale training of sequence recommendation models wastes substantial
  compute due to stragglers, slow communication, and load imbalance.
project_url: ''
reading_status: read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3821_gs6415h.pdf
slug: freescale-recs
topics:
- communication-overlap
title: 'FreeScale: Distributed Training for Sequence Recommendation Models with Minimal
  Scaling Cost'
---

## Summary

Sequence recommendation models (think user history modeling at scale) present a distinct challenge from LLMs: they involve very large embedding tables and heterogeneous computation patterns that make distributed training inefficient at scale. FreeScale addresses three sources of waste simultaneously:

1. **Load-balanced input sampling**: Distributes sequence batches so each GPU gets similar total work, reducing stragglers
2. **Overlapped embedding communication**: Hides AllGather/ReduceScatter latency behind forward computation
3. **SM-Free communication**: Uses specialized GPU resources for collectives without competing with compute SMs

The combination of these reduces pipeline bubbles by up to 90.3% on 256 H100 GPUs.

## Key Contributions

- Load-balanced input sampling to reduce straggler bubbles in recommendation model training
- Compute-communication overlap strategy tailored to embedding-heavy workloads
- SM-Free communication method that avoids SM contention
- 90.3% reduction in computational bubbles at 256-GPU scale

## Method

The load balancing pass analyzes input sequences at the batch level and reorders them across workers to equalize per-worker compute. The embedding overlap is implemented by pipelining embedding lookup (which requires AllGather of sharded tables) with the dense model forward pass. SM-Free communication uses GPU DMA engines or peer memory rather than streaming multiprocessors.

## Results

- Up to 90.3% reduction in computational bubbles
- Tested on 256 H100 GPUs
- Production deployment at Meta

## Limitations

- Highly specific to embedding-heavy recommendation model topology
- Load balancing approach may not generalize to architectures without variable-length sequences

## Personal Notes

<!-- Add your own observations, questions, and connections to other work here -->