---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2601.05296
authors:
- Jiyuan Zhang
- Yining Liu
- Siqi Yan
- Lisen Deng
- Jennifer Cao
- Shuqi Yang
- Bi Xue
- Min Ni
- Shen Li
award: ''
citations: 0
citations_updated: '2026-05-24'
code_url: ''
date: '2026-05-21'
domain:
- recs-models
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
observations:
- cpu-memory-tradeoff
- fusion-reduces-bandwidth
key_results: Over 4× speedup and over 50% memory savings compared to existing MoE
  training frameworks; deployed in Meta recommendation production
mlsys_official_category: Research Papers
mlsys_url: https://mlsys.org/virtual/2026/oral/3826
models_evaluated: []
openreview_url: https://openreview.net/forum?id=L8qKfWWkry
organizations:
- Meta
presentation_type: oral
problem: 'Mixture-of-Experts models face a memory wall during training: expert weights
  and activation buffers exceed GPU HBM capacity as model scale increases.'
project_url: ''
reading_status: read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3826_TlhaaTE.pdf
slug: moeblaze
topics:
- moe
- kernel-fusion
- cpu-offload
title: 'MoEBlaze: Breaking the Memory Wall for Efficient MoE Training on Modern GPUs'
---

## Summary

MoE (Mixture-of-Experts) models use conditional computation — only a subset of experts are activated per token — making them parameter-efficient at inference but memory-intensive at training because all expert weights must reside in memory (for gradients). MoEBlaze breaks this memory wall through an end-to-end redesign of token dispatch and MoE training:

- **Optimized token dispatch data structures**: Reduces overhead from routing tokens to experts, which involves complex scatter/gather patterns
- **Specialized fused kernels**: Fuse expert computation with routing and communication steps to reduce memory pressure
- **CPU offload for inactive experts**: Non-activated expert weights are offloaded to CPU memory, with prefetching to hide latency

The combination achieves over 4× speedup and 50%+ memory savings, with production deployment in Meta's recommendation systems.

## Key Contributions

- End-to-end MoE training system targeting the memory wall
- Optimized token dispatch data structures for expert routing
- Fused kernels for expert compute + routing
- CPU offload for inactive experts with latency hiding
- Production deployment at Meta

## Method

The token dispatch phase uses compact, cache-friendly data structures to batch tokens headed to the same expert. Fused kernels combine the expert linear layers with the routing scatter/gather. For memory savings, experts not in the current batch's top-k are speculatively offloaded to CPU pinned memory, with background prefetch based on predicted routing.

## Results

- Over 4× speedup vs. existing MoE frameworks
- Over 50% memory savings
- Deployed in Meta recommendation production

## Limitations

- CPU offload latency hiding depends on routing predictability
- Results may be specific to recommendation model MoE topology (sparse, many small experts) vs. LLM MoE (fewer, larger experts)

## Personal Notes

<!-- Add your own observations, questions, and connections to other work here -->