---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
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
organizations:
- University of Illinois Urbana-Champaign
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Consistently higher speedups than static approximation strategies on
  3 compound AI systems combining LLMs with retrieval and tool calling; discovers
  Pareto-optimal accuracy-performance trade-off points
models_evaluated: []
observations:
  skip: approx MLIR dialect expresses approximation choices for both ML
    and non-ML components (LLM sampling, retrieval heuristics) in a unified IR; approx-opt
    explores the space to skip computation whose accuracy cost is within budget.
  cache: End-to-end compilation of compound systems lets approxMLIR
    discover cross-component approximations (e.g., skip retrieval when LLM confidence
    is high) that per-component optimizers cannot see.
official_category: ''
openreview_url: https://openreview.net/forum?id=nKm25GWbuB
presentation_type: oral
principles:
- skip
- cache
problem: Compound AI systems mixing LLMs and non-ML components (RAG, tool calling)
  have no unified way to trade accuracy for performance across both component types,
  leaving cross-component optimization opportunities unexploited.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: approxmlir-accuracy-aware-compiler-for-compound-ml-system
status: draft
title: 'ApproxMLIR : Accuracy-Aware Compiler for Compound ML System'
topics:
- prefix-caching
- quantization
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3757
---

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
