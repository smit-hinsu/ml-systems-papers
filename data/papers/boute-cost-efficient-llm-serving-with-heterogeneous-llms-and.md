---
slug: boute-cost-efficient-llm-serving-with-heterogeneous-llms-and
title: "BOute: Cost-Efficient LLM Serving with Heterogeneous LLMs and GPUs via Multi-Objective Bayesian Optimization"
authors:
- Youhe Jiang
- Fangcheng Fu
- Eiko Yoneki
organizations:
- University of Cambridge
- Shanghai Jiao Tong University
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3795
openreview_url: https://openreview.net/forum?id=ZVQb92umqX
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
- llm-serving
- fleet-efficiency
hardware:
- Heterogeneous GPU cluster
models_evaluated:
- Heterogeneous LLMs
agentic_models: []
topics: []
principles:
- cache
- balance
observations:
  cache: "MOBO jointly searches routing strategy and model deployment config, avoiding the sub-optimality of tuning each independently."
  balance: "Heterogeneous GPU deployment routes simple queries to cheaper GPUs and models, keeping high-end GPUs busy with complex queries."
problem: "Co-optimizing query routing across heterogeneous LLMs and GPU deployment configs is too complex for manual tuning, leaving significant cost savings unrealized."
key_results: "BOute improves throughput by up to 157% and reduces cost by 15-61% vs existing systems under identical quality and latency constraints."
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
