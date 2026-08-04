---
agentic_models: []
arxiv_date: 2025-12
arxiv_url: https://arxiv.org/abs/2512.07993
authors:
- Jiayi Tian
- Seyedarmin Azizi
- Yequan Zhao
- Erfan Baghaei Potraghloo
- Sean McPherson
- Sharath Nittur Sridhar
- Zhengyang Wang
- Zheng Zhang
- Massoud Pedram
- Souvik Kundu
award: ''
citations: 3
citations_updated: '2026-07-31'
code_url: https://github.com/TTTTTTris/SkipKV
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 26.7% accuracy gain vs. baseline KV eviction; 1.6x shorter generation
  and 1.7x throughput vs. per-token eviction methods at similar compression budget.
models_evaluated: []
observations:
  skip: Sentence-level scoring identifies and removes semantically similar CoT sentences
    entirely from KV cache, skipping both eviction and generation for redundant reasoning
    steps.
official_category: ''
openreview_url: https://openreview.net/forum?id=0EsV9SIm8p
optimization_type: []
organizations:
- University of Southern California
- Intel Labs
presentation_type: oral
principles:
- skip
problem: Large reasoning models produce verbose CoT responses causing linear KV cache
  growth; token-level eviction fails in multi-batch settings due to unstable scoring.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3864_lxfVaNQ.pdf
slug: skipkv-selective-skipping-of-kv-generation-and-storage-for-e
status: draft
title: 'SkipKV: Selective Skipping of KV Generation and Storage for Efficient Inference
  with Large Reasoning Models'
topics:
- kv-cache
- speculative-decoding
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3864
---

## Key Contributions

- **Sentence-level KV compression**: coarse-grained sentence-level removal of semantically similar CoT sentences, in contrast to per-token eviction; uses a sentence-scoring metric to identify and skip redundant reasoning steps
- **Steering vector adjustment**: dynamically adjusts a steering vector to update hidden activation states during inference, enforcing the LRM to generate concise responses and suppressing redundant token generation
- **Training-free deployment**: SkipKV requires no fine-tuning; operates on existing large reasoning models (e.g., DeepSeek-R1-style) as a drop-in inference optimization
- Achieves up to 26.7% higher accuracy vs. baseline KV eviction methods at similar compression budget; 1.6× shorter generation and 1.7× throughput improvement vs. SoTA

## Trade-offs

- Sentence-level granularity may remove semantically similar but factually distinct reasoning chains; a coarser filter risks removing useful deliberation steps.
- Steering vector adjustment is applied dynamically based on a heuristic; miscalibration could cause the model to generate overly concise responses at the cost of correctness.

## Nuances

- Comparison is to existing KV eviction methods; methods that compress KV via quantization or low-rank approximation rather than eviction are a different design point not directly compared.
- Evaluation on "multiple reasoning benchmarks" is unspecified in the abstract; results may vary across mathematical, coding, and commonsense reasoning tasks.
- The 1.7× throughput improvement is measured under batch inference; single-request latency improvement may differ.
