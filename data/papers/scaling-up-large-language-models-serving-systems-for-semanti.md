---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Kayhan Behdin
- Qingquan Song
- Sriram Vasudevan
- Jian Sheng
- Xiaojing Ma
- Z Zhou
- Chuanrui Zhu
- Guoyao Li
- Chanh Nguyen
- Sayan Ghosh
- Hejian Sang
- Ata Fatahi
- Sundara Raman Ramachandran
- Xiaoqing Wang
- Qing Lan
- Vinay Y S
- Qi Guo
- Caleb Johnson
- Zhipeng Wang
- Fedor Borisyuk
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
- recs-models
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 10x throughput increase in production at LinkedIn serving millions of
  requests/sec; 40% model size reduction via pruning with maintained accuracy.
models_evaluated: []
observations:
  cache: Context compression reduces input context length by >10x with minimal accuracy
    loss, cutting prefill compute and KV cache memory per request.
  fuse: Pruning reduces model size by up to 40%, decreasing weight load per forward
    pass and reducing HBM bandwidth pressure during serving.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=re82zZczHj
organizations:
- LinkedIn
presentation_type: oral
principles:
- cache
- fuse
problem: Deploying LLMs for semantic job search at LinkedIn is prohibitively expensive
  due to strict latency/throughput requirements at millions of requests per second.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3745_jivse2G.pdf
slug: scaling-up-large-language-models-serving-systems-for-semanti
status: draft
title: Scaling Up Large Language Models Serving Systems for Semantic Job Search
topics:
- quantization
- prefix-caching
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3745
---

## Background

LinkedIn's job search must rank millions of listings against user profiles in real time — millions of requests per second with strict latency budgets. LLMs dramatically outperform traditional embedding models on semantic matching, but even a small decoder-only LLM is expensive per request: prefill cost scales with input length, and naive deployment would require far more GPUs than cost-per-click economics justify.

## Key Contributions

- **Structured model pruning**: reduces decoder-only SLM size by up to 40% while maintaining relevance ranking accuracy for semantic job search; enables deployment on fewer GPUs
- **Context compression**: compresses input context length by more than 10× with minimal accuracy loss, dramatically reducing prefill compute cost and KV cache size per request
- **GPU serving infrastructure optimization**: practical lessons from deploying the compressed model at scale on GPUs; achieves 10× throughput improvement over the baseline serving system in production
- System serves millions of requests per second at LinkedIn, handling strict latency and throughput SLAs for a text-based decoder-only architecture

## Findings

- Model compression (pruning + context compression) enables 10× throughput improvement while meeting the quality bar for production semantic search.
- Context compression delivering >10× reduction with minimal accuracy loss is achievable for domain-specific search tasks.

## Trade-offs

- Context compression is task-specific; compression strategies optimized for semantic job search may not transfer to open-ended generation tasks.
- Structured pruning requires retraining/fine-tuning to recover accuracy; upfront training cost must be amortized over production serving lifetime.

## Nuances

- The 10× throughput improvement combines model compression and serving infrastructure optimizations; the individual contribution of each component is not broken down in the abstract.
- "Minimal accuracy loss" is measured on LinkedIn's internal relevance benchmarks; absolute accuracy degradation thresholds are proprietary.