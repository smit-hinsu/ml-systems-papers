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
key_results: '>75% roofline efficiency on SN40; speculative decoding 1.7× faster vs.
  DGX H100 on 16 SN40 chips; 6× speculative decoding speedup over baseline'
models_evaluated: []
observations:
  tier: GPUs extract as little as 21% of memory bandwidth for decode due to CPU
    scheduling overhead; SN40 dataflow keeps data moving continuously without any
    CPU involvement in the critical path.
  pipeline: BatchStreaming overlaps KV cache loading with current compute;
    ScheduleOffloading moves dispatch logic off the compute path, eliminating
    synchronization gaps between kernels on SN40.
  fuse: KernelLooping fuses multiple decode iterations into one persistent kernel,
    eliminating launch overhead and inter-kernel synchronization that forces
    unnecessary HBM round-trips on GPU architectures.
  simplify: GPU decode dispatches every kernel through the CPU at runtime; replacing
    dynamic dispatch with a statically compiled dataflow graph raises bandwidth
    utilization from 21% to >75% of roofline.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=7wOOhxkuN8
organizations:
- SambaNova Systems
presentation_type: oral
principles:
- tier
- pipeline
- fuse
- simplify
problem: GPU decode extracts only 21% of memory bandwidth; kernel launch overhead
  and synchronization gaps block continuous data movement during autoregressive decode.
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

## Background

Autoregressive decode is memory-bandwidth-bound, yet GPUs achieve only ~21% bandwidth utilization because CPU kernel launch, barrier synchronization, and dispatch scheduling inject stall time between every pair of kernels. SambaNova's SN40 Reconfigurable Dataflow Unit (RDU) statically schedules operators into a continuous data-movement graph with no CPU on the critical path — but extracting this advantage for full LLM workloads requires rethinking decode loops, KV prefetching, and speculative decoding for dataflow execution.

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
