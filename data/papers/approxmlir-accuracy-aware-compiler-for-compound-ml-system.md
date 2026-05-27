---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Hao Ren
- Yi Mu
- Sasa Misailovic
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-compilers
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Higher speedups than static approximation on 3 compound AI systems (LLM+retrieval,
  LLM+tools); finds Pareto-optimal accuracy-performance trade-offs.
models_evaluated: []
observations:
  cache: End-to-end compilation of compound systems lets approxMLIR discover cross-component
    approximations (e.g., skip retrieval when LLM confidence is high) that per-component
    optimizers cannot see.
  skip: approx MLIR dialect expresses approximation choices for ML and non-ML components
    in a unified IR; approx-opt searches the joint space to skip work whose accuracy
    cost stays within budget.
official_category: ''
openreview_url: https://openreview.net/forum?id=nKm25GWbuB
organizations:
- University of Illinois Urbana-Champaign
presentation_type: oral
principles:
- skip
- cache
problem: Compound AI systems (LLM+RAG, tool calling) have no unified way to trade
  accuracy for performance, leaving cross-component optimization unexploited.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3757.pdf
slug: approxmlir-accuracy-aware-compiler-for-compound-ml-system
status: draft
title: 'ApproxMLIR : Accuracy-Aware Compiler for Compound ML System'
topics:
- prefix-caching
- quantization
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3757
---

## Background

Compound AI systems (LLM + RAG, LLM + tool calls) can be approximated at many points — quantize the LLM, skip retrieval on high-confidence queries, use cheaper tool policies — but these choices interact. Existing ML compilers optimize single neural networks with no way to express an accuracy budget spanning an LLM and a retrieval engine in one IR, forcing cross-component trade-offs to be found by hand-tuning. The result: individually reasonable approximations combine unexpectedly to breach quality constraints.

## Key Contributions

- **approx MLIR dialect**: unified IR extension that represents approximation choices for both ML components (LLM sampling temperature, quantization) and non-ML components (retrieval heuristics, tool call policies) in a single compilation framework
- **approx-opt optimizer**: MLIR-based pass that searches the joint accuracy-performance trade-off space across components, discovering Pareto-optimal configurations that static per-component strategies miss
- **Cross-component accuracy accounting**: formal model that tracks accuracy budget across the full compound system pipeline, enabling the compiler to safely trade quality in cheap components to save computation in expensive ones
- **Three compound AI system evaluations**: applied to systems combining LLMs with information retrieval and tool calling; consistently achieves higher speedups than static approximation strategies while staying within accuracy constraints

## Trade-offs

- Accuracy accounting requires a ground-truth accuracy oracle or proxy metric; compound systems without well-defined output quality metrics (e.g., open-ended generation) are harder to optimize.
- The approx MLIR dialect requires porting each system component to the MLIR toolchain; existing LLM serving frameworks with custom CUDA kernels need non-trivial integration work.

## Nuances

- "Consistently higher speedups" is a relative claim against static approximation baselines; absolute speedup numbers are not provided in the abstract.
- The paper targets batch/offline compound system workloads; interactive latency-sensitive serving with strict per-request deadlines may limit approximation aggressiveness.