---
agentic_models: []
arxiv_url: ''
authors:
- Shanli Xing
- Vivian Zhai
- Alexander Jiang
- Yixin Dong
- Yong Wu
- Zihao Ye
- Charlie Ruan
- Yingyi Huang
- Yineng Zhang
- Liangsheng Yin
- Aksara Bayyapu
- Luis Ceze
- Tianqi Chen
award: ''
citations: null
citations_updated: ''
code_url: ''
date: '2026-05-20'
domain:
- llm-serving
- ml-compilers
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
insights:
- kernel-verifiability
key_results: Standardized kernel schema + public leaderboard + dynamic substitution
  into SGLang and vLLM production systems
mlsys_official_category: Research Papers
mlsys_url: https://mlsys.org/virtual/2026/oral/3832
models_evaluated: []
openreview_url: https://openreview.net/forum?id=IyryZno8Hh
organizations:
- University of Washington
- Carnegie Mellon University
presentation_type: oral
problem: There is no standardized feedback loop connecting kernel generation, benchmarking,
  and production deployment for LLM inference kernels.
project_url: ''
reading_status: read
research_or_industry: research
slides_url: ''
slug: flashinfer-bench
techniques:
- kernel-fusion
- autotuning
title: 'FlashInfer-Bench: Building the Virtuous Cycle for AI-driven LLM Systems'
---

## Summary

FlashInfer-Bench creates a **virtuous cycle** between three activities that are currently siloed: (1) AI-driven kernel generation, (2) systematic benchmarking, and (3) production deployment. The key insight is that kernel performance is a verifiable problem — you can score a generated kernel objectively — and that this property should be exploited to build a continuous improvement loop.

The system introduces:
- **FlashInfer Trace**: A unified schema for kernel definitions and workload descriptions
- A curated workload dataset representing realistic LLM inference patterns
- Benchmarking infrastructure and a public leaderboard
- A **dynamic substitution mechanism** that lets newly-optimized kernels be swapped into live production systems (SGLang, vLLM) without code changes

## Key Contributions

- FlashInfer Trace schema unifying kernel definition and workload description
- Curated benchmark dataset for LLM inference kernels
- Public leaderboard creating competitive pressure to improve kernels
- Dynamic kernel substitution into SGLang and vLLM

## Method

The system defines a standard interface for kernels: inputs, outputs, and performance metrics. A kernel author writes a spec (FlashInfer Trace), submits it to the benchmark harness, gets a score, and can optionally push a winning kernel into production systems via the substitution API. AI-generated kernels can participate in the same pipeline.

## Results

- Framework demonstration with integration into SGLang and vLLM
- Public leaderboard shows measurable quality signal for kernel generation models

## Limitations

- Coverage of kernel types not fully characterized
- Generalizability beyond attention/FlashInfer kernel family unclear

## Personal Notes

<!-- Add your own observations, questions, and connections to other work here -->