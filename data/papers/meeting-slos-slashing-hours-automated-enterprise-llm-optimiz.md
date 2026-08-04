---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Nicholas Santavas
- Kareem Eissa
- Patrycja Cieplicka
- Piotr Florek
- Matteo Nulli
- Stefan Vasilev
- Seyyed Hadi Hashemi
- Antonios Gasteratos
- Shahram Khadivi
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: More than 2× GPU throughput improvement in production deployment; reduces
  model optimization from hours of manual effort to automated pipeline execution
models_evaluated: []
observations: {}
official_category: ''
openreview_url: https://openreview.net/forum?id=om4H7AI2hc
optimization_type: []
organizations:
- eBay
- Democritus University of Thrace
presentation_type: oral
principles: []
problem: Enterprise teams lack LLM optimization expertise to compress models within
  GPU budgets, leaving utilization low across heterogeneous infrastructure.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3752.pdf
slug: meeting-slos-slashing-hours-automated-enterprise-llm-optimiz
status: draft
title: 'Meeting SLOs, Slashing Hours: Automated Enterprise LLM Optimization with OptiKIT'
topics:
- quantization
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3752
---

## Key Contributions

- **OptiKIT framework**: distributed LLM optimization system that automates compression and tuning workflows (quantization, pruning, distillation) for non-expert application teams without requiring deep ML optimization expertise
- **Dynamic resource allocator**: assigns optimization jobs to available GPUs across heterogeneous infrastructure, balancing load and adapting to cluster state during multi-day pipeline runs
- **Staged pipeline with automatic cleanup**: checkpoint-driven execution that resumes from the last completed stage on failure and discards intermediate artifacts, reducing redundant compute and storage overhead
- **Enterprise integration layer**: REST API and monitoring hooks for seamless integration with existing deployment pipelines; production-deployed at eBay achieving >2× GPU throughput improvement

## Trade-offs

- Automated optimization pipelines reduce expert control; teams must trust the system's hyperparameter choices, which may not be optimal for every model or use case.
- The multi-stage pipeline introduces end-to-end latency before an optimized model is ready; interactive or iterative optimization workflows are not supported.