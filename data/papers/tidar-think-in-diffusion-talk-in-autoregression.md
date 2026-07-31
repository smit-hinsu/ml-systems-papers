---
agentic_models: []
arxiv_url: 'https://arxiv.org/abs/2511.08923'
authors:
- Jingyu Liu
- Xin Dong
- Zhifan Ye
- Rishabh Mehta
- Yonggan Fu
- vartika singh
- Ce Zhang
- Pavlo Molchanov
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: 4.71×–5.91× tokens/s vs. autoregressive at 1.5B and 8B; surpasses speculative
  decoding and diffusion models (Dream, Llada) in throughput and quality
models_evaluated: []
observations:
  pipeline: Diffusion drafting generates multiple tokens in parallel within a single
    forward pass using structured attention masks, filling GPU compute that is idle
    during sequential AR token generation
  speculate: Diffusion generates candidate token proposals across all positions in
    parallel; the AR phase verifies and commits only accepted positions, hiding full-sequence
    generation behind one pass.
  simplify: A separate drafter must be trained, served, and kept aligned with the
    target, and verification costs a second forward pass — upkeep that buys only
    parallelism one model could supply itself.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=onfxEjoE4L
organizations:
- University of Chicago
- Harvard University
- Georgia Tech
- NVIDIA
presentation_type: oral
principles:
- pipeline
- speculate
- simplify
problem: Speculative decoding serializes generation and needs a draft model; diffusion
  models parallelize token generation but degrade quality vs. AR baselines.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3751_1jPpJd3.pdf
slug: tidar-think-in-diffusion-talk-in-autoregression
status: draft
title: 'TiDAR: Think in Diffusion, Talk in Autoregression'
topics:
- speculative-decoding
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3751
---

## Background

Diffusion language models produce a whole block of tokens at once by iteratively denoising it, so decoding is parallel rather than one token at a time — but their output quality trails autoregressive models. Prior work treats the two as separate families: pick diffusion for speed or AR for quality, and hybrid schemes still need a second draft model.

## Key Contributions

- **TiDAR hybrid architecture**: drafts multiple tokens simultaneously using a diffusion process (Thinking) within a single forward pass, then samples final outputs autoregressively (Talking) using specially designed structured attention masks — no separate draft model required
- **Structured attention masks for single-pass hybrid decoding**: a novel mask design that partitions the attention computation so diffusion token positions attend bidirectionally for drafting while AR output positions attend causally, enabling both modes in one transformer forward pass
- **Serving-friendly standalone design**: unlike traditional speculative decoding which requires a separate draft model and verification pass, TiDAR runs as a single model with no additional inference-time components
- Evaluated at 1.5B and 8B model scales; achieves 4.71×–5.91× throughput improvement over autoregressive baselines while surpassing both speculative decoding and pure diffusion models (Dream, Llada) in combined efficiency and quality

## Trade-offs

- The diffusion drafting stage uses bidirectional attention which is more expensive per token than causal attention; the net throughput gain depends on the draft acceptance rate
- Quality may degrade for tasks requiring strict left-to-right coherence that the diffusion drafting stage can disrupt

## Nuances

- Throughput numbers (4.71×–5.91×) are relative to autoregressive baseline, not to optimized speculative decoding with a well-matched draft model; the comparison to speculative decoding is not rigidly controlled for draft model quality
- Evaluation at 1.5B and 8B sizes leaves it unclear whether the approach scales to frontier model sizes (70B+) where memory bandwidth is the dominant bottleneck and the trade-offs may shift
- The "AR-level quality" claim is validated on standard benchmarks; whether bidirectional diffusion drafting preserves quality on long-context or instruction-following tasks is not fully characterized