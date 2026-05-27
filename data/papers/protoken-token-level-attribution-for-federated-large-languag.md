---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Waris Gill
- Ahmad Humayun
- Ali Anwar
- Muhammad Ali Gulzar
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 98.62% average attribution accuracy across 16 configurations spanning
  4 LLM architectures and 4 domains in federated settings.
models_evaluated:
- Gemma
- Llama
- Qwen
- SmolLM
observations:
  skip: Transformer architectures concentrate task-specific signals in
    later blocks; ProToken selects only those layers for attribution, reducing computation
    vs. full-model attribution.
  cache: Gradient-based relevance weighting filters irrelevant neuron
    activations, focusing attribution on neurons that directly influence each token
    generation rather than scoring all activations.
official_category: ''
openreview_url: https://openreview.net/forum?id=8WXUjbFr0Z
organizations:
- Virginia Tech
- University of Minnesota
presentation_type: oral
principles:
- skip
- cache
problem: Federated LLMs lack token-level attribution, making it impossible to identify
  which client contributed to a specific generated response.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: protoken-token-level-attribution-for-federated-large-languag
status: draft
title: 'ProToken: Token-Level Attribution for Federated Large Language Models'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3850
---

## Background

In federated learning, clients train locally and share only gradients. For LLMs this raises a data provenance question: if the model generates a harmful response, which client's data caused it? Standard attribution methods work at the dataset or sample level, but LLM generation is token-by-token — a single response may draw on contributions from multiple clients across different tokens. No prior approach attributes individual generated tokens to specific federated clients.

## Key Contributions

- **ProToken attribution framework**: token-level provenance for federated LLMs during autoregressive generation; attributes each generated token to its responsible client while preserving FL privacy constraints
- **Strategic layer selection**: exploits the observation that transformer task-specific signals concentrate in later blocks; limits attribution computation to those layers for tractability
- **Gradient-based relevance weighting**: filters neural activations by gradient magnitude to focus attribution on neurons that directly influence each token, reducing noise from irrelevant activations
- Evaluated across 16 configurations (4 LLM architectures × 4 domain datasets: medical, financial, mathematical, coding); achieves 98.62% attribution accuracy and maintains accuracy as client count scales

## Trade-offs

- Attribution requires per-token gradient computation, which adds inference overhead beyond standard federated LLM generation.
- Layer selection heuristic (later blocks) may vary across architectures; different model families may require re-calibration of the selection strategy.

## Nuances

- Evaluation is on controlled FL settings; real-world deployment with heterogeneous and potentially adversarial clients may introduce noise that reduces attribution accuracy.
- Privacy analysis against gradient inversion or membership inference attacks is not detailed in the abstract.
