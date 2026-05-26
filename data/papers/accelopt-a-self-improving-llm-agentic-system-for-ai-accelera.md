---
agentic_models:
- Claude Sonnet 4
arxiv_url: https://arxiv.org/abs/2511.15915
arxiv_date: '2025-11'
authors:
- Genghan Zhang
- Shaowei Zhu
- Anjiang Wei
- Zhenyu Song
- Allen Nie
- Zhen Jia
- Nandita Vijaykumar
- Yida Wang
- Kunle Olukotun
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/zhang677/AccelOpt
domain:
- ml-kernels
organizations:
- Stanford University
- Amazon
hardware:
- Trainium
- H100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Improves NKIBench kernels from 49% to 61% peak throughput on Trainium
  1; matches Claude Sonnet 4 quality at 26× lower cost using open-source models
models_evaluated: []
observations:
  search-ai: Agentic beam search explores kernel optimization space with
    memory of slow-fast kernel pairs; each iteration distills insights into an optimization
    memory, enabling measurable improvement across iterations on NKIBench.
  cache: Optimization memory caches generalizable insights from prior
    slow-fast kernel pairs, preventing the LLM planner from re-discovering the same
    strategies on subsequent kernels.
official_category: ''
openreview_url: https://openreview.net/forum?id=SBS4NJHYjZ
organizations:
- Stanford University
- Amazon
presentation_type: oral
principles:
- search-ai
- cache
problem: Emerging AI accelerators (Trainium, custom ASICs) lack expert-written optimized
  kernels; manual tuning requires deep hardware knowledge unavailable at scale.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: accelopt-a-self-improving-llm-agentic-system-for-ai-accelera
status: draft
title: 'AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization'
topics:
- autotuning
- llm-code-generation
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3808
---

## Key Contributions

- **Three-agent agentic workflow**: planner agent generates optimization strategies, executor agent implements them, summarizer agent distills insights from profiling feedback; together they drive iterative beam search over the kernel optimization space without requiring hand-written hardware expertise
- **Optimization memory**: accumulates slow-fast kernel pairs and LLM-generated summaries of generalizable optimization insights; guides future iterations to avoid re-discovering known dead ends and builds compound improvement across runs
- **NKIBench**: new benchmark of AWS Trainium accelerator kernels with varying complexity extracted from real LLM workloads; covers Trainium 1 and 2 with theoretical peak throughput as the evaluation target
- **Self-improving convergence**: average peak throughput improves from 49% → 61% on Trainium 1 and 45% → 59% on Trainium 2 across iterations; open-source model variant matches Claude Sonnet 4 quality at 26× lower API cost

## Trade-offs

- Beam search with iterative LLM calls incurs significant wall-clock time and token cost per kernel; only cost-effective when the optimized kernel is used many times.
- Optimization memory quality degrades for kernels with novel structure not represented in prior slow-fast pairs; cold-start performance on entirely new operator types is weaker.

## Nuances

- The benchmark focuses on NKI (Neuron Kernel Interface) for Trainium; generalization to other accelerator ISAs or Triton targets on different hardware requires retraining the memory from scratch.
- "Self-improving" refers to improvement across iterations within a single optimization run, not continual online learning across separate deployments.
