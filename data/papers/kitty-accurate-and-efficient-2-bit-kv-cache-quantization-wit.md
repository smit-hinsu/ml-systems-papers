---
agentic_models: []
arxiv_date: '2025-11-23'
arxiv_url: '2511.18643'
authors:
- Haojun Xia
- Xiaoxia Wu
- Jisen Li
- Tsai-chuan Wu
- Junxiong Wang
- Jue WANG
- Chenxi Li
- Aman Singhal
- Alay Dilipbhai Shah
- Alpay Ariyak
- Donglin Zhuang
- Zhongzhu Zhou
- Ben Athiwaratkun
- Zhen Zheng
- Shuaiwen Leon Song
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/Summer-Summer/Kitty
domain:
- llm-serving
hardware:
- GPU (CUDA/Triton)
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Nearly 8× KV memory reduction; up to 8× larger batches and 2.1×–4.1×
  higher throughput on Qwen3 and LLaMA3 vs. 4-bit KV under same memory budget
models_evaluated:
- Qwen3
- LLaMA3
observations:
  fuse: Page-centric KV layout decomposes mixed-precision Key pages into two unified
    2-bit tensors, enabling coalesced memory reads and removing scattered access patterns
    that harm HBM bandwidth utilization.
  quantize: 2-bit KV quantization identifies per-channel outliers and preserves them
    at higher precision; mixed-precision cuts KV memory 4× vs FP16 with <1% accuracy
    degradation on Llama-3.
  skip: Channel-wise Precision Boost ranks Key-cache channels by sensitivity, keeps
    a small fraction at 4-bit, and quantizes insensitive channels at 2-bit — avoiding
    accuracy loss from applying uniform 2-bit.
official_category: ''
openreview_url: https://openreview.net/forum?id=r3mQiuYKIN
organizations:
- Cornell University
- University of Washington
presentation_type: oral
principles:
- skip
- fuse
- quantize
problem: 2-bit KV cache quantization degrades LLM accuracy, especially on long-context
  reasoning, while 4-bit preserves accuracy but limits batch size gains.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3746.pdf
slug: kitty-accurate-and-efficient-2-bit-kv-cache-quantization-wit
status: under-review
title: 'Kitty: Accurate and Efficient 2-bit KV Cache Quantization with Dynamic Channel-wise
  Precision Boost'
topics:
- kv-cache
- quantization
- memory-management
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3746
---

## Background

KV cache quantization compresses key/value memory by storing at lower bit-width. 4-bit preserves accuracy while halving memory vs. FP16, but 2-bit (which would halve it again) degrades quality sharply on long-context reasoning. The root cause is Key-cache **outlier channels** — a small fraction of channels with much larger magnitude that uniform 2-bit quantization collapses, destroying attention distributions.

## Key Contributions

- **Dynamic Channel-wise Precision Boost**: Ranks Key-cache channels by per-channel sensitivity; only the most sensitive channels are kept at 4-bit while the rest are quantized to 2-bit, achieving near-zero accuracy drop while approaching full 2-bit memory density.
- **Page-centric KV layout**: Decomposes each mixed-precision Key page into two unified 2-bit tensors, preserving coalesced memory access and avoiding scattered reads from mixing 2-bit and 4-bit data within a single page.
- **Triton-compatible dequantization kernels**: Lightweight runtime pipeline with Triton kernels for page dequantization that incurs negligible overhead, enabling dynamic channel boost decisions without throughput penalty.

## Trade-offs

- The channel sensitivity ranking must be computed per model and potentially per dataset; adaptive re-ranking at serving time adds latency compared to static 4-bit quantization.
- Only Key cache channels benefit from the precision boost; Value cache is uniformly 2-bit, which may limit accuracy on tasks where Value cache sensitivity is high.

## Nuances

- Results are validated across 7 tasks on Qwen3 and LLaMA3; generalization to other model families or extreme long-context settings (>128K tokens) is not evaluated.
- The 4.1× throughput gain is the upper bound; the 2.1× lower bound reflects cases where compute rather than memory is the bottleneck and the batch size increase provides less benefit.