---
agentic_models: []
arxiv_url: https://arxiv.org/abs/2511.19269
arxiv_date: '2025-11'
authors:
- Minseo Kim
- Chenfeng Xu
- Coleman Hooper
- Harman Singh
- Ben Athiwaratkun
- Ce Zhang
- Kurt Keutzer
- Amir Gholami
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/SqueezeAILab/CDLM
domain:
- llm-serving
hardware:
- A100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 14.5× latency reduction on MBPP and 11.2× on GSM8K vs. baseline DLMs on
  A100, with competitive accuracy vs. AR models
models_evaluated:
- Dream-7B-Instruct
- LLaDA-8B-Instruct
observations:
  cache: Block-wise causal attention mask enables standard KV caching
    in diffusion LMs; previously each denoising step re-computed all positions from
    scratch, making caching impossible.
  pipeline: Consistency distillation enables multi-token finalization
    per step, reducing total denoising steps by 4.1×–7.7× and letting the model finalize
    multiple tokens in one forward pass.
official_category: ''
openreview_url: https://openreview.net/forum?id=eB8yjR6alL
organizations:
- UC Berkeley
- Snowflake
- ETH Zurich
presentation_type: oral
principles:
- cache
- pipeline
problem: Diffusion language models require dozens of iterative denoising steps and
  cannot use KV caching, making inference 10–15× slower than autoregressive models.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: cdlm-consistency-diffusion-language-models-for-faster-sampli
status: under-review
title: 'CDLM: Consistency Diffusion Language Models for Faster Sampling'
topics:
- kv-cache
- speculative-decoding
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3785
---

## Key Contributions

- **Consistency distillation training**: fine-tunes a diffusion LM (Dream-7B, LLaDA-8B) with a forward-KL distillation objective on unmasked positions plus a consistency term on still-masked tokens, enabling multi-token finalization per denoising step and reducing required steps by 4.1×–7.7×
- **Block-wise causal attention mask**: replaces the standard bidirectional mask with a block-causal structure during fine-tuning, making the model fully compatible with standard KV caching and eliminating redundant attention recomputation across denoising steps
- **LoRA-based adaptation**: achieves full CDLM training in 8–16 hours on 4× A100 GPUs via LoRA, making the method accessible without full fine-tuning
- **End-to-end speedup**: 3.6×–14.5× latency reduction over baseline DLMs on math and coding benchmarks while maintaining accuracy competitive with autoregressive LLMs of comparable size

## Trade-offs

- The block-wise causal mask trades the full bidirectional context of standard diffusion LMs for caching efficiency; tasks that benefit most from global context (e.g., long-range reasoning) may see slight accuracy regressions.
- Consistency distillation requires a teacher model (the original DLM), adding training complexity; the method does not apply to DLMs without a strong teacher checkpoint.

## Nuances

- Results are evaluated on Dream-7B and LLaDA-8B; generalization to larger diffusion LMs (30B+) or different masking schedules is not validated.
- Speedup figures (3.6×–14.5×) are relative to unoptimized baseline DLMs, not the fastest autoregressive serving systems; DLMs still lag behind optimized AR inference at equal parameter count.
