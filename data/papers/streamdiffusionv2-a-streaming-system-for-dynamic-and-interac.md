---
agentic_models: []
arxiv_url: ''
arxiv_date: ''
authors:
- Tianrui Feng
- Zhi Li
- Shuo Yang
- Haocheng Xi
- Muyang Li
- Xiuyu Li
- Lvmin Zhang
- Keting Yang
- Kelly Peng
- Song Han
- Maneesh Agrawala
- Kurt Keutzer
- Akio Kodaira
- Chenfeng Xu
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware:
- NVIDIA H100
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: 58.28 FPS on 14B model and 64.52 FPS on 1.3B model on 4× H100 with first
  frame under 0.5 s.
models_evaluated:
- CogVideoX-5B (14B parameter video diffusion)
- 1.3B parameter video diffusion
observations:
  pipeline: Pipeline orchestration parallelizes denoising steps across
    GPUs; near-linear FPS scaling achieved without violating per-frame latency deadlines.
  cache: Sink-token-guided rolling KV cache reuses attention state
    across streaming frames, avoiding full recomputation each generation step.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=p9WALNBvc6
organizations:
- MIT
- UC Berkeley
- Stanford University
presentation_type: oral
principles:
- pipeline
- cache
problem: Offline video diffusion systems optimize throughput via batching but cannot
  meet strict per-frame SLOs and time-to-first-frame requirements of live streaming.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: ''
slug: streamdiffusionv2-a-streaming-system-for-dynamic-and-interac
status: draft
title: 'StreamDiffusionV2: A Streaming System for Dynamic and Interactive Video Generation'
topics:
- streaming
- continuous-batching
- kv-cache
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3750
---

## Background

Video diffusion models produce each frame by iteratively denoising over many steps. Offline generation optimizes throughput, but live streaming imposes hard SLOs: 30+ FPS at a fixed rate with sub-second time-to-first-frame. At 14B parameters a single denoising forward pass already exceeds the inter-frame budget, and existing diffusion serving stacks schedule with no notion of SLOs.

## Key Contributions

- **SLO-aware batching scheduler**: jointly enforces time-to-first-frame and per-frame deadline constraints; dynamically batches live-streaming requests to maximize throughput without violating latency SLOs.
- **Block scheduler**: coordinates denoising block execution order across pipeline stages to maintain frame pipelining under heterogeneous GPU environments.
- **Sink-token-guided rolling KV cache**: maintains a compact rolling attention context across generated frames using sink tokens, eliminating full KV recomputation per frame and enabling temporal consistency without retraining.
- **Motion-aware noise controller**: modulates noise injection based on detected motion, preserving temporal consistency between frames under variable-motion content.
- **Scalable pipeline orchestration**: parallelizes the diffusion process across denoising steps and network layers on multiple GPUs; achieves near-linear FPS scaling to 4× H100 without violating latency guarantees.
- Achieves 58.28 FPS (14B model) and 64.52 FPS (1.3B model) on 4× H100, with first-frame latency under 0.5 s and no TensorRT or quantization.

## Trade-offs

- Pipeline parallelism across denoising steps introduces inter-GPU KV-transfer overhead; at low GPU counts or short denoising steps the communication cost may offset the FPS gains.
- The rolling KV cache trades off full temporal context depth for bounded memory; very long live-stream sessions may lose distant temporal coherence.

## Nuances

- Evaluation is training-free; adapting to new video diffusion architectures may require redesigning the block scheduler and rolling KV cache integration.
- Flexible denoising steps (1–4) enable a quality-latency tradeoff; the 58.28 FPS result uses minimal steps and may reduce visual quality for high-motion content.
