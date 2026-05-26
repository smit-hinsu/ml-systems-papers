---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Xiaoxuan Liu
- Jiaxiang Yu
- Jongseok Park
- Ion Stoica
- Alvin Cheung
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: First systematic study of speculative decoding on production vLLM; reveals
  substantial gaps between observed and theoretical speedup upper bounds across n-gram,
  EAGLE/EAGLE-3, Draft-Model, and MTP variants at real batch sizes
models_evaluated: []
observations:
  balance: Acceptance length varies markedly across output token positions,
    requests, and datasets; this uneven acceptance distribution means SD benefits
    are concentrated in a fraction of tokens and diminish as batch size grows because
    verification cost dominates.
  cache: Theoretical speedup analysis reveals that verification by
    the target model dominates total execution time, exposing that draft generation
    cost is not the limiting factor for many SD configurations in production settings.
official_category: ''
openreview_url: https://openreview.net/forum?id=fzkqtezFEi
organizations:
- UC Berkeley
presentation_type: oral
principles:
- balance
- cache
problem: Speculative decoding speedup claims rely on research prototypes and small
  batch sizes; its real-world effectiveness on production inference engines at scale
  is unknown.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: speculative-decoding-performance-or-illusion
status: draft
title: 'Speculative Decoding: Performance or Illusion?'
topics:
- speculative-decoding
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3782
---

## Key Contributions

- **First production-grade SD evaluation**: Systematic study of four SD variants (n-gram, EAGLE/EAGLE-3, Draft-Model, Multi-Token Prediction) on production vLLM, covering diverse workloads, model scales, and batch sizes rather than research prototypes.
- **Theoretical speedup upper bound**: Derives and quantifies the gap between measured SD performance and the theoretical maximum speedup, providing a principled tool for identifying where optimization effort will have the most impact.
- **Acceptance length analysis**: Characterizes how acceptance length varies across token positions, requests, and datasets, explaining why SD performance degrades at larger batch sizes where verification dominates.

## Trade-offs

- The study focuses on vLLM and may not generalize to other production engines (TensorRT-LLM, SGLang) with different verification and batching implementations.
- Providing an upper bound highlights gaps but does not prescribe specific techniques to close them; translating findings to actionable improvements requires further work.

## Nuances

- The finding that verification dominates execution suggests that SD speedup depends critically on verifier batching efficiency, not just draft quality — a system design insight often overlooked in algorithm-focused SD papers.
- Acceptance length variation across datasets implies that SD benefit is highly workload-dependent; deployments should profile their specific request distribution before relying on SD for latency targets.
