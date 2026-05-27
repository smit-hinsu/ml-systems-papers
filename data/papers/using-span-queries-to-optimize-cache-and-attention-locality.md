---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Paul Castro
- Nick Mitchell
- Nathan Ordonez
- Thomas Parnell
- Mudhakar Srivatsa
- Antoni Viros-i-Martin
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 10–20× TTFT reduction for two non-chat use cases; attention-optimized
  span query on 2B model outperforms stock 8B model on accuracy.
models_evaluated: []
observations:
  cache: Span query commutativity constraints let the server reorder commutative input
    segments and reuse cached KV states across structurally equivalent queries, eliminating
    redundant prefill.
  tier: Span query optimization places commutative segments with existing KV cache
    hits first in the attention order, maximizing prefix cache reuse and minimizing
    cache misses.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=qcGGSXpFcM
organizations:
- IBM Research
presentation_type: oral
principles:
- cache
- tier
problem: Inference servers optimized for linear chat use poor KV cache strategies
  for inference-time scaling, RAG, and agentic workloads with non-linear input structure.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3747_FfJdljm.pdf
slug: using-span-queries-to-optimize-cache-and-attention-locality
status: draft
title: Using Span Queries to Optimize Cache and Attention Locality
topics:
- prefix-caching
- kv-cache
- sparse-attention
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3747
---

## Background

KV prefix caching reduces TTFT by reusing states when a request starts with the same token prefix. This works for linear chat, but RAG, inference-time scaling, and agentic pipelines have non-linear inputs: retrieved chunks can arrive in any order, reasoning branches share partial context, and tool results are inserted mid-conversation. When document order doesn't match the prefix tree, KV states can't be reused even for semantically identical inputs — serving frameworks have no way to express that segments are interchangeable.

## Key Contributions

- **Span query abstraction**: a generalized representation of inference calls as an expression tree linked by commutativity constraints; chat, RAG, inference-time scaling, and agentic workloads are all special cases that differ only in whether input segments commute.
- **Automatic commutativity optimization**: the inference server reorders commutative input segments (e.g., RAG document chunks) to maximize KV cache locality without changing semantics, enabling 10–20× TTFT reductions for non-chat workloads.
- **Attention locality optimization**: span queries can also be reordered to improve attention computation locality, reducing the "lost-in-the-middle" degradation for long-context inputs; a 2B model with attention-optimized span queries matches an 8B stock inference server on accuracy.
- **Minimal vLLM modification**: span query execution required changes to only 492 lines of vLLM code, demonstrating low integration cost.

## Trade-offs

- Commutativity must be declared explicitly by the client; the server cannot automatically infer which segments commute, requiring application-level annotation.
- Reordering commutative segments for cache locality may change the attention bias and affect model quality in subtle ways; the paper validates accuracy on specific benchmarks but generalization to all use cases is not guaranteed.

## Nuances

- The 10–20× TTFT reduction is measured on two specific non-chat use cases; results depend heavily on the degree of overlap between commutative segments and existing cache state.
- The lost-in-the-middle fix via attention reordering is promising but evaluated on a 2B model; larger models with stronger positional encoding biases (e.g., RoPE with long context) may behave differently.