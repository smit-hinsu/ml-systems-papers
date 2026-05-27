---
agentic_models: []
arxiv_date: ''
arxiv_url: ''
authors:
- Zongpu Zhang
- Pranab Dash
- Qiang Xu
- Y. Charlie Hu
- Jian Li
- Haibing Guan
award: ''
citations: null
citations_updated: ''
code_url: ''
domain:
- llm-serving
hardware: []
indexed_by: smithinsu
indexed_date: '2026-05-25'
key_results: CORE reduces TTFT by 8.5–17.7% and time-per-token by 27.8–39.6% on average
  without increasing energy per token on mobile devices.
models_evaluated: []
observations:
  balance: Default mobile OS governors make independent CPU/GPU/memory decisions;
    CORE cross-resource coordination eliminates 23–40% latency overhead from mismatches
    during prefill and decode.
  pipeline: CORE jointly schedules CPU, GPU, and memory frequencies for each LLM phase
    (prefill vs. decode), overlapping their frequency ramp-up to avoid sequential
    governor delays.
official_category: ''
optimization_type: []
openreview_url: https://openreview.net/forum?id=PSyHQ8kVUT
organizations:
- Purdue University
- Shanghai Jiao Tong University
presentation_type: oral
principles:
- balance
- pipeline
problem: Mobile LLM inference is bottlenecked by independent CPU/GPU/memory frequency
  governors that lack cross-resource coordination, causing 23–40% latency overhead.
project_url: ''
reading_status: want-to-read
research_or_industry: research
slides_url: https://mlsys.org/media/mlsys-2026/Slides/3814_0uuYG7Z.pdf
slug: rethinking-dvfs-for-mobile-llms-unified-energy-aware-schedul
status: draft
title: 'Rethinking DVFS for Mobile LLMs: Unified Energy-Aware Scheduling with CORE'
topics: []
venue: mlsys-2026
venue_url: https://mlsys.org/virtual/2026/oral/3814
---

## Background

Mobile SoCs use DVFS (Dynamic Voltage and Frequency Scaling) to trade frequency for power. Each resource — CPU, GPU, DRAM — has its own governor that makes frequency decisions independently, without awareness of the others. LLM inference has two phases with very different resource profiles: prefill is compute-bound, decode is memory-bandwidth-bound. Independent governors react too slowly and inconsistently to these phase transitions, causing 23–40% latency overhead and 5–16% excess energy from coordination failures alone.

## Key Contributions

- **CORE (unified energy-aware governor)**: jointly coordinates CPU, GPU, and memory frequencies for mobile LLM inference, replacing independent per-resource DVFS governors that make conflicting decisions
- **Phase-aware frequency scheduling**: differentiates prefill (compute-bound) and decode (memory-bound) phases, applying different frequency profiles to match resource demands and minimize energy waste
- **Efficiency characterization study**: first evaluation of default governor inefficiency across multiple mobile LLM frameworks and models; quantifies 23.0–40.4% latency overhead and 5.0–16.6% energy overhead from independent governors
- Achieves 8.5–17.7% TTFT reduction and 27.8–39.6% time-per-token reduction on diverse LLMs without increasing energy per token

## Trade-offs

- CORE requires OS-level access to frequency governors; deployment on locked/production mobile devices without root access may be restricted.
- Optimal frequency profiles are characterized per model; new models require profiling runs to determine the ideal CPU/GPU/memory frequency combination.

## Nuances

- The 23–40% overhead from default governors is measured as a gap vs. optimal frequency combinations; CORE approaches but may not fully close this gap in all configurations.
- Evaluation covers multiple mobile LLM frameworks but does not specify which hardware platforms (SoC models); results may vary across Qualcomm, Apple, and MediaTek chips.