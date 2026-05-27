---
agentic_models: []
arxiv_url: ''
authors:
- Aditya Ukarande
- Deep Shekhar
- Marc Blackstein
- Ram Rangan
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware:
- Client GPU (NVIDIA IGI SDK)
- CPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: Pipelined sharding achieves up to 6.7x TTFT and 30x TPS improvement for
  LLMs, and 10x VRAM reduction for Cosmos-Reason1 VLM on NVIDIA client GPUs.
models_evaluated:
- Dense LLMs
- MoE LLMs
- Cosmos-Reason1 VLM
observations:
  pipeline: Pipelined sharding overlaps CPU-to-GPU tensor copy with GPU compute, hiding
    memory transfer latency for VRAM-constrained inference.
  tier: Sub-layer sharding with prioritized VRAM placement puts hot tensors on GPU
    and offloads cold tensors to CPU, maximizing effective throughput.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=VKqQYg6JPb
organizations:
- NVIDIA
presentation_type: oral
principles:
- pipeline
- tier
problem: Client VRAM budgets block full LLM and high-res VLM inference; no single
  product handles dense, MoE, and VLM workloads across all client conditions.
project_url: ''
reading_status: want-to-read
research_or_industry: industry
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3802.pdf
slug: efficient-vram-constrained-xlm-inference-on-clients
status: draft
title: Efficient, VRAM-Constrained xLM Inference on Clients
topics:
- cpu-offload
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3802
---

## Background

A typical client GPU has 8–24 GB of VRAM while a 7B FP16 model requires 14 GB. The standard fix is CPU offloading — keeping layers in CPU RAM and copying them to GPU before use — but naive offloading serializes copy and compute, leaving the GPU idle during transfers. VLMs like Cosmos-Reason1 add high-resolution image encoders that push requirements even higher, and client hardware heterogeneity (3–10× CPU-to-GPU bandwidth variation) means no static configuration works across all devices.

## Key Contributions

- **Pipelined sharding**: A CPU-GPU hybrid scheduling technique using sub-layer model sharding, pipelined copy-compute, and prioritized VRAM tensor placement that adapts to runtime system conditions.
- **VLMOpt**: Combines vision tensor CPU offloading, flash attention, and VRAM overlap avoidance for efficient high-resolution VLM inference within client VRAM budgets.

## Trade-offs

- Pipelined sharding introduces latency variability depending on CPU-GPU interconnect bandwidth, which differs across client systems.
- Sub-layer granularity sharding requires profiling to determine optimal split points; this is done via benchmark-profile guidance.

## Nuances

- Targets NVIDIA's IGI SDK and Cosmos-Reason1 products specifically; results depend on client GPU capabilities and CPU-GPU bandwidth.
- The 30x TPS improvement for LLMs is relative to a non-pipelined CPU-offload baseline, not a full GPU baseline.