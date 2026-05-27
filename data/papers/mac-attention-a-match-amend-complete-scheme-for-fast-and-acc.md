---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Jinghan Yao
- Sam Jacobs
- Walid Krichene
- Masahiro Tanaka
- Dhabaleswar Panda
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Reduces KV accesses by up to 99% and cuts token generation latency by
  over 60% at 128K context; up to 14.3× attention-phase speedup
models_evaluated: []
observations:
  cache: Pre-RoPE L2 matching over a local window finds semantically similar prior
    queries; reusing their attention output cuts constant-complexity decode regardless
    of context length.
  tier: Amend stage recomputes only a small band near the match boundary in SRAM rather
    than re-reading the full KV cache from HBM, keeping memory traffic O(1) on hit.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=b6HBRCejb7
organizations:
- Ohio State University
- Microsoft
- Anyscale
presentation_type: oral
principles:
- cache
- tier
problem: Long-context LLM decode re-reads the full ever-growing KV cache for every
  token, making inference IO-bound at 128K+ context lengths.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3794_HiTCC0P.pdf
slug: mac-attention-a-match-amend-complete-scheme-for-fast-and-acc
status: draft
title: 'MAC-Attention: a Match--Amend--Complete scheme for fast and accurate attention
  computation'
topics:
- kv-cache
- sparse-attention
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3794
---

## Background

At 128K token contexts, each decode step reads the full KV cache from HBM — an O(N) memory transfer that grows with every generated token. FlashAttention minimizes passes but can't reduce total bytes transferred. Sparse attention (sliding-window, StreamingLLM) drops tokens to cut reads but accepts accuracy loss. MAC-Attention exploits a different observation: nearby tokens often have semantically similar queries, so prior attention outputs can be reused instead of recomputed.

## Key Contributions

- **Match stage**: pre-RoPE L2 similarity search over a short local window identifies a prior query whose attention output can be reused; on a hit, KV access complexity becomes O(1) independent of context length
- **Amend stage**: recomputes attention only over a narrow band near the match boundary, correcting for positional drift without re-reading the full cache
- **Complete stage**: numerically stable merge of the rectified reused result with fresh attention over the KV tail (recently added tokens), ensuring full coverage
- System composes with IO-aware kernels (FlashAttention), paged-KV managers, and MQA/GQA without model weight changes; evaluated on LongBench v2 (120K), RULER (120K), and LongGenBench (16K)

## Trade-offs

- Benefits only materialize on match hits; cold-start sequences or highly diverse query streams will see little reduction in KV traffic since the local window may not contain a semantically similar prior query.
- Pre-RoPE matching adds a search cost over the local window on every decode step; for very short contexts where the KV cache is small, this overhead may offset the gain.

## Nuances

- Evaluation compares against full-attention quality rather than against other sparse/compressed attention methods directly; comparison to eviction-based methods is indirect.
- The local window size for matching is a hyperparameter whose optimal value likely varies with domain and generation style; the paper fixes a single setting.