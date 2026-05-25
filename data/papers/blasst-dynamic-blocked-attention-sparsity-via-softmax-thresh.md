---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2512.12087
authors:
- Jiayi Yuan
- Cameron Shinn
- Kai Xu
- Jingze Cui
- George Klimiashvili
- Guangxuan Xiao
- Perkz Zheng
- Bo Li
- Zhou Yuxin
- Zhouhai Ye
- Weijie You
- Tian Zheng
- Dominic Brown
- Pengbo Wang
- Markus Hoehnerbach
- Richard Cai
- Julien Demouth
- John D. Owens
- Xia Hu
- Song Han
- Timmy Liu
- Huizi Mao
award: ''
citations: null
citations_updated: ''
code_url: ''
date: 2026-05
domain:
- llm-serving
- ml-kernels
hardware:
- NVIDIA H200
- NVIDIA B200
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 1.62× prefill and 1.48× decode speedup at ~74% sparsity on H200/B200
  with Llama-3.1 and DeepSeek-R1; integrated into TensorRT-LLM and FlashInfer.
models_evaluated:
- Llama-3.1-8B
- Llama-3.1-70B
- Qwen3-8B
- Qwen3-30B
- DeepSeek-R1
principles:
- exploit-sparsity
- reduce-data-movement
observations:
  exploit-sparsity: At 74% average sparsity across Llama-3.1 and Qwen3 long-context
    benchmarks, most attention blocks contribute negligibly to output after softmax
    normalization and can be skipped without accuracy loss.
  reduce-data-movement: Skipping negligible attention blocks eliminates value-block
    HBM loads and the attention-value matmul; at 74% sparsity, bandwidth freed
    dominates the speedup more than compute reduction.
official_category: ''
openreview_url: https://openreview.net/forum?id=6INSBXTQ4x
organizations: []
presentation_type: oral
problem: Long-context LLM inference requires full attention over all tokens; existing
  sparse methods need training, pre-computation, or per-head profiling, blocking
  drop-in deployment.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3854.pdf
slug: blasst-dynamic-blocked-attention-sparsity-via-softmax-thresh
status: draft
title: 'BLASST: Dynamic BLocked Attention Sparsity via Softmax Thresholding'
topics:
- sparse-attention
- kv-cache
- kernel-fusion
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3854
---

## Key Contributions

- **Softmax-threshold block-skip criterion**: During FlashAttention's online-softmax tile loop, if a tile's local maximum score satisfies `m̃ᵢ − m < ln(λ)`, its softmax weights are negligible after normalization and the entire tile — softmax ops, value-block HBM load, and attention-value matmul — is skipped without an extra profiling pass.
- **Single scalar threshold λ**: The only tuning parameter; an automated calibration procedure determines λ using the inverse relationship λ = a/L (where L is context length), enabling deployment without per-model or per-head tuning.
- **Universal attention variant support**: The block-skip mechanism is compatible with MHA, GQA, MQA, and MLA (used in DeepSeek-R1), requiring no architecture-specific modifications.
- **Optimized CUDA kernels**: Custom kernels expose the sparsity to the hardware scheduler; integrated as a drop-in replacement into TensorRT-LLM and FlashInfer with no changes to model weights or serving configuration.

## Trade-offs

- Block-level granularity means BLASST skips whole tiles; fine-grained token-level sparsity patterns within a tile cannot be exploited, leaving some compute savings on the table compared to token-level sparse attention.
- Sparsity variance across heads and layers is high; a single global threshold is suboptimal for heads with atypical attention distributions — the paper notes per-head thresholds could improve the accuracy-efficiency curve.
- At very high sparsity targets (>75%), accuracy degrades more steeply, bounding the useful operating range.

## Nuances

- Results are reported at model-average sparsity; individual layers (especially early ones) may show substantially lower sparsity, so worst-case latency for single layers is not fully characterized.
- Benchmarks are dominated by RULER and LongBench which favor retrieval tasks; tasks requiring dense attention across all tokens (e.g., multi-document reasoning) may see larger accuracy drops.
- The Blackwell (B200) prefill speedup is lower (1.33× at 50% sparsity) than Hopper; Blackwell's faster FP8 compute narrows the gap between dense and sparse paths.
