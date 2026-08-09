---
agentic_models: []
arxiv_date: 2025-02
arxiv_url: https://arxiv.org/abs/2502.08829
authors:
- Ahmed Elhussein
- Florent Pollet
- Gamze Gürsoy
award: ''
citations: 2
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Competitive FL accuracy with 1-epoch split-point search vs. ad-hoc partial
  FL baselines across diverse architectures and non-IID data splits
models_evaluated: []
observations: {}
official_category: ''
openreview_url: https://openreview.net/forum?id=QBUy1HdKrZ
optimization_type: []
organizations:
- Columbia University
presentation_type: oral
principles: []
problem: Partial FL methods use ad-hoc heuristics for layer federation choice, causing
  inconsistent performance and client regressions on non-IID data.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: player-fl-a-principled-approach-to-personalized-layer-wise-c
status: draft
title: 'PLayer-FL: A Principled Approach to Personalized Layer-wise Cross-Silo Federated
  Learning'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3813
---

## Background

Federated learning trains across clients without centralizing data, but on non-IID data full-model aggregation overwrites layers tuned to each client's distribution. Partial FL federates only the early general-purpose layers and keeps later ones local. Where to split has been picked by intuition — freeze the last N layers — with inconsistent results across architectures.

## Key Contributions

- **Federation-sensitivity metric**: novel per-layer score quantifying each layer's robustness to gradient aggregation, inspired by model pruning sensitivity analysis; computed efficiently after a single training epoch without full training runs
- **Principled split-point selection**: uses the federation-sensitivity metric to locate the transition between generalizable (safe-to-federate) and task-specific (stay-local) layers; the metric correlates strongly with established generalization measures across diverse architectures
- **Systematic layer-wise generalization analysis**: first characterization of when and how the generalizable-to-task-specific transition emerges early in FL training, providing theoretical grounding for partial FL methods
- Achieves consistently competitive performance across a wide range of tasks while reducing client-side regressions relative to ad-hoc partial FL baselines

## Trade-offs

- The metric is computed after one epoch, which may be unreliable for very small datasets or highly non-IID distributions where early-epoch gradients are noisy.
- The method assumes a single contiguous split point; architectures with irregular skip connections or attention mechanisms may require multi-region federation strategies.
