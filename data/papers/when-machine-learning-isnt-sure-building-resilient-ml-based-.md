---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Varun Gohil
- Nevena Stojkovic
- Noman Bashir
- Sundar Dev
- Gaurang Upasani
- David Lo
- Parthasarathy Ranganathan
- Christina Delimitrou
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- fleet-efficiency
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Uncertainty-aware rejection improves resilience across 3 case studies
  (server provisioning, cluster management, storage I/O) by filtering unreliable ML
  calls.
models_evaluated: []
observations:
  balance: Falling back to safe strategies when prediction uncertainty is high prevents
    ML-driven misconfigurations that would cause resource imbalance or admission failures
    in production.
  search-ai: The framework quantifies prediction uncertainty at runtime to determine
    when ML outputs are trustworthy, enabling ML to solve measurable system objectives
    only within its reliable operating envelope.
official_category: ''
openreview_url: https://openreview.net/forum?id=i0iOQL2MF5
organizations:
- Cornell University
- Meta
- Google
presentation_type: oral
principles:
- balance
- search-ai
problem: ML models in computer systems fail silently on out-of-distribution inputs,
  causing costly failures when predictions are applied without uncertainty awareness.
project_url: ''
reading_status: want-to-read
research_or_industry: mixed
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3772_bJ5i4pq.pdf
slug: when-machine-learning-isnt-sure-building-resilient-ml-based-
status: draft
title: 'When Machine Learning Isn’t Sure: Building Resilient ML-Based Computer Systems
  by Embracing Uncertainty'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3772
---

## Background

ML models make operational decisions — server provisioning, job routing, I/O admission control — trained on historical telemetry that drifts over time. New application versions, traffic changes, and hardware upgrades create out-of-distribution inputs where predictions can be badly wrong. Unlike a bad recommendation, incorrect system control predictions cascade: an underprovisioned server causes latency spikes, a misrouted job starves a cluster. Standard models produce confident-looking outputs even on OOD inputs, so failures are silent until they cause visible damage.

## Key Contributions

- **Uncertainty-aware framework for ML-driven systems**: a general approach that quantifies prediction uncertainty at runtime, rejects unreliable outputs, and gracefully degrades to a safe fallback strategy — applicable across diverse system ML tasks.
- **Cross-task uncertainty estimator evaluation**: systematic study finding that no single uncertainty estimator (e.g., Bayesian, ensemble, conformal) universally dominates; the best estimator depends on how its properties align with each task's design and resource constraints.
- **Task-specific fallback design**: demonstrates that the optimal fallback workflow (lightweight/parallel vs. resource-intensive/sequential) depends on the runtime latency constraints of each task, guiding practical deployment decisions.
- Evaluated across three case studies: server provisioning, cluster management, and storage I/O admission; the framework consistently improves resilience by rejecting OOD inputs before they cause harmful actions.

## Findings

- The best uncertainty estimator is not universal; task-specific properties (label space, OOD frequency, latency budget) determine which estimator should be deployed.
- Fallback strategy design is non-trivial: parallel lightweight fallbacks suit latency-sensitive tasks while sequential resource-intensive fallbacks suit accuracy-critical tasks with loose latency budgets.
- Across all three case studies, uncertainty-aware rejection prevents the majority of ML-driven system failures attributable to OOD inputs.

## Trade-offs

- Uncertainty quantification adds inference overhead per prediction; for high-frequency system decisions (e.g., per-request scheduling), the overhead may be prohibitive without careful implementation.
- Fallback strategies sacrifice the ML model's efficiency gains when triggered; high OOD rates in production can negate the benefits of ML-driven optimization entirely.

## Nuances

- The three case studies are from specific production contexts (server provisioning, cluster management, storage); generalization to other ML-driven system tasks (e.g., network routing, query optimization) requires per-task uncertainty estimator and fallback evaluation.
- "Costly failures" from OOD inputs are not quantified with specific numbers in the abstract; the severity of failures avoided varies by task.