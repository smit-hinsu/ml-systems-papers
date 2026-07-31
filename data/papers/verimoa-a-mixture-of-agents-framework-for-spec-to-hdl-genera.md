---
agentic_models:
- Multiple LLM backbones (GPT-4, smaller models)
arxiv_date: ''
arxiv_url: 'https://arxiv.org/abs/2510.27617'
authors:
- Heng Ping
- Arijit Bhattacharjee
- Peiyu Zhang
- Shixuan Li
- Wei Yang
- Anzhe Cheng
- Xiaole Zhang
- Jesse Thomason
- Ali Jannesari
- Nesreen Ahmed
- Paul Bogdan
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 15–30% improvement in Pass@1 on VerilogEval 2.0 and RTLLM 2.0 benchmarks
  across diverse LLM backbones without any training.
models_evaluated: []
observations:
  cache: Quality-guided caching retains all intermediate HDL outputs and ranks them
    across reasoning layers; subsequent agents reuse high-quality prior outputs instead
    of starting from scratch.
  search-ai: Multi-path generation through C++ and Python intermediates and quality-guided
    selection optimizes a verifiable objective (HDL correctness) by exploring diverse
    solution paths and selecting the best.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=5wgZXJ0kWA
organizations:
- University of Southern California
- Iowa State University
- Intel Labs
presentation_type: oral
principles:
- cache
- search-ai
problem: LLM-based HDL generation suffers from noise propagation across agent layers
  and limited solution diversity, limiting correctness on complex RTL specifications.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3855_j54FoJa.pdf
slug: verimoa-a-mixture-of-agents-framework-for-spec-to-hdl-genera
status: draft
title: 'VeriMoA: A Mixture-of-Agents Framework for Spec-to-HDL Generation'
topics:
- llm-code-generation
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3855
---

## Background

Verilog is the register-transfer-level language synthesis tools compile into silicon. Correct code expresses hardware parallelism, timing, and bit-level behavior at once, and small mistakes yield circuits that silently compute the wrong thing. LLMs do poorly here because Verilog is rare in training data next to Python or C++. Mixture-of-Agents (MoA) chains several LLM calls for refinement, but passing every output forward propagates early errors and collapses solution diversity.

## Key Contributions

- **VeriMoA framework**: training-free mixture-of-agents (MoA) system for spec-to-HDL generation with two synergistic mechanisms: quality-guided caching and multi-path generation, enabling 15–30% Pass@1 improvement on VerilogEval 2.0 and RTLLM 2.0.
- **Quality-guided caching mechanism**: maintains all intermediate HDL outputs across reasoning layers; ranks outputs by quality and feeds the best candidates into subsequent agents, preventing noise propagation by selecting against low-quality intermediates.
- **Multi-path generation strategy**: uses C++ and Python as intermediate representations to decompose spec-to-HDL translation into two stages; exploits LLM fluency in high-resource languages to promote solution diversity and reduce reliance on Verilog-specific training data.
- Enables smaller models to match larger models and fine-tuned alternatives without costly training; demonstrates that training-free multi-agent reasoning can substitute for domain-specific fine-tuning in hardware design.

## Trade-offs

- Multi-path generation through C++ and Python intermediates adds inference latency proportional to the number of paths; the throughput cost per design is higher than single-agent generation.
- Quality-guided caching maintains all intermediate outputs in memory; for very long or complex specifications, memory usage grows with the number of reasoning layers.

## Nuances

- The 15–30% Pass@1 improvement is measured on VerilogEval 2.0 and RTLLM 2.0 benchmarks; these benchmarks may not fully represent the difficulty distribution of production RTL specifications.
- The claim that smaller models can match larger models is backbone-dependent; the specific model sizes and comparison points are not detailed in the abstract.