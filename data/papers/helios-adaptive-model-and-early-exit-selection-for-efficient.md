---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Avinash Kumar
- Shashank Nag
- Jason Clemons
- Lizy K. John
- Poulami Das
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 1.48× higher throughput and 15.14× larger batch size vs. existing EE-LLM
  frameworks on single-model early-exit baselines
models_evaluated:
- Early-Exit LLMs
observations:
  balance: Multi-model switching routes tokens that miss early exits on
    one model to another where those tokens do exit, collectively maximizing early-exit
    utilization across the combined ensemble rather than stalling on the single-model
    bottleneck.
  tier: Greedy layer loading loads only weights for layers most
    likely to be used based on profiled exit distributions, freeing HBM for larger
    batch sizes instead of holding all layer weights resident.
official_category: ''
openreview_url: https://openreview.net/forum?id=CV52m9NJFK
organizations:
- University of Texas at Austin
- NVIDIA
presentation_type: oral
principles:
- balance
- tier
problem: EE-LLM serving bottlenecks on tokens that never exit early; loading all
  layer weights wastes HBM that could be used for larger batches.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: helios-adaptive-model-and-early-exit-selection-for-efficient
status: draft
title: 'HELIOS : Adaptive Model And Early-Exit Selection for Efficient LLM Inference
  Serving'
topics:
- memory-management
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3846
---

## Key Contributions

- **Multi-model dynamic switching**: HELIOS maintains a pool of EE-LLM variants and routes each token to the model where it is most likely to exit early; early-exit patterns across models are complementary, reducing the fraction of late-exit tokens that stall throughput.
- **Greedy layer loading**: When a token's predicted exit confidence is low, HELIOS allows it to exit speculatively and loads only the weights for the most likely traversed layers, converting reclaimed HBM into batch-size headroom for a 15.14× batch-size gain.
- **Real-time profiling and adaptive control**: Continuous profiling updates exit distributions per model per request type; token fate tracking corrects quality degradation caused by greedy exits without large offline profiling overheads.

## Trade-offs

- Maintaining multiple EE-LLM models increases aggregate weight storage; the memory savings from greedy loading must exceed the overhead of holding multiple checkpoints.
- Greedy exits introduce occasional token-quality degradation when a token's true confidence is lower than predicted; correctness depends on profiling accuracy.

## Nuances

- Early-exit complementarity is workload-dependent; datasets where all tokens consistently traverse deep layers diminish the multi-model benefit.
- The 15.14× batch-size gain is relative to a single-model EE-LLM that holds all layers in HBM; the comparison to dense-model serving with full batches is not provided.
