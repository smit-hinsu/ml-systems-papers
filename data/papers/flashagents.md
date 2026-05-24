---
agentic_models: []
arxiv_url: ''
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
code_url: ''
date: '2026-05-19'
domain:
- agentic-inference
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
insights:
- prefix-reuse
- communication-compute-overlap
key_results: Up to 40% end-to-end latency reduction; 3.5× speedup in controlled two-agent
  benchmarks
mlsys_official_category: Research Papers
mlsys_url: https://mlsys.org/virtual/2026/oral/3760
models_evaluated: []
openreview_url: https://openreview.net/forum?id=m14PPUfgEc
organizations: []
presentation_type: oral
problem: In multi-agent LLM pipelines, downstream agents must wait for upstream agents
  to finish before starting their prefill, causing serial latency stacking.
project_url: ''
reading_status: read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3760_dJT5ZOY.pdf
slug: flashagents
techniques:
- prefix-caching
- streaming
- kv-cache
title: 'FlashAgents: Accelerating Multi-Agent LLM Systems via Streaming Prefill Overlap'
---

## Summary

Multi-agent LLM systems have a fundamental latency problem: Agent B cannot start its prefill until Agent A has finished generating its output. FlashAgents attacks this by introducing **token-level streaming between agents**: Agent B begins processing Agent A's tokens as they arrive, rather than waiting for the full response.

Two complementary techniques are introduced:

1. **Inter-agent streaming with incremental prefill**: Downstream agents begin prefilling on partial upstream outputs using a streaming prefill mechanism. As each new token arrives from upstream, it is appended to the KV cache incrementally.

2. **Intra-turn prefix caching with radix trees**: Across turns or parallel agent calls that share a common prompt prefix, a radix-tree-based cache detects redundant prefill computation and reuses cached KV states.

The system is implemented on SGLang.

## Key Contributions

- Token-level inter-agent streaming protocol for prefill overlap
- Radix-tree-based prefix cache for multi-agent workloads
- 40% end-to-end latency reduction; 3.5× speedup in two-agent setting
- Implementation on SGLang

## Method

Incremental prefill proceeds token-by-token from upstream: as each token is generated, it is forwarded to the downstream agent's serving engine, which appends it to a running KV state. The radix cache component handles the common case where multiple downstream agents receive the same system prompt or context prefix, avoiding redundant computation.

## Results

- Up to 40% end-to-end latency reduction
- 3.5× speedup in controlled two-agent benchmarks

## Limitations

- Evaluation limited to two-agent pipelines; DAG or fan-out agent topologies not fully characterized
- Incremental prefill has overhead per token vs. batched prefill; breakeven point not fully analyzed

## Personal Notes

<!-- Add your own observations, questions, and connections to other work here -->