---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Zhen Zheng
- Xiaonan Song
- Chuanjie Liu
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/microsoft/MixLLM
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Perplexity increase for Llama 3.1 70B reduced from ~0.5 (SOTA) to within
  0.2; MMLU-Pro loss cut from 1.92 to 0.99 with only 10% more bits
models_evaluated:
- Llama-3.1-70B
observations:
  quantize: Bit-width is allocated layer by layer, but the output features that carry
    the accuracy are spread unevenly across the whole model, so a per-layer budget
    overpays cheap layers.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=VBbMRQ4VOc
organizations:
- Microsoft
presentation_type: oral
principles:
- quantize
problem: Mixed-precision quantization prior work either sacrifices accuracy or achieves
  low system efficiency; both matter for production LLM deployment.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3805.pdf
slug: mixllm-llm-quantization-with-global-mixed-precision-between-
status: draft
title: 'MixLLM: LLM Quantization with Global Mixed-precision between Output-features
  and Highly-efficient System Design'
topics:
- quantization
- kernel-fusion
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3805
---

## Key Contributions

- **Global output-feature sensitivity ranking**: identifies important output features across all layers simultaneously rather than per-layer, allocating higher bit-width only to features that most affect accuracy; achieves sweet-spot accuracy with minimal extra bits
- **Two-step dequantization kernel**: separates quantized weight loading from precision conversion, enabling Tensor Core utilization without costly format-mismatch overhead during MatMul
- **Software pipeline for overlap**: schedules memory access, dequantization, and MatMul in a pipelined fashion so HBM reads are hidden behind active computation, reaching state-of-the-art system efficiency
- With only 10% more bits vs. SOTA, reduces Llama 3.1 70B perplexity increase from ~0.5 to within 0.2 and MMLU-Pro loss from 1.92 to 0.99 across three popular models

## Trade-offs

- Global sensitivity analysis requires a full cross-layer pass before quantization; per-layer methods that can be applied layer-by-layer are more incremental and easier to pipeline.
- The bit-width assignment is determined offline and fixed at deployment; dynamic workloads with varying accuracy requirements cannot adapt without rerunning the assignment.