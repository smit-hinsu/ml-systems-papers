---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Huazheng Lao
- Xiaofeng Li
- Rui Xu
- Long Chen
- Xia Zhu
- Jinquan Zhang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 1.3–1.8× higher decoding throughput vs. SoTA recallable sparsity methods
  under different batch sizes
models_evaluated: []
observations:
  skip: Plugin interface decouples sparsity selection from KV cache management so
    any recallable sparsity method integrates without modifying the serving framework,
    enabling clean adoption.
  tier: Object reaggregation groups discrete KV pages before CPU recall, reducing
    PCIe transfer overhead; hot page hit algorithm keeps frequently recalled pages
    GPU-resident, exploiting temporal locality.
official_category: ''
openreview_url: https://openreview.net/forum?id=EB5bgzv4qA
organizations:
- Southeast University
- Guangdong University of Technology
presentation_type: oral
principles:
- tier
- skip
problem: Recallable KV sparsity methods are intrusive to paged KV cache management
  and suffer linearly growing recall overhead at high batch sizes, limiting throughput.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3844_RqcbN0P.pdf
slug: opkv-a-high-throughput-plugin-driven-framework-for-recallabl
status: draft
title: 'OPKV: A High-Throughput Plugin-Driven Framework for Recallable Sparsity in
  Paged KV Cache Systems'
topics:
- kv-cache
- sparse-attention
- cpu-offload
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3844
---

## Background

At large batch sizes, the KV cache for all active sequences doesn't fit in GPU memory, so pages are evicted to CPU RAM and recalled on demand. Recallable sparsity predicts which KV pages each attention step actually needs and skips recalling the rest — but integrating this into paged KV cache systems (like vLLM) requires touching memory management internals, and recall overhead grows linearly with batch size.

## Key Contributions

- **Plugin interface**: decouples sparsity selection logic from model code and KV cache management, allowing any recallable sparsity policy to be integrated into paged KV cache systems without framework modification
- **Object reaggregation**: groups spatially discrete KV pages before CPU recall to exploit spatial locality, reducing PCIe transfer round-trips and recall latency under high batch sizes
- **Hot page hit algorithm**: identifies temporally local KV pages that are recalled repeatedly and keeps them GPU-resident, trading a small amount of GPU memory for large reductions in CPU-GPU recall overhead
- **Millisecond-level metadata manager**: local intra-iteration manager tracks page access patterns and drives eviction decisions with sub-millisecond overhead, enabling fine-grained batch-level cache control
- Achieves 1.3–1.8× higher decoding throughput over SOTA recallable sparsity baselines across batch sizes

## Trade-offs

- Hot page retention consumes additional GPU memory proportional to the hot-set size; under extreme memory pressure the hot page cache may not fit, reducing effectiveness.
- Object reaggregation adds a preprocessing step before each recall operation; for sparse patterns with high spatial locality (already clustered pages), the benefit is marginal.