---
slug: breaking-the-ice-analyzing-cold-start-latency-in-vllm
title: "Breaking the Ice: Analyzing Cold Start Latency in vLLM"
authors:
- Huzaifa Shaaban Kabakibo
- Animesh Trivedi
- Lin Wang
organizations:
- University of Paderborn
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3784
openreview_url: https://openreview.net/forum?id=eoEobeKTNZ
arxiv_url: ''
presentation_type: oral
official_category: ''
award: ''
status: draft
reading_status: want-to-read
research_or_industry: research
indexed_by: smithinsu
indexed_date: '2026-05-24'
citations: null
citations_updated: ''
code_url: 'https://github.com/upb-cn/vllm-startup-profiler'
project_url: ''
slides_url: ''
domain:
- llm-serving
- observability
hardware:
- CPU
- GPU
models_evaluated:
- vLLM (various model sizes)
agentic_models: []
topics: []
principles:
- cache
observations:
  cache: "Cold start is predominantly CPU-bound across 6 identified phases; the analytical model pinpoints which steps can be parallelized or cached to reduce startup."
problem: "vLLM cold start latency is opaque despite being the default inference engine, blocking resource planning for serverless and auto-scaling deployments."
key_results: "vLLM V1 startup decomposes into 6 CPU-bound phases; analytical model predicts startup latency with <10% error across model sizes and hardware configs."
---

## Key Contributions

- **6-phase startup breakdown**: First systematic decomposition of vLLM's startup process into foundational steps (including torch.compile, model loading, CUDA context init) with fine-grained attribution of latency sources.
- **Analytical prediction model**: A lightweight model that accurately predicts vLLM startup latency given hardware configuration and model parameters, enabling resource planning for large-scale inference environments.

## Trade-offs

- The characterization targets vLLM V1 API; results may shift across versions given vLLM's rapid development pace.
- The analytical model is parameterized empirically and may require re-calibration for unusual hardware or model architectures.

## Nuances

- Startup is predominantly CPU-bound, not GPU-bound — this means more GPU memory or faster GPUs do not help cold start latency.
- torch.compile is a significant contributor to startup time in the V1 API; the paper quantifies this for the first time.
