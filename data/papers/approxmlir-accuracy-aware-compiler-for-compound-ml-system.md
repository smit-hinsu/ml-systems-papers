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
  approximate: A compound system has quality knobs in both its ML and non-ML parts,
    and quality given up cheaply in retrieval buys compute back in the LLM, but no
    compiler could see both ends at once.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=nKm25GWbuB
organizations:
- University of Illinois Urbana-Champaign
presentation_type: oral
principles:
- approximate
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