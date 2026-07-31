---
agentic_models: []
arxiv_date: 2025-10
arxiv_url: https://arxiv.org/abs/2510.18784
authors:
- Soroush Tabesh
- Mher Safaryan
- Andrei Panferov
- Alexandra Volkova
- Dan Alistarh
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
hardware:
- GPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: CAGE halves compression accuracy loss vs prior best method; W3A3 Llama
  accuracy matches W4A4 with QuEST at similar compute cost.
models_evaluated:
- Llama (W3A3, W4A4)
observations:
  quantize: CAGE corrects STE gradient bias using curvature from Adam second-moment
    statistics; the correction enables W3A3 models to match W4A4 accuracy without
    extra training passes.
official_category: ''
openreview_url: https://openreview.net/forum?id=Fubm1TtWeo
optimization_type: []
organizations:
- Institute of Science and Technology Austria (ISTA)
presentation_type: oral
principles:
- quantize
problem: Straight-through estimator in QAT introduces gradient bias from quantization
  discontinuities, leaving an accuracy gap vs full-precision training.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3841_N6ZwMw7.pdf
slug: cage-curvature-aware-gradient-estimation-for-accurate-quanti
status: draft
title: 'CAGE: Curvature-Aware Gradient Estimation For Accurate Quantization-Aware
  Training'
topics:
- quantization
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3841
---

## Key Contributions

- **CAGE (Curvature-Aware Gradient Estimation)**: Augments the straight-through estimator with a curvature-aware correction term derived from a multi-objective view of QAT, reducing the loss increase induced by quantization.
- **Pareto-optimal QAT theory**: Introduces the notion of Pareto-optimal solutions for quantized optimization and proves convergence guarantees for CAGE in the smooth non-convex setting.
- **Adam-statistics implementation**: Leverages existing Adam second-moment statistics for efficient curvature estimation with no additional compute overhead beyond standard QAT.

## Trade-offs

- CAGE's correction term depends on Adam optimizer statistics, so it requires an Adam-family optimizer; SGD or other optimizers need separate curvature estimation.
- The multi-objective formulation adds a balancing hyperparameter between loss minimization and quantization constraint adherence.

## Nuances

- The W3A3 matching W4A4 result specifically uses QuEST as the W4A4 baseline; other baselines may show different relative gaps.
- CAGE is optimizer-agnostic in principle but the efficient implementation specifically targets Adam statistics.