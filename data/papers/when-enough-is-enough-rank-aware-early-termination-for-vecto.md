---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Jianan Lu
- Asaf Cidon
- Michael J. Freedman
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 1.4× higher throughput vs. existing early termination schemes and
  3.2× vs. no early termination at the same accuracy target.
models_evaluated: []
observations:
  approximate: Graph vector search settles the top-ranked neighbor early, then keeps
    paying sequential disk reads for the ranks a RAG consumer barely weighs.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=IFz0pROwF1
organizations:
- Columbia University
- Princeton University
presentation_type: oral
principles:
- approximate
problem: Graph-based vector search reads disk long after the highest-ranked results
  are found, wasting I/O budget on low-value results and limiting throughput.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3835_aLQTTRb.pdf
slug: when-enough-is-enough-rank-aware-early-termination-for-vecto
status: draft
title: 'When Enough is Enough: Rank-Aware Early Termination for Vector Search'
topics:
- prefix-caching
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3835
---

## Background

Graph-based vector indexes such as HNSW walk a proximity graph toward the query, and when the index exceeds RAM each hop is a sequential disk read. The walk finds close neighbors early, then spends a long tail on diminishing returns — the top-1 result is usually settled well before the budget runs out. Existing early-termination schemes stop on a fixed I/O budget or similarity threshold, ignoring that RAG consumers care far more about the top ranks than the rest.

## Key Contributions

- **Terminus**: rank-aware early termination mechanism for disk-based graph vector search; models per-I/O search utility using a rank-weighted function and terminates when recent I/Os yield negligible utility gains, dynamically aligning I/O spending with downstream application rank utility.
- **Rank-weighted utility function**: assigns decreasing marginal utility to progressively lower-ranked results, reflecting the actual value delivered to downstream RAG or retrieval applications that weight top results heavily.
- **Adaptive termination**: terminates search based on the utility curve rather than a fixed I/O budget; recovers more top-ranked results at the same I/O cost compared to static early termination schemes.
- Delivers up to 1.4× higher throughput over existing early termination schemes and up to 3.2× over no early termination at equivalent accuracy, with minimal impact on RAG accuracy.

## Trade-offs

- The rank-weighted utility function must be calibrated to the downstream application's actual rank preferences; miscalibration can cause premature termination (missing critical results) or excessive I/O (not terminating early enough).
- Terminus targets disk I/O-bound vector search; for fully in-memory indexes where I/O is not the bottleneck, the mechanism provides no benefit.

## Nuances

- The 1.4× throughput gain over existing early termination is measured at the same accuracy target; the absolute accuracy level affects where on the accuracy-throughput curve the comparison is made.
- "Minimal impact on RAG accuracy" is evaluated on specific RAG benchmarks; applications where lower-ranked results are equally important (diverse retrieval) would see quality degradation.