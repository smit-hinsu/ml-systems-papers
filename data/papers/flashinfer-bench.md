---
agentic_models: []
arxiv_date: 2026-01
arxiv_url: https://arxiv.org/abs/2601.00227
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
domain:
- ml-kernels
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: FlashInfer Trace schema + leaderboard + apply() injection into SGLang/vLLM;
  multiple LLM agents evaluated across 3 kernel classes (attention, GEMM, activation).
models_evaluated: []
observations:
  cache: Dynamic kernel substitution via apply() lets a winning kernel immediately
    replace the default in SGLang/vLLM without rewriting application code or re-running
    benchmarks
  fuse: Winning LLM-generated kernels are consistently fused attention or GEMM variants;
    the benchmark reveals that reducing HBM round-trips via fusion is the dominant
    lever agents converge on.
  search-ai: Kernel performance is objectively measurable via latency on real hardware,
    making it a tractable target for LLM agents competing on a public leaderboard
official_category: Research Papers
openreview_url: https://openreview.net/forum?id=IyryZno8Hh
optimization_type: []
organizations:
- University of Washington
- Carnegie Mellon University
presentation_type: oral
principles:
- search-ai
- cache
- fuse
problem: AI-generated kernels lack a benchmark against production workloads and a
  mechanism to inject them into live systems, breaking the generation-deployment loop.
project_url: ''
reading_status: read
research_or_industry: research
slides_url: ''
slug: flashinfer-bench
status: draft
title: 'FlashInfer-Bench: Building the Virtuous Cycle for AI-driven LLM Systems'
topics:
- autotuning
- llm-code-generation
- kernel-fusion
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3832
---

## Key Contributions

- **FlashInfer Trace schema**: unified representation for kernel definitions, workload descriptions, implementations, and evaluation results, enabling consistent communication between LLM agents and inference systems
- **Curated benchmark dataset**: production serving traces distilled into a representative set of LLM inference kernel workloads, covering attention, GEMM, and activation patterns
- **Public leaderboard**: tracks LLM agents' GPU programming quality on correctness- and performance-aware metrics, creating competitive pressure for kernel improvement
- **Dynamic apply() substitution mechanism**: injects the best-performing kernel from the leaderboard directly into running SGLang or vLLM instances without code changes, closing the generation-to-deployment loop
- Evaluation of multiple LLM agents reveals trade-offs between GPU programming languages (Triton vs. CUDA) and optimization strategies

## Trade-offs

- The framework is currently scoped to FlashInfer-style kernels (attention-centric); coverage of other operation classes (sparse ops, all-reduce) is not characterized
- Leaderboard competition assumes a fixed workload distribution; kernel winners may not generalize to out-of-distribution serving patterns

## Nuances

- No single numeric speedup is reported for the system itself — the value is infrastructure, not a specific performance gain, which makes it harder to evaluate impact
- The apply() substitution mechanism requires the production system to trust dynamically-loaded kernel code, raising safety and reproducibility concerns not discussed in the paper
- LLM agents that win the leaderboard may exploit dataset-specific patterns; whether they generalize to new hardware (e.g., Blackwell, AMD) is untested