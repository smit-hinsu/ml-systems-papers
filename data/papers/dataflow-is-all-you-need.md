---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Darshan Gandhi
- Pushkar Nandkar
- David Koeplinger
- Nasim Farahini
- Romy Tsoupidi
- Samuel Rydh
- Matheen Musaddiq
- Tuowen Zhao
- Reid Goodbar
- Nathan Sheeley
- Leon Zhang
- Matthew Shaffer
- John Long
- Han Wang
- Angela Wang
- Arjun Sabnis
- Joshua Brot
- Yun Du
- Hakan Zeffer
- Mingran Wang
- Raghu Prabhakar
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware:
- SambaNova SN40
- H100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: '>75% of theoretical peak roofline on SN40 across diverse models; speculative
  decoding 1.7× faster on 16 SN40 chips vs. DGX H100 despite comparable HBM bandwidth;
  6× speculative decoding speedup'
models_evaluated: []
observations:
  tier: GPUs extract as little as 21% of available memory bandwidth
    for decode due to CPU scheduling and kernel synchronization overhead; SN40 dataflow
    eliminates these overheads by keeping data moving continuously without CPU involvement.
  pipeline: BatchStreaming overlaps KV cache loading for subsequent
    requests with compute for the current request; ScheduleOffloading shifts dispatch
    logic off the compute path entirely, eliminating synchronization gaps between kernels.
  fuse: KernelLooping fuses multiple decode iterations into a single
    persistent kernel, eliminating kernel launch overhead and inter-kernel synchronization
    that forces unnecessary HBM round-trips on GPU architectures.
official_category: ''
openreview_url: https://openreview.net/forum?id=7wOOhxkuN8
organizations:
- SambaNova Systems
presentation_type: oral
principles:
- tier
- pipeline
- fuse
problem: GPU decode is bottlenecked by kernel launch overhead, synchronization, and
  poor compute-communication overlap; even high-bandwidth GPUs extract only 21% of
  available memory bandwidth for autoregressive decode.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: ''
slug: dataflow-is-all-you-need
status: draft
title: Dataflow Is All You Need
topics:
- kv-cache
- speculative-decoding
- moe
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3852
---

## Key Contributions

- **KernelLooping**: fuses multiple autoregressive decode iterations into a single persistent kernel on the SN40 RDU, eliminating inter-iteration kernel launch gaps and synchronization overheads that limit bandwidth utilization on GPUs
- **BatchStreaming**: overlaps KV cache prefetching for the next batch with the compute of the current decode step, hiding memory latency behind compute on the dataflow architecture
- **ScheduleOffloading**: moves token dispatch and scheduling logic off the critical compute path to dedicated control logic on the RDU, eliminating CPU-side scheduling overheads that create bubbles in GPU pipelines
- **Architecture-wide generalization**: all three optimizations apply uniformly to small/large dense models, MoEs, hybrid architectures, and models with different attention mechanisms without model-specific code

## Trade-offs

- Results are specific to SambaNova's SN40 RDU, a proprietary dataflow accelerator; the techniques cannot be directly ported to standard GPU deployments.
- The 1.7× speculative decoding speedup over DGX H100 is for 16 SN40 chips — a non-standard comparison that may not reflect typical per-device or per-dollar efficiency.

## Nuances

- The 21% GPU bandwidth utilization claim is a baseline characterization, not from a published GPU paper; actual GPU utilization varies significantly across serving frameworks and optimizations.
- The >75% roofline efficiency holds across diverse model architectures, but the paper does not characterize performance under heavy multi-user batching scenarios typical in cloud serving.
- The system is deployed in production at cloud.sambanova.ai, making this an industry paper with production validation.
