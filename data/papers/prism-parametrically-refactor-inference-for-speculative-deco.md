---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Xuliang Wang
- Yuetao Chen
- Maochan Zhen
- Fang Liu
- Xinzhou Zheng
- Xingwu Liu
- Hong Xu
- Ming Li
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: PRISM boosts decoding throughput 2.6× on a highly optimized engine and
  outperforms existing draft architectures on acceptance length at minimal draft latency
models_evaluated: []
observations:
  cache: By splitting capacity across separate parameter sets, PRISM avoids executing
    unused model capacity for each draft token, keeping per-token draft latency low
    while maintaining high acceptance length.
  pipeline: PRISM disaggregates each draft step across disjoint parameter sets, allowing
    subsets to compute in parallel rather than a single sequential forward pass through
    a large draft model.
  speculate: PRISM extracts shared prefix layers from the target and adds thin adapter
    heads; shared-prefix drafting reuses the target's own computation, keeping the
    drafter close to the target distribution.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=cvU2HuuxEf
organizations:
- Chinese University of Hong Kong
- University of Science and Technology of China
- Northwestern Polytechnical University
- Dalian University of Technology
- University of Waterloo
presentation_type: oral
principles:
- pipeline
- cache
- speculate
problem: Larger speculative decoding draft models improve acceptance length but add
  prohibitive compute overhead, creating a fundamental accuracy-vs-latency trade-off.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3789.pdf
slug: prism-parametrically-refactor-inference-for-speculative-deco
status: draft
title: 'PRISM: Parametrically Refactor Inference for Speculative Decoding Draft Models'
topics:
- speculative-decoding
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3789
---

## Background

Speculative decoding has a small draft model propose several tokens, then the large target model verifies them in parallel — gaining throughput proportional to how many draft tokens are accepted. The core tension: small drafters are fast but diverge from the target distribution; large drafters improve acceptance length but add enough compute overhead to eliminate the speedup. Architectural tricks (SSM drafters, multi-head drafters) have narrowed but not broken this trade-off.

## Key Contributions

- **Parameter set disaggregation**: PRISM decouples model capacity from inference cost by distributing each draft prediction step across multiple disjoint parameter sets instead of a single monolithic forward pass, enabling high-capacity drafting at low per-step latency.
- **Superior acceptance length**: Across benchmarks, PRISM achieves longer acceptance lengths than all existing draft architectures (SSM drafters, small LM drafters, multi-head drafters) while maintaining competitive draft latency.
- **Improved data scaling**: PRISM scales more effectively with expanding training data volumes than other draft architectures, revealing a favorable data scaling law not shared by prior approaches.

## Trade-offs

- Disaggregated parameter sets increase the number of weight tensors and associated memory bandwidth pressure; the implementation must carefully schedule parameter access to keep draft overhead low.
- PRISM requires re-training a custom draft architecture; it cannot be applied as a drop-in replacement using existing draft model checkpoints.

## Nuances

- The 2.6× throughput gain is measured on an already highly optimized inference engine, making it a strong baseline; the relative improvement on less optimized systems could be higher or lower depending on the bottleneck.
- The data scaling advantage of PRISM over other architectures implies that its full benefit requires substantially more training data, which may increase the cost of producing a PRISM draft model.