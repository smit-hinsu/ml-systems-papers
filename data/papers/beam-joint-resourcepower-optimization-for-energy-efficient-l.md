---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Hyunjae Lee
- Sangjin Choi
- Seungjae Lim
- Youngjin Kwon
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
- fleet-efficiency
hardware:
- GPU
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: Up to 51% reduction in end-to-end GPU energy consumption vs. vLLM while
  meeting per-request TTFT and TBT SLOs
models_evaluated: []
observations:
  balance: BEAM jointly optimizes GPU frequency, chunk size, and microbatch count;
    independent tuning of any single dimension yields only a local optimum, missing
    up to 51% energy savings vs. vLLM.
  pipeline: Event-driven controller responds to request arrivals and completions to
    reallocate latency slack across power and resource dimensions; sub-millisecond
    decisions stay off the critical path.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=BfNBXM8CCT
organizations:
- KAIST
presentation_type: oral
principles:
- balance
- pipeline
problem: LLM inference SLOs leave latency slack unexploited; existing systems tune
  batching or DVFS in isolation rather than jointly, missing compound energy savings.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3849_mCVfQGX.pdf
slug: beam-joint-resourcepower-optimization-for-energy-efficient-l
status: draft
title: 'BEAM: Joint Resource–Power Optimization for Energy-Efficient LLM Inference
  under SLO contraints'
topics:
- continuous-batching
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3849
---

## Key Contributions

- **Joint resource-power controller**: BEAM co-optimizes GPU frequency (DVFS), chunk size, and microbatch count simultaneously rather than treating them as independent knobs; the coupling between these dimensions means independent optimization yields only local optima
- **Latency-slack exploitation**: identifies the gap between earliest possible completion and per-request TTFT/TBT deadlines as an optimization window; distributes slack across resource and power dimensions to minimize energy consumption
- **Event-driven real-time control**: responds to request arrivals and completions immediately; a lightweight predictive model enables sub-millisecond scheduling decisions with negligible overhead
- **51% GPU energy reduction**: implemented atop vLLM runtime, achieves up to 51% lower end-to-end GPU energy consumption compared to vLLM under identical SLO constraints

## Trade-offs

- Joint optimization adds controller complexity; incorrect predictions about remaining latency slack can cause SLO violations if the system becomes too aggressive with frequency scaling.
- DVFS range and granularity are hardware-dependent; GPUs with coarse-grained frequency steps or narrow voltage ranges limit the achievable energy savings.

## Nuances

- The 51% energy reduction is the peak result; average savings across a representative workload mix are not reported in the abstract.
- Results are evaluated against vLLM without energy optimization; energy-aware baselines from the literature (e.g., DVFS-only or batching-only approaches) are the key comparison.