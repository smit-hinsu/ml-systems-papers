---
agentic_models: []
arxiv_date: 2025-11
arxiv_url: https://arxiv.org/abs/2511.21513
authors:
- Wanli Zhong
- Haibo Feng
- Zirui Zhou
- Hanyang Peng
- Shiqi Yu
award: ''
citations: 1
citations_updated: '2026-07-31'
code_url: https://github.com/WanliZhong/IntAttention
domain:
- edge-inference
- hardware
hardware:
- Armv8 CPUs
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 3.7× speedup and 61% energy reduction vs. FP16 baseline; 2.0× speedup
  vs. conventional INT8 attention pipeline on Armv8 CPUs
models_evaluated:
- Transformer language models
- Vision transformers
observations:
  fuse: IntAttention eliminates the dequantize-softmax-requantize detour consuming
    65% of attention latency, keeping the attention path in integer domain and removing
    FP type-conversion memory round-trips.
  quantize: All attention operations — Q/K/V projection and softmax — run in INT8/INT4
    without dequantization; the fully integer pipeline eliminates format-conversion
    overhead at every boundary.
  simplify: The float-domain softmax detour inserted to enable INT8 attention consumes
    65% of latency — the conversion stage costs more than the quantized compute it
    enables.
official_category: ''
openreview_url: https://openreview.net/forum?id=CPCRITwAaP
optimization_type: []
organizations:
- Southern University of Science and Technology
presentation_type: oral
principles:
- quantize
- simplify
principles_review:
- fuse
problem: INT8 attention on edge hardware still requires float softmax, causing a dequantize-softmax-requantize
  detour that dominates up to 65% of attention latency.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3848.pdf
slug: intattention-a-fully-integer-attention-pipeline-for-efficien
status: draft
title: 'IntAttention: A Fully Integer Attention Pipeline for Efficient Edge Inference'
topics:
- attention-kernels
- quantization
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3848
---

## Key Contributions

- **IndexSoftmax operator**: A hardware-friendly integer-domain softmax replacement that uses sparsity-aware clipping, a 32-entry lookup table for exponential approximation, and direct integer normalization to eliminate all floating-point operations in the attention path.
- **Fully integer attention pipeline**: IntAttention is a training-free drop-in replacement for the entire attention path (QK matmul, softmax, AV matmul) in INT8, removing the dequantize→softmax→requantize detour that dominated prior INT8 attention latency.
- **Sparsity-aware clipping**: Identifies and clips near-zero attention scores before LUT lookup, reducing average LUT accesses and further cutting the indexing overhead.

## Trade-offs

- The 32-entry LUT introduces approximation error in the softmax computation; the paper reports strong overall fidelity but does not characterize worst-case accuracy on adversarial inputs.
- IntAttention is validated on Armv8 CPUs; performance benefits on other edge ISAs (RISC-V, DSPs) are not evaluated and may differ due to varying LUT and integer pipeline characteristics.

## Nuances

- The 3.7× speedup is over FP16, not over conventional INT8 with float softmax; the 2.0× gain over conventional INT8 better reflects the incremental benefit of eliminating the softmax detour.
- The system is training-free, meaning it can be applied post-hoc to any INT8-quantized Transformer model without fine-tuning.
