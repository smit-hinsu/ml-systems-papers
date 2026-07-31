---
agentic_models: []
arxiv_date: 2025-11
arxiv_url: https://arxiv.org/abs/2511.11505
authors:
- Yonatan Dukler
- Guihong Li
- Deval Shah
- Jiang Liu
- Vikram Appia
- Emad Barsoum
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
- llm-training
hardware:
- GPU cluster
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: FarSkip-Collective achieves 32.6% TTFT speedup serving DeepSeek-V3, 97.3%
  comm-compute overlap in prefill, and <1% accuracy loss on Llama 4 Scout 109B.
models_evaluated:
- Llama 4 Scout (109B)
- DeepSeek-V3
observations:
  pipeline: Skip connections let later-layer compute begin before all-to-all MoE routing
    completes, achieving 97.3% communication-computation overlap during prefill.
official_category: ''
openreview_url: https://openreview.net/forum?id=ruOpvLzsGV
optimization_type: []
organizations:
- AMD
presentation_type: oral
principles:
- pipeline
problem: Blocking all-to-all MoE communication serializes compute in distributed inference
  and training, wasting GPU cycles at every expert routing boundary.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3743.pdf
slug: farskip-collective-unhobbling-blocking-communication-in-mixt
status: draft
title: 'FarSkip-Collective: Unhobbling Blocking Communication in Mixture of Experts
  Models'
topics:
- communication-overlap
- moe
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3743
---

## Key Contributions

- **FarSkip-Collective architecture**: Modifies MoE models by adding skip connections that enable overlapping all-to-all communication with computation from subsequent layers, without changing model capacity.
- **Self-distillation conversion**: Full conversion of large models (16B to 109B parameters) from blocking to non-blocking communication architectures via self-distillation, preserving accuracy within 1% of original.
- **Framework integration**: Optimized implementations in SGLang for inference that explicitly overlap communication with computation for both prefill and training.

## Trade-offs

- Skip connections alter the computation graph, so converted models are not drop-in replacements; checkpoints are incompatible with the original architecture.
- Self-distillation conversion requires additional training compute proportional to model size.

## Nuances

- The 97.3% overlap is measured during prefill; decode phase overlap may differ due to smaller batch sizes.
- Accuracy within 1% is measured on instruction-tuned Llama 4 Scout; base model accuracy gap may differ.