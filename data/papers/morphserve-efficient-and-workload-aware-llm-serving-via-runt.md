---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Zhaoyuan Su
- Zeyu Zhang
- Tingfeng Lan
- Zirui Wang
- Haiying Shen
- Juncheng Yang
- Yue Cheng
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Reduces SLO violations by 92.45% and improves P95 TTFT by 2.2–3.9× vs.
  full-precision serving; 41.3% less accuracy degradation vs. planning-based quantization
models_evaluated:
- Vicuna
- Llama-2
observations:
  quantize: Precision is chosen once at deploy time for the worst-case burst, so the
    accuracy it costs is paid during every quiet hour as well.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=PDu13oOl4G
organizations:
- University of Virginia
- Harvard University
presentation_type: oral
principles:
- quantize
problem: Static quantization degrades accuracy permanently; full-precision serving
  violates SLOs under bursty load. Neither adapts to real-time workload fluctuations.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3816_X9jZeWW.pdf
slug: morphserve-efficient-and-workload-aware-llm-serving-via-runt
status: draft
title: 'MorphServe: Efficient and Workload-Aware LLM Serving via Runtime Quantized
  Layer Swapping and KV Cache Resizing'
topics:
- quantization
- kv-cache
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3816
---

## Key Contributions

- **Quantized layer swapping**: asynchronous token-level mechanism that selectively replaces less accuracy-sensitive layers with quantized (INT4/INT8) alternatives during high-load periods, preserving generation quality for critical layers
- **Pressure-aware KV cache resizing**: repurposes VRAM freed by layer quantization to dynamically expand KV cache capacity, increasing effective batch size without additional hardware
- **State-preserving transitions**: both mechanisms coordinate at token granularity, avoiding generation interruptions during precision transitions; evaluated on Vicuna and Llama family models with real-world workload traces
- Achieves 92.45% reduction in average SLO violations and 2.2–3.9× P95 TTFT improvement vs. full-precision serving while maintaining generation quality

## Trade-offs

- Quantized layer swapping introduces brief accuracy degradation during high-load periods; application domains with strict quality constraints may not tolerate transient precision reduction.
- The mechanism requires per-layer sensitivity profiling to identify which layers can be safely quantized; this profiling must be done offline before deployment.

## Nuances

- The 41.3% accuracy degradation reduction is relative to planning-based static quantization methods, not full-precision serving; quality is improved over always-quantized but still below always-full-precision.
- Workload traces used for evaluation are from real-world LLM serving; the optimal sensitivity threshold for layer selection may vary across model architectures.