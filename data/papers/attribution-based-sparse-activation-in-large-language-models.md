---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Jifeng Song
- Xiangyu Yin
- Boyuan Yang
- Kai Huang
- Weichen Liu
- Wei Gao
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
organizations:
- University of Pittsburgh
- Huazhong University of Science and Technology
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 70% model sparsity with <5% accuracy loss on QA and text summarization;
  35% latency reduction and 40% memory reduction for LLM inference
models_evaluated: []
observations:
  skip: New attribution metric corrects interdependency errors in existing
    scores; 70% neuron deactivation with <5% accuracy loss enables 35% latency and
    40% memory reduction without model retraining.
  balance: Input-dependent sparse activation selects the neuron subset
    at runtime per token, keeping GPU computation focused on high-attribution neurons
    while idle FLOPS from zero-attribution neurons are skipped.
official_category: ''
openreview_url: https://openreview.net/forum?id=gJFigZeb5D
presentation_type: oral
principles:
- skip
- balance
problem: LLM inference is expensive due to large parameter counts; existing lossless
  sparse activation only deactivates zero-output neurons and is ineffective on modern
  high-efficiency LLMs where near-zero neurons are rare.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: attribution-based-sparse-activation-in-large-language-models
status: draft
title: Attribution-based Sparse Activation in Large Language Models
topics:
- sparse-attention
- quantization
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3779
---

## Key Contributions

- **Attribution-based sparse activation**: lossy neuron deactivation technique that skips neurons with low attribution scores rather than only zero-output neurons, achieving high sparsity on modern LLMs that existing lossless methods cannot reach
- **Corrected attribution metric**: formal analysis showing that existing attribution metrics have large errors for sparse activation due to inter-neuron attribution score interdependencies; new metric provably corrects these errors to enable accurate neuron selection
- **Runtime adaptability**: input-dependent neuron selection adapts to each input at inference time without model retraining, making it usable across different downstream tasks without fine-tuning
- **70% sparsity with <5% accuracy loss**: demonstrated on difficult generative tasks (question answering, text summarization), delivering 35% latency and 40% memory reductions

## Trade-offs

- Lossy activation introduces task-dependent accuracy degradation; the <5% threshold holds for QA and summarization but may not hold for tasks requiring precise numerical reasoning or exact recall.
- Per-input attribution scoring adds overhead relative to lossless zero-detection; net latency savings depend on the ratio of activation computation to neuron selection cost.

## Nuances

- The attribution metric's correctness guarantee applies to the specific interdependency model described; architectures with different activation structures (e.g., gated linear units) may require metric re-derivation.
- "Runtime adaptability" means no retraining but still requires running the attribution scoring pass; this pass is not free and its cost is not fully quantified in the abstract.
