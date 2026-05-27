---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Taosong Fang
- Zhen Zheng
- Zhengzhao Ma
- Yaojie Lu
- Hongyu Lin
- Xianpei Han
- Le Sun
award: ''
citations: null
citations_updated: ''
code_label: Available in SGLang
code_url: https://github.com/sgl-project/sglang
domain:
- agentic-inference
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Up to 40% end-to-end latency reduction on real multi-agent workflows;
  3.5× speedup in controlled two-agent benchmarks on SGLang
models_evaluated: []
principles:
- pipeline
- cache
observations:
  pipeline: "Incremental prefill pipelined with upstream decode cuts end-to-end latency up to 40%; the breakeven is when upstream decode time exceeds the per-token prefill overhead on the downstream."
  cache: "Agentic workloads share system prompt prefixes, but the radix cache fills only after a call completes — concurrent calls within the same turn don't benefit by default"
official_category: Research Papers
openreview_url: https://openreview.net/forum?id=m14PPUfgEc
organizations:
- Chinese Academy of Sciences
- Microsoft
presentation_type: oral
problem: In multi-agent LLM pipelines each downstream agent idles during upstream
  decode, waiting for the complete response before it can start its own prefill.
project_url: ''
status: published
reading_status: read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3760_dJT5ZOY.pdf
slug: flashagents
title: 'FlashAgents: Accelerating Multi-Agent LLM Systems via Streaming Prefill Overlap'
topics:
- prefix-caching
- streaming
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3760
---

## Background

In multi-agent LLM pipelines, the downstream agent cannot start prefill until the upstream agent finishes — the full output must be assembled before the next serving engine accepts a job. For long responses this idle wait dominates end-to-end latency. HTTP streaming solves the display problem but most serving frameworks buffer the full prompt before scheduling prefill, so the downstream model sits idle despite having spare capacity.

## Key Contributions

- **Incremental prefill protocol**: forwards each upstream token to the downstream serving
  engine as it is generated; the downstream agent starts prefill from the first upstream
  token rather than waiting for the full prompt, hiding upstream decode behind downstream
  prefill
- **Intra-turn radix-tree prefix cache**: detects shared instruction templates or system
  prompts across concurrent agent calls within a processing turn; after the first call
  populates the cache, subsequent calls within the same turn skip re-computing the shared
  prefix's KV state
- Protocol layer on SGLang requiring no changes to model weights or agent application code

## Trade-offs

- Incremental prefill processes tokens one at a time rather than in a batch, so per-token prefill efficiency is lower than a single batched call — net benefit depends on the ratio of upstream decode time to downstream prefill time.
- Intra-turn prefix cache consumes additional GPU memory proportional to the number of concurrent agent requests sharing a prefix.

## Nuances

- Only linear A→B pipelines are evaluated; fan-out and DAG topologies (one agent broadcasting to N downstream agents) are not characterized and would require protocol changes to handle multiple concurrent upstream token streams.
- The incremental prefill breakeven point — where streaming savings exceed per-token overhead — is not quantified in the paper.
- Upstream speculative decoding or chunked prefill would alter the token emission cadence and may require protocol adaptation.
