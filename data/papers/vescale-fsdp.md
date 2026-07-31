---
agentic_models: []
arxiv_url: ''
authors:
- Zezhou Wang
- Youjie Li
- Zhiqi Lin
- Jiacheng Yang
- Cong Xie
- Guanyu Feng
- Zheng Zhong
- Ziyue Huang
- Hongyu Zhu
- Zhi Zhang
- Yanghua Peng
- Xin Liu
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 5%–66% higher throughput and 16%–30% lower memory vs. existing FSDP systems;
  scales to tens of thousands of GPUs with zero-copy communications via RaggedShard
models_evaluated: []
observations:
  pipeline: AllGather and ReduceScatter are overlapped with forward/backward
    compute via structure-aware scheduling, hiding collective latency behind local
    computation at each FSDP unit boundary.
  balance: RaggedShard accommodates varying shard sizes arising from block-wise
    quantization or non-uniform layer dimensions, preventing the padding waste that
    fixed-stride sharding incurs
  fuse: veScale-FSDP eliminates the extra memcpy PyTorch FSDP needs
    for contiguous parameter layout before AllGather; structure-aware planning further
    reduces calls by fusing collectives at block granularity.
official_category: Research Papers
optimization_type: []
openreview_url: https://openreview.net/forum?id=3Lj8R0F48P
organizations:
- ByteDance
presentation_type: oral
principles:
- fuse
- pipeline
- balance
problem: FSDP requires flat parameter sharding, making it incompatible with block-wise
  quantization, Shampoo/Muon optimizers, and per-module parallelism strategies.
project_url: ''
reading_status: read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3860.pdf
slug: vescale-fsdp
status: draft
title: 'veScale-FSDP: Flexible and High-Performance FSDP at Scale'
topics:
- fsdp-zero
- quantization
- communication-overlap
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3860
---

## Key Contributions

- **RaggedShard format**: flexible sharding metadata representation that decouples parameter sharding from flat-parameter assumptions, supporting non-uniform block sizes arising from block-wise quantization, sparse layers, or custom module boundaries
- **Structure-aware planning algorithm**: optimizes AllGather and ReduceScatter scheduling at block granularity using the RaggedShard graph, enabling zero-copy communications and fusing collectives across compatible parameter groups
- **Native block-wise quantization integration**: inserts quantize/dequantize transforms directly into the FSDP communication schedule as first-class operations, enabling mixed-precision training without post-hoc wrappers
- **Non-element-wise optimizer support**: first FSDP implementation to natively support Shampoo and Muon optimizers, which require block-structured access to parameter shards incompatible with flat-parameter layouts
- 5%–66% throughput improvement and 16%–30% memory savings vs. PyTorch FSDP and DeepSpeed ZeRO, scaling to tens of thousands of GPUs

## Trade-offs

- RaggedShard metadata graph adds engineering complexity; users must specify sharding patterns explicitly, unlike PyTorch FSDP which automates flat-parameter wrapping
- Structure-aware planning has upfront compilation cost; for short training runs this overhead may not amortize

## Nuances

- The 66% throughput improvement represents the best-case scenario; average gains depend heavily on model architecture and how much quantization or non-standard optimizer usage is involved — simpler models with standard AdamW likely see gains closer to the 5% end
- Scaling claim ("tens of thousands of GPUs") is stated without specifying the exact configurations tested; fault tolerance and recovery behavior at this scale is not characterized
- ByteDance's production use cases motivating the design (e.g., specific model sizes and optimizer combinations) are not fully disclosed, making it difficult to assess how broadly the improvements generalize