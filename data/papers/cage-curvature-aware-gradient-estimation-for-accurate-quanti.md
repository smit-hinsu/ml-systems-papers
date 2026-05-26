---
slug: cage-curvature-aware-gradient-estimation-for-accurate-quanti
title: "CAGE: Curvature-Aware Gradient Estimation For Accurate Quantization-Aware Training"
authors:
- Soroush Tabesh
- Mher Safaryan
- Andrei Panferov
- Alexandra Volkova
- Dan Alistarh
organizations:
- Institute of Science and Technology Austria (ISTA)
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3841
openreview_url: https://openreview.net/forum?id=Fubm1TtWeo
arxiv_url: ''
presentation_type: oral
official_category: ''
award: ''
status: draft
reading_status: want-to-read
research_or_industry: research
indexed_by: smithinsu
indexed_date: '2026-05-24'
citations: null
citations_updated: ''
code_url: ''
project_url: ''
slides_url: ''
domain:
- llm-training
hardware:
- GPU
models_evaluated:
- Llama (W3A3, W4A4)
agentic_models: []
topics:
- quantization
principles:
- cache
observations:
  cache: "Curvature-aware correction reuses Adam second-moment statistics already computed during training to estimate local curvature with no extra passes."
problem: "Straight-through estimator in QAT introduces gradient bias from quantization discontinuities, leaving an accuracy gap vs full-precision training."
key_results: "CAGE halves compression accuracy loss vs prior best method; W3A3 Llama accuracy matches W4A4 with QuEST at similar compute cost."
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
