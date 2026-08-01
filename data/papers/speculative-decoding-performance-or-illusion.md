---
agentic_models: []
arxiv_date: ''
arxiv_url: https://arxiv.org/abs/2601.11580
authors:
- Xiaoxuan Liu
- Jiaxiang Yu
- Jongseok Park
- Ion Stoica
- Alvin Cheung
award: ''
citations: 12
citations_updated: '2026-07-31'
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 4 SD variants (n-gram, EAGLE, Draft-Model, MTP) consistently underperform
  theoretical speedup on production vLLM; gains diminish at large batch sizes
models_evaluated: []
observations:
  cache: Theoretical speedup analysis reveals verification by the target model dominates
    total execution time, exposing draft generation cost as not the limiting factor
    in production SD settings.
  measure: SD speedups are reported from research prototypes at tiny batches; nobody
    had checked what survives inside production vLLM once continuous batching is already
    saturating the GPU.
  speculate: At large batch sizes, continuous batching fully utilizes the GPU; the
    latency speculation was meant to hide is already absorbed, leaving token verification
    overhead as pure cost.
official_category: ''
openreview_url: https://openreview.net/forum?id=fzkqtezFEi
optimization_type: []
organizations:
- UC Berkeley
presentation_type: oral
principles:
- cache
- speculate
- measure
problem: Speculative decoding speedup claims use research prototypes at small batches;
  production effectiveness on inference engines at scale is unknown.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3782.pdf
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
