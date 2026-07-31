---
agentic_models: []
arxiv_url: ''
authors:
- Andrew Bitar
- Aravind Vayalapra
- Baorui Zhou
- Matthew Boyd
- Charlie Wang
- Sahil Parmar
- Eugene Sha
- Gautam Rayaprolu
- Peter Hicks
- Alex Bowe
- Roberto DiCecco
- Santosh Raghavan
- Evan Patrick
- Josip Smolcic
- David Han
- Kris Kang
- Andy Rock
- Josh Hay
- Mohamed Eldafrawy
- Mikhail Kandel
- Omar Kilani
- Liming Gong
- Andrew Paprotskyi
- Arash Taheri-Dezfouli
- Josh Fender
- Andrew Ling
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware:
- GroqChip
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Production SRAM-based LLM inference on thousands of GroqChips serving
  100B+ tokens/day; no HBM bandwidth bottleneck vs. GPU-based decode pipelines.
models_evaluated: []
observations:
  tier: SRAM bandwidth is orders of magnitude higher than HBM;
    placing model weights in on-chip SRAM instead of HBM eliminates the memory bandwidth
    bottleneck that dominates GPU decode latency
  pipeline: Large pipeline of chips partitions the model across SRAM
    tiers, allowing prefill and decode stages to overlap across different pipeline
    stages for sustained high throughput
  fuse: Synchronous low-diameter interconnect enables pipelining across
    thousands of chips without the serialization delays of asynchronous HBM-based
    communication
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=IZaXDwDtL1
organizations:
- Groq
presentation_type: oral
principles:
- tier
- fuse
- pipeline
problem: GPU decode is HBM-bandwidth-bound; loading model weights each token leaves
  FLOPS severely underutilized and caps tokens-per-second per chip.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3834_VmkjzHq.pdf
slug: ship-sram-based-huge-inference-pipelines-for-fast-llm-servin
status: draft
title: 'SHIP: SRAM-Based Huge Inference Pipelines for Fast LLM Serving'
topics:
- kv-cache
- pipeline-parallelism
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3834
---

## Background

Groq's GroqChip carries roughly 220 MB of on-chip SRAM per chip plus a deterministic compiler, instead of the few MB a GPU has next to HBM. Thousands of chips on a synchronous, low-diameter fabric can hold an entire model in SRAM, so decode never pays the HBM weight-loading cost — at the price of far more chips per model.

## Key Contributions

- **SRAM-based inference pipeline (SHIP)**: deploys model weights and KV cache entirely in on-chip SRAM rather than HBM, eliminating the memory bandwidth bottleneck that limits GPU decode throughput; production deployment on Groq's public cloud serving hundreds of billions of tokens daily
- **Synchronous low-diameter interconnect**: connects thousands of GroqChips with a deterministic, low-latency fabric that enables pipeline-parallel model execution without the queuing delays of asynchronous GPU NVLink fabrics
- **Constrained-memory serving optimizations**: techniques for managing KV cache and model weights under SRAM's tighter capacity budget, including context-length-aware batching and prefix strategies that sustain efficiency across varying prefill-to-decode ratios
- Large-scale pipeline design that maintains latency and efficiency under diverse real-world traffic scenarios (varying request sizes, context lengths, and concurrency levels)

## Trade-offs

- SRAM capacity per chip is far smaller than HBM, requiring more chips per model and increasing the cost-per-token for large models compared to high-memory GPU nodes
- Scaling to larger models requires proportionally more chips; the fixed interconnect topology may limit flexibility for models that do not partition cleanly across the pipeline

## Nuances

- The paper does not publish head-to-head latency numbers comparing SHIP to GPU baselines (e.g., H100 or B200); the "state-of-the-art latency" claim is qualitative
- GroqChip is specialized hardware with no publicly available second-source; the architecture's benefits are real but cannot be reproduced without Groq's specific chip
- KV cache capacity is the main operational constraint at scale; how SHIP handles context windows longer than what fits in SRAM pipeline stages is not described in the abstract