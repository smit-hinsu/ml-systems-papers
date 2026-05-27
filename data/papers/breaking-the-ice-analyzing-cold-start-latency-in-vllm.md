---
agentic_models: []
arxiv_url: ''
authors:
- Huzaifa Shaaban Kabakibo
- Animesh Trivedi
- Lin Wang
award: ''
citations: null
citations_updated: ''
code_url: https://github.com/upb-cn/vllm-startup-profiler
domain:
- llm-serving
- observability
hardware:
- CPU
- GPU
indexed_by: smithinsu
indexed_date: '2026-05-24'
key_results: vLLM V1 startup decomposes into 6 CPU-bound phases; analytical model
  predicts startup latency with <10% error across model sizes and hardware configs.
models_evaluated:
- vLLM (various model sizes)
observations:
  cache: Cold start is predominantly CPU-bound across 6 identified phases; the analytical
    model pinpoints which steps can be parallelized or cached to reduce startup.
official_category: ''
openreview_url: https://openreview.net/forum?id=eoEobeKTNZ
organizations:
- University of Paderborn
presentation_type: oral
principles:
- cache
problem: vLLM cold start latency is opaque despite being the default inference engine,
  blocking resource planning for serverless and auto-scaling deployments.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3784.pdf
slug: breaking-the-ice-analyzing-cold-start-latency-in-vllm
status: draft
title: 'Breaking the Ice: Analyzing Cold Start Latency in vLLM'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3784
---

## Background

vLLM cold starts take tens of seconds to several minutes — far longer than typical microservices — because the engine must initialize CUDA contexts, load weights from disk, compile kernels with `torch.compile`, and pre-allocate KV-cache memory before serving any request. For serverless and auto-scaling this forces a hard choice: over-provision to avoid cold starts or accept queuing spikes on traffic surges. Despite vLLM's ubiquity, its startup sequence has no published phase breakdown.

## Key Contributions

- **6-phase startup breakdown**: First systematic decomposition of vLLM's startup process into foundational steps (including torch.compile, model loading, CUDA context init) with fine-grained attribution of latency sources.
- **Analytical prediction model**: A lightweight model that accurately predicts vLLM startup latency given hardware configuration and model parameters, enabling resource planning for large-scale inference environments.

## Trade-offs

- The characterization targets vLLM V1 API; results may shift across versions given vLLM's rapid development pace.
- The analytical model is parameterized empirically and may require re-calibration for unusual hardware or model architectures.

## Nuances

- Startup is predominantly CPU-bound, not GPU-bound — this means more GPU memory or faster GPUs do not help cold start latency.
- torch.compile is a significant contributor to startup time in the V1 API; the paper quantifies this for the first time.