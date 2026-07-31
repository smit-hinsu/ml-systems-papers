---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Armin Abdollahi
- Mehdi Kamal
- Massoud Pedram
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- ml-compilers
- hardware
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 9.4 percentage point improvement in pass rate at 10% tolerance over prior
  methods, with ~20× higher throughput (0.12 s per design).
models_evaluated: []
observations:
  cache: At 0.12 s per design vs. minutes-long synthesis runs, RocketPPA avoids the
    redundant work of full tool invocations during early-stage design space exploration.
  search-ai: RocketPPA uses an LLM with MoE regression and contrastive learning to
    predict PPA metrics—a verifiable hardware design objective—enabling fast design-space
    search without full synthesis.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=lpO7kxiayb
organizations:
- University of Southern California
presentation_type: oral
principles:
- search-ai
- cache
problem: Fast surrogate models for Verilog PPA prediction lack accuracy across technology
  nodes; slow synthesis runs block early design-space exploration.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3761.pdf
slug: unified-llm-model-for-power-performance-and-area-prediction-
status: draft
title: Unified LLM Model for Power, Performance, and Area Prediction from Hardware
  Code
topics:
- llm-code-generation
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3761
---

## Background

Getting PPA (power, performance, area) for Verilog RTL means running logic synthesis — Synopsys DC or Cadence Genus — which takes minutes to hours per design, far too slow to rank thousands of candidates during early exploration. Surrogate models predict PPA straight from source, but prior ones use hand-crafted features or small networks that don't transfer across technology nodes (15 nm vs. 45 nm) or synthesis optimization styles, so every configuration needs its own retrained model.

## Key Contributions

- **RocketPPA**: unified LLM-based surrogate model for PPA prediction of Verilog designs; combines an LLM backbone with mixture-of-experts regression heads and LoRA for parameter-efficient fine-tuning across multiple technology nodes and optimization styles.
- **Contrastive learning framework**: trains the model to cluster semantically similar hardware designs in embedding space, providing an inductive bias that reflects the structure of the hardware design space and improving generalization across unseen designs.
- **Cross-regime generalization**: trained on 15 nm and 45 nm nodes with area- and delay-optimized flows; leave-one-regime-out experiments show robust cross-regime performance with minimal degradation.
- Achieves 9.4 percentage point improvement in pass rate at 10% PPA tolerance over prior methods; throughput of 0.12 s per design is approximately 20× faster than prior approaches, enabling rapid design-space exploration.
- Ablation: contrastive learning contributes 2.5 percentage points of accuracy improvement independently.

## Trade-offs

- The model is trained on 15 nm and 45 nm technology nodes; generalization to sub-7 nm nodes or advanced packaging (chiplets, 3D ICs) is not validated and may require retraining.
- LLM backbone inference at 0.12 s per design is fast relative to synthesis but still slower than analytical or regression-based models; very large design spaces (millions of candidates) may still be bottlenecked.

## Nuances

- "Pass rate at 10% tolerance" measures how often the predicted PPA is within 10% of synthesis results; designs outside this tolerance may still lead to incorrect design decisions.
- The contrastive learning framework requires semantic similarity labels for Verilog designs; automated similarity labeling at scale is not trivial and may introduce label noise.