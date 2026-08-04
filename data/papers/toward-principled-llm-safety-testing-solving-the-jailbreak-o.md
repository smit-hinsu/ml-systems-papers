---
agentic_models: []
arxiv_date: ''
arxiv_url: https://arxiv.org/abs/2506.17299
authors:
- Shuyi Lin
- Anshuman Suri
- Alina Oprea
- Cheng Tan
award: ''
citations: 4
citations_updated: '2026-07-31'
code_url: https://github.com/shuyilinn/BOA
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: BOA 2-phase search certifies LLM jailbreak absence above a user-set probability
  threshold more reliably than prior methods, enabling reproducible auditing
models_evaluated: []
observations:
  search-ai: BOA frames jailbreak detection as a verifiable oracle problem with a
    probability threshold, allowing AI-guided search to systematically solve a measurable
    security objective.
official_category: ''
openreview_url: https://openreview.net/forum?id=vr3Rrg6Xnm
optimization_type: []
organizations:
- Northeastern University
presentation_type: oral
principles:
- search-ai
problem: No systematic method exists to determine if an LLM can generate a jailbreak
  above a probability threshold, making security assessment unprincipled.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3739.pdf
slug: toward-principled-llm-safety-testing-solving-the-jailbreak-o
status: draft
title: 'Toward Principled LLM Safety Testing: Solving the Jailbreak Oracle Problem'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3739
---

## Background

Red-teaming finds individual jailbreaks but guarantees nothing: one example says nothing about how many others exist, and finding none says nothing about safety. Under adversarial decoding the output space grows exponentially with sequence length, so exhaustive search is out. The unasked question is not "can we find a jailbreak" but "does this model produce one with probability above a threshold?" — which has an auditable, reproducible answer.

## Key Contributions

- **Jailbreak oracle problem formalization**: defines the problem as: given a model, prompt, and decoding strategy, determine whether a jailbreak response can be generated with likelihood exceeding a specified threshold — enabling principled, reproducible security assessments.
- **BOA (Breadth-first + depth-first search Oracle Approach)**: two-phase search system — (1) breadth-first sampling identifies easily accessible jailbreaks quickly, (2) depth-first priority search guided by fine-grained safety scores systematically explores low-probability but high-risk paths in the exponentially large response space.
- **Model certification framework**: enables rigorous model certification by determining a lower bound on the probability that a model can be jailbroken under adversarial decoding, supporting standardized red-team comparisons and defense evaluations.
- Code available at https://github.com/shuyilinn/BOA/tree/mlsys2026ae.

## Trade-offs

- The depth-first priority search is guided by a fine-grained safety scorer; if the scorer is miscalibrated, high-risk paths may be deprioritized, producing false certifications.
- The exponential response space means BOA provides probabilistic rather than absolute guarantees; certification at very low probability thresholds requires extensive search budget.

## Nuances

- The oracle formalization assumes a fixed decoding strategy; jailbreak probability under adaptive or model-specific decoding (e.g., nucleus sampling with different temperatures) changes the oracle answer and may not be covered by a single evaluation.
- "Model certification under extreme adversarial conditions" is a strong claim; the practical meaning of "certified" here is bounded by the computational search budget, not a formal proof.
