---
agentic_models: []
arxiv_date: 2025-10
arxiv_url: https://arxiv.org/abs/2510.17899
authors:
- Floris-Jan Willemsen
- Niki van Stein
- Ben van Werkhoven
award: ''
citations: 1
citations_updated: '2026-07-31'
code_url: ''
domain:
- ml-compilers
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Best LLM-generated optimizer achieves 72.4% improvement over human-designed
  baselines on 4 apps (GEMM, convolution, hotspot, dedispersion) across 6 GPUs.
models_evaluated: []
observations:
  search-ai: LLMs synthesize and refine auto-tuning search algorithms using application-
    and search-space descriptions; performance vs. near-optimal configurations is
    the verifiable signal driving improvement.
official_category: ''
openreview_url: https://openreview.net/forum?id=qKlHJCbY6m
optimization_type: []
organizations:
- Leiden University
- Netherlands eScience Center
presentation_type: oral
principles:
- search-ai
problem: Auto-tuning search spaces are vast and irregular; manually designed optimizers
  miss hardware-specific structure, leaving significant performance on the table.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3748_4D9zX0g.pdf
slug: automated-algorithm-design-for-auto-tuning-optimizers
status: draft
title: Automated Algorithm Design for Auto-Tuning Optimizers
topics:
- autotuning
- llm-code-generation
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3748
---

## Key Contributions

- **LLM-driven optimizer synthesis**: framework that prompts LLMs with problem descriptions and search space characteristics to generate, test, and iteratively refine specialized optimization algorithms for auto-tuning, replacing manually designed evolutionary/surrogate baselines
- **Application-specific knowledge injection**: providing application- and search-space-specific context during generation yields 30.7% and 14.6% performance improvements respectively over generic prompting, demonstrating that domain context is load-bearing
- **State-of-the-art result on 4 applications, 6 platforms**: best-performing LLM-generated optimizer achieves 72.4% average improvement over existing state-of-the-art auto-tuning algorithms; evaluated in two contemporary auto-tuning frameworks
- **Iterative refinement loop**: generated algorithms are evaluated on real hardware, with feedback used to guide the next generation iteration; convergence mirrors human expert algorithm design process but runs automatically

## Trade-offs

- LLM synthesis costs real tokens and wall-clock time upfront; the approach is only cost-effective when the generated optimizer will be reused across many tuning runs on the same application.
- Generated optimizers are specialized to the problem they were designed for; reusing a generated algorithm on a structurally different application or search space may yield poor results.

## Nuances

- The 72.4% improvement is for the best-performing generated algorithm; median improvement and variance across LLM runs are not highlighted in the abstract.
- Evaluation uses two specific auto-tuning frameworks; coverage of other popular frameworks (e.g., OpenTuner, Optuna) is not characterized.
