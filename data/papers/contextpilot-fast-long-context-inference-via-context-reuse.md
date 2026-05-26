---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Yinsicheng Jiang
- Yeqi Huang
- Liang Cheng
- Cheng Deng
- Xuan Sun
- Luo Mai
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/EfficientContext/ContextPilot
domain:
- llm-serving
- agentic-inference
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 3× prefill latency reduction vs. state-of-the-art methods while
  preserving—or even improving—reasoning quality at longer context lengths
models_evaluated: []
observations:
  cache: Context index identifies overlapping context blocks across
    users and turns; alignment and de-duplication maximize KV-cache reuse so shared
    context is computed at most once, regardless of surface-level textual differences.
  tier: Succinct context annotations prevent reasoning quality
    degradation under reuse, enabling safe KV-cache sharing where prior approaches
    required full recomputation to maintain accuracy.
official_category: ''
openreview_url: https://openreview.net/forum?id=RnKvDy1jv2
organizations:
- University of Edinburgh
presentation_type: oral
principles:
- cache
- tier
problem: Long-context prefill dominates latency in RAG/agent workloads; prior KV-cache
  reuse techniques either degrade reasoning quality or fail to surface real reuse.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: contextpilot-fast-long-context-inference-via-context-reuse
status: draft
title: 'ContextPilot: Fast Long-Context Inference via Context Reuse'
topics:
- prefix-caching
- kv-cache
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3810
---

## Key Contributions

- **Context index**: identifies overlapping context blocks across LLM interactions (across users and conversation turns), enabling KV-cache reuse even when inputs are not identical prefixes
- **Context alignment and de-duplication**: normalizes overlapping blocks so that semantically equivalent context spans share the same KV cache entry, maximizing hit rates beyond exact-match prefix caching
- **Succinct context annotations**: lightweight annotations attached to reused KV cache entries that preserve reasoning quality, solving the accuracy-reuse tradeoff that forces other systems to recompute
- **Modular integration layer**: clean interface that plugs into existing inference engines without model weight changes; 3× prefill latency reduction vs. state-of-the-art methods

## Trade-offs

- Context index and alignment preprocessing add overhead proportional to context length; very short contexts may see net latency increase from the bookkeeping cost.
- Succinct annotations consume additional KV cache memory; the overhead scales with the number of distinct shared contexts being annotated.

## Nuances

- The 3× speedup is relative to state-of-the-art prior methods, not naive full recompute; absolute wall-clock savings depend on the fraction of context that actually overlaps across concurrent requests.
- The claim that longer contexts improve reasoning quality under reuse is counter-intuitive; it likely applies when de-duplication removes redundant or noisy context segments rather than load-bearing information.
