---
agentic_models: []
arxiv_date: ''
arxiv_url: 'https://arxiv.org/abs/2511.00606'
authors:
- Jameson Sandler
- Jacob Christopher
- Tom Hartvigsen
- Ferdinando Fioretto
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: +55% tokens-per-second over prior SD baselines; 5.5× avg speedup over
  standard autoregressive decoding on reasoning, coding, and math benchmarks.
models_evaluated: []
observations:
  cache: Drafter calibration aligns draft-token distributions with the autoregressive
    verifier, reducing rejection rates and avoiding wasted verification compute on
    misaligned tokens.
  pipeline: Discrete diffusion drafting generates multiple tokens in parallel in a
    single non-autoregressive pass, eliminating the sequential per-token dependency
    that limits autoregressive drafts.
  speculate: SpecDiff-2 aligns the diffusion drafter to the target LLM distribution;
    higher alignment raises acceptance rates, making the parallel diffusion pass a
    reliable speculative proposal.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=o42VU86ZsV
organizations:
- University of Virginia
presentation_type: oral
principles:
- pipeline
- cache
- speculate
problem: Autoregressive draft models cannot parallelize token drafting; draft-verifier
  misalignment causes high rejection rates that negate speculative decoding speedup.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3755.pdf
slug: specdiff-2-scaling-diffusion-drafter-alignment-for-faster-sp
status: draft
title: 'SpecDiff-2: Scaling Diffusion Drafter Alignment For Faster Speculative Decoding'
topics:
- speculative-decoding
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3755
---

## Background

Discrete diffusion models can emit every draft token in a single non-autoregressive pass, removing the sequential bottleneck in speculative drafting. Their training objective differs from an autoregressive target model, though, so earlier diffusion drafters produced acceptance rates low enough to cancel the parallelism gain.

## Key Contributions

- **Discrete diffusion drafting**: Replaces the autoregressive draft model with a discrete diffusion process that generates all draft tokens in a single non-autoregressive forward pass, parallelizing the drafting stage and removing the sequential bottleneck.
- **Diffusion-autoregressive alignment techniques**: Novel calibration methods align the token distributions produced by the discrete diffusion drafter with those of the autoregressive verifier, directly reducing rejection rates and recapturing speedup lost to distribution mismatch.
- **Joint bottleneck resolution**: SpecDiff-2 simultaneously addresses parallelism (bottleneck 1) and alignment (bottleneck 2), achieving a new best on acceptance length and tokens-per-second across reasoning, coding, and math benchmarks.

## Trade-offs

- Training a discrete diffusion drafter requires a different training procedure than standard autoregressive draft models; existing autoregressive draft checkpoints cannot be directly reused.
- Calibration techniques for drafter-verifier alignment add complexity and training cost; miscalibration would make rejection rates worse than a simple autoregressive drafter.

## Nuances

- The 5.5× speedup is an average over benchmarks; speedup varies significantly by task, sequence length, and model size; some configurations may see lower gains.
- Speculative decoding speedup in general depends on batch size; results at small batch sizes may overstate real-world gains when serving concurrent requests at production scale.