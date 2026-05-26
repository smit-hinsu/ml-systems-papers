---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
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
  skip: Terminus terminates disk I/O once recent reads yield negligible
    rank-weighted utility, skipping the long tail of low-value graph traversals that
    existing fixed-budget termination continues.
  cache: Rank-aware termination stops searching after discovering the
    highest-ranked results, avoiding redundant I/Os spent retrieving lower-ranked
    neighbors that contribute minimally to downstream RAG accuracy.
official_category: ''
openreview_url: https://openreview.net/forum?id=IFz0pROwF1
organizations:
- Columbia University
- Princeton University
presentation_type: oral
principles:
- skip
- cache
problem: Graph-based vector search continues reading disk long after the highest-ranked
  results are found, wasting I/O budget on low-value results and limiting throughput.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: when-enough-is-enough-rank-aware-early-termination-for-vecto
status: draft
title: 'When Enough is Enough: Rank-Aware Early Termination for Vector Search'
topics:
- prefix-caching
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3835
---

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
