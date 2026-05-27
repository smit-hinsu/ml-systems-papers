---
agentic_models: []
arxiv_url: ''
authors:
- Shakya Jayakody
- Youpeng Zhao
- Chinmay Dhanraj Nehate
- Jun Wang
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware:
- GPU cluster
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: GhostServe reduces checkpointing latency by 2.7x, recovery latency by
  2.1x per batch, and median response latency by 1.2x vs existing fault-tolerant methods.
models_evaluated:
- Long-context LLMs (agent-based)
observations:
  cache: Erasure-coded KV cache parity shards in host memory enable fast recovery
    without full KV recomputation after device failure.
  tier: Parity shards are stored in host memory instead of GPU memory, protecting
    the KV cache at minimal GPU memory cost.
official_category: ''
openreview_url: https://openreview.net/forum?id=xKjYiUgeOK
organizations:
- University of Central Florida
presentation_type: oral
principles:
- cache
- tier
problem: Long-running agentic LLM inference is vulnerable to device failures that
  force costly full KV cache recomputation, wasting time and compute.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3736_8a0AKFA.pdf
slug: ghostserve-a-lightweight-checkpointing-system-in-the-shadow-
status: draft
title: 'GhostServe: A Lightweight Checkpointing System in the Shadow for Fault-Tolerant
  LLM Serving'
topics:
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3736
---

## Background

Long-running agentic LLM sessions accumulate large KV caches that encode all prior context. A GPU failure mid-session destroys the KV cache and forces full replay from scratch — a cost that scales with session length. Full KV replication to a second GPU doubles memory pressure. Erasure coding offers a middle ground: parity shards can reconstruct any single lost block at lower storage overhead than replication, but applying it to a streaming, growing KV cache requires careful design.

## Key Contributions

- **Shadow checkpointing with erasure coding**: Applies erasure coding to the streaming KV cache to generate parity shards stored in host memory, enabling fast KV reconstruction after GPU failure without replication overhead.
- **Seamless inference recovery**: On device failure, GhostServe reconstructs the lost KV cache from erasure-coded shards and resumes inference without full recomputation.

## Trade-offs

- Erasure coding adds CPU overhead for parity shard computation; this must be hidden in the critical path.
- Host memory must be large enough to hold parity shards for all active long-context sequences, which can be substantial for million-token contexts.

## Nuances

- The 1.2x median response latency improvement is measured in the presence of failures; under failure-free operation the overhead is minimal.
- GhostServe protects only the KV cache, not model weights; model weight failures require separate handling.