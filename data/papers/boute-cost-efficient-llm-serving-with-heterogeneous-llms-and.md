---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2602.10729
authors:
- Youhe Jiang
- Fangcheng Fu
- Eiko Yoneki
award: ''
citations: 6
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-serving
- fleet-efficiency
hardware:
- Heterogeneous GPU cluster
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: BOute improves throughput by up to 157% and reduces cost by 15-61% vs
  existing systems under identical quality and latency constraints.
models_evaluated:
- Heterogeneous LLMs
observations:
  balance: Heterogeneous GPU deployment routes simple queries to cheaper GPUs and
    models, keeping high-end GPUs busy with complex queries.
  cache: MOBO jointly searches routing strategy and model deployment config, avoiding
    the sub-optimality of tuning each independently.
official_category: ''
openreview_url: https://openreview.net/forum?id=ZVQb92umqX
optimization_type: []
organizations:
- University of Cambridge
- Shanghai Jiao Tong University
presentation_type: oral
principles:
- cache
- balance
problem: Co-optimizing query routing across heterogeneous LLMs and GPU deployment
  configs is too complex for manual tuning, leaving significant cost savings unrealized.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3795.pdf
slug: boute-cost-efficient-llm-serving-with-heterogeneous-llms-and
status: draft
title: 'BOute: Cost-Efficient LLM Serving with Heterogeneous LLMs and GPUs via Multi-Objective
  Bayesian Optimization'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3795
---

## Key Contributions

- **BOute (Bayesian Optimization for routing)**: A quality-aware scheduling system that co-optimizes query routing strategy and heterogeneous model deployment using multi-objective Bayesian optimization (MOBO).
- **Joint optimization**: Simultaneously determines which queries go to which model/GPU tier while allocating parallelism and resources, respecting latency SLOs and quality thresholds.

## Trade-offs

- MOBO search has non-trivial overhead for initial configuration; the benefit amortizes over long deployment periods.
- Quality guarantees depend on accurate quality routing predictors, which may degrade on out-of-distribution query types.

## Nuances

- The 157% throughput improvement is the peak case; the average improvement is 59% under identical cost budgets.
- Cost reduction of 38% on average targets maintaining the same performance targets — a different optimization axis than throughput maximization.
