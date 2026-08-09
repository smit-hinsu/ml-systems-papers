---
agentic_models: []
arxiv_date: 2025-12
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
citations: 9
citations_updated: '2026-07-31'
code_url: ''
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
observations:
  simplify: Prior sparse attention needs a training or profiling pass to predict skippable
    blocks, yet the online-softmax loop already computes the running max that answers
    the question for free.
  approximate: Once softmax normalizes, a tile whose local max sits far below the
    running max adds almost nothing to the output, and how far below is a threshold
    that buys sparsity against accuracy.
official_category: ''
openreview_url: https://openreview.net/forum?id=6INSBXTQ4x
optimization_type: []
organizations:
- Rice University
- UC Davis
- NVIDIA
presentation_type: oral
principles:
- approximate
- simplify
problem: Dense softmax is O(n²) and prohibitively slow beyond 32K tokens; sparse alternatives
  require training or profiling — blocking drop-in deployment.
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
