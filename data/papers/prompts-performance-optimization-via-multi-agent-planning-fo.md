---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Yuran Ding
- Ruobing Han
- Xiaofan Zhang
- Xinwei Chen
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
- llm-serving
hardware:
- TPU
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Top recommendation matched production config in 87.5% of cases; up to
  434% perf improvement across 8 workloads on 2–512 TPU chips.
models_evaluated: []
observations:
  balance: Analyzer Agent diagnoses bottlenecks by synthesizing profiler data; Proposal
    Agent generates sharding configs that eliminate idle compute from tensor/pipeline
    parallelism imbalance.
  search-ai: Multi-agent RAG framework identifies expert-validated sharding configs
    within top-3 recommendations in a single invocation across 8 real LLM workloads
    on TPU clusters.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=FTOfgVHcZn
organizations:
- Google
presentation_type: oral
principles:
- search-ai
- balance
problem: Optimizing LLM training/serving sharding configs on large TPU clusters requires
  deep expertise or expensive black-box search.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3843.pdf
slug: prompts-performance-optimization-via-multi-agent-planning-fo
status: draft
title: 'PROMPTS: PeRformance Optimization via Multi-Agent Planning for LLM Training
  and Serving'
topics:
- tensor-parallelism
- pipeline-parallelism
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3843
---

## Key Contributions

- **Analyzer Agent**: diagnoses performance bottlenecks by synthesizing profiler traces; identifies sharding misconfigurations across tensor/pipeline/data-parallel dimensions without manual inspection
- **Proposal Agent with RAG**: leverages a knowledge base of optimization strategies to generate ranked sharding configurations with detailed justifications via retrieval-augmented generation
- **Multi-agent framework (PROMPTS)**: integrates LLM-based reasoning with expert knowledge to reduce optimization search cost; validated on 8 real-world MoE and dense LLM workloads spanning 2–512 TPU chips on 2D/3D Torus interconnects
- Framework covers full LLM lifecycle (pre-training, post-training, serving) and matches expert-validated production configs within top-3 recommendations in a single invocation

## Trade-offs

- RAG quality depends on the completeness of the knowledge base; configurations for novel hardware topologies or architectures not in the knowledge base may degrade recommendation quality.
- Framework is validated on TPU clusters; applicability to GPU clusters with NVLink/InfiniBand interconnects is not directly evaluated.

## Nuances

- The 434% improvement figure represents the best case across workloads; average improvement is not separately stated in the abstract.
- "Single invocation" contrasts with iterative black-box search methods; total token cost of the agent invocation is not characterized.
- Organizations are not explicitly stated in the available metadata.