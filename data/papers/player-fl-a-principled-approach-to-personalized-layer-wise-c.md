---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Ahmed Elhussein
- Florent Pollet
- "Gamze Gürsoy"
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Consistently competitive performance across diverse architectures; federation-sensitivity
  metric computed from a single training epoch identifies the optimal layer split point
models_evaluated: []
observations:
  balance: Federating only the early, generalizable layers avoids synchronizing
    task-specific layers across clients; this splits the parameter space so that
    federation benefits only where global aggregation helps, not where it hurts.
  cache: Computing the federation-sensitivity metric after a single
    epoch avoids full training runs for split-point search; one lightweight pass
    is sufficient to identify the generalizable-to-task-specific transition.
official_category: ''
openreview_url: https://openreview.net/forum?id=QBUy1HdKrZ
organizations:
- Columbia University
presentation_type: oral
principles:
- balance
- cache
problem: Existing partial FL methods rely on ad-hoc architecture-specific heuristics
  for choosing which layers to federate, causing inconsistent performance and client
  regressions on non-IID data.
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

## Key Contributions

- **Federation-sensitivity metric**: novel per-layer score quantifying each layer's robustness to gradient aggregation, inspired by model pruning sensitivity analysis; computed efficiently after a single training epoch without full training runs
- **Principled split-point selection**: uses the federation-sensitivity metric to locate the transition between generalizable (safe-to-federate) and task-specific (stay-local) layers; the metric correlates strongly with established generalization measures across diverse architectures
- **Systematic layer-wise generalization analysis**: first characterization of when and how the generalizable-to-task-specific transition emerges early in FL training, providing theoretical grounding for partial FL methods
- Achieves consistently competitive performance across a wide range of tasks while reducing client-side regressions relative to ad-hoc partial FL baselines

## Trade-offs

- The metric is computed after one epoch, which may be unreliable for very small datasets or highly non-IID distributions where early-epoch gradients are noisy.
- The method assumes a single contiguous split point; architectures with irregular skip connections or attention mechanisms may require multi-region federation strategies.
