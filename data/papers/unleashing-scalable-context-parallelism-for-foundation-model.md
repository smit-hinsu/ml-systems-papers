---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Yilong Zhao
- Xiaonan Nie
- Kan Zhu
- Shuang Ma
- Zhichao Lai
- Hongxiang Hao
- Yang Zhou
- Baris Kasikci
- Ion Stoica
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-training
hardware:
- NVIDIA GPU
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Near-linear scalability on up to 256 GPUs with 1.13×–2.21× improvement
  in attention MFU over prior context parallelism methods.
models_evaluated: []
observations:
  balance: Block-level bin-packing of short and long sequence fragments across workers
    eliminates workload imbalance from over-sharding, improving attention MFU by up
    to 2.21× vs. prior context parallelism.
  fuse: Arbitrary peer-to-peer communication topology (vs. fixed ring) allows FCP
    to place sequence blocks on workers that minimize cross-node transfers for the
    actual sequence distribution.
official_category: ''
openreview_url: https://openreview.net/forum?id=MPVycRsIn6
organizations:
- University of Washington
- UC Berkeley
presentation_type: oral
principles:
- balance
- fuse
problem: Existing context parallelism designs over-shard short sequences or batch
  them separately, causing compute inefficiency and imbalance during LLM pretraining.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3822_HdG9Mug.pdf
slug: unleashing-scalable-context-parallelism-for-foundation-model
status: draft
title: Unleashing Scalable Context Parallelism for Foundation Models Pre-Training
  via FCP
topics:
- tensor-parallelism
- communication-overlap
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3822
---

## Background

Context parallelism shards long sequences across GPUs using ring-pattern collectives so each worker sees the full sequence. The difficulty is length diversity in pretraining datasets: short documents (hundreds of tokens) mixed with very long ones (millions). Existing designs either over-shard short sequences — many workers holding tiny slices, wasting bandwidth — or process short and long sequences in separate batches, losing throughput. Neither adapts the communication topology to the actual sequence distribution.

## Key Contributions

- **FCP (Flexible Context Parallelism)**: shards and schedules sequences at block-level granularity rather than at fixed sequence-level granularity; replaces rigid ring communication topologies with arbitrary peer-to-peer communication for flexible block placement.
- **Block-level bin-packing**: packs blocks from both short and long sequences across workers to achieve balanced compute loads per iteration, eliminating the efficiency loss from over-sharding short sequences or processing them separately.
- **Arbitrary P2P communication topology**: decouples the communication pattern from the sequence distribution; FCP selects transfers that minimize cross-node traffic for the actual block placement rather than following a fixed ring order.
- Evaluated on up to 256 NVIDIA GPUs; achieves near-linear scalability with 1.13×–2.21× improvement in attention MFU over prior context parallelism methods.

## Trade-offs

- Arbitrary P2P communication requires a topology-aware scheduler that adds overhead at the planning phase; for very short sequences where ring communication has negligible imbalance, the scheduling overhead may not be amortized.
- Block-level granularity increases the number of communication messages relative to sequence-level sharding; at very high GPU counts this may stress the network fabric with small messages.

## Nuances

- The 2.21× MFU improvement is the upper bound across evaluated configurations; workloads with more uniform sequence length distributions will see smaller gains.
- FCP focuses on attention context parallelism; the interaction with tensor and pipeline parallelism in full training pipelines is not deeply characterized.